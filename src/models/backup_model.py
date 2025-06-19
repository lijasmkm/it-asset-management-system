"""
Backup Model for IT Asset Management System
Handles all database operations related to backups
"""
import os
import sqlite3
import shutil
from datetime import datetime, timedelta
from src.config.database import db_config

class BackupModel:
    def __init__(self):
        """Initialize the backup model"""
        self.db = db_config
        self.backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backups')
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        """
        Create a backup of the database
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"assets_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Copy the database file
            shutil.copy2(self.db.db_path, backup_path)
            
            # Record the backup in the database
            self.db.connect()
            self.db.cursor.execute(
                "INSERT INTO backups (filename, path, size, status) VALUES (?, ?, ?, ?)",
                (backup_filename, backup_path, os.path.getsize(backup_path), 'success')
            )
            self.db.commit()
            
            # Clean up old backups (older than 365 days)
            self._cleanup_old_backups()
            
            return True, f"Backup created successfully: {backup_filename}"
            
        except Exception as e:
            # Log the error
            if hasattr(self, 'db') and self.db.connection:
                self.db.cursor.execute(
                    "INSERT INTO backups (filename, path, size, status) VALUES (?, ?, ?, ?)",
                    (backup_filename, backup_path, 0, f'error: {str(e)}')
                )
                self.db.commit()
            
            return False, f"Backup error: {e}"
        finally:
            if hasattr(self, 'db') and self.db.connection:
                self.db.close()
    
    def _cleanup_old_backups(self):
        """
        Remove backups older than 365 days
        """
        try:
            # Calculate the cutoff date (365 days ago)
            cutoff_date = datetime.now() - timedelta(days=365)
            cutoff_str = cutoff_date.strftime('%Y%m%d')
            
            # Get all backup files
            backup_files = os.listdir(self.backup_dir)
            
            for filename in backup_files:
                if filename.startswith('assets_backup_'):
                    # Extract the date from the filename
                    try:
                        file_date_str = filename.split('_')[2].split('.')[0][:8]  # Extract YYYYMMDD
                        
                        # If the file is older than the cutoff date, delete it
                        if file_date_str < cutoff_str:
                            file_path = os.path.join(self.backup_dir, filename)
                            os.remove(file_path)
                            
                            # Update the status in the database
                            self.db.cursor.execute(
                                "UPDATE backups SET status = 'deleted (expired)' WHERE filename = ?",
                                (filename,)
                            )
                    except (IndexError, ValueError):
                        # Skip files with invalid naming format
                        continue
            
            self.db.commit()
            
        except Exception as e:
            print(f"Error cleaning up old backups: {e}")
    
    def get_all_backups(self):
        """
        Get all backup records
        
        Returns:
            list: List of backup dictionaries
        """
        try:
            self.db.connect()
            
            self.db.cursor.execute("SELECT * FROM backups ORDER BY created_at DESC")
            backups = self.db.cursor.fetchall()
            
            # Convert sqlite3.Row objects to dictionaries
            return [dict(backup) for backup in backups]
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            self.db.close()
    
    def restore_backup(self, backup_id):
        """
        Restore the database from a backup
        
        Args:
            backup_id (int): ID of the backup to restore
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            self.db.connect()
            
            # Get the backup record
            self.db.cursor.execute("SELECT * FROM backups WHERE id = ?", (backup_id,))
            backup = self.db.cursor.fetchone()
            
            if not backup:
                return False, "Backup not found"
            
            # Check if the backup file exists
            if not os.path.exists(backup['path']):
                return False, "Backup file not found"
            
            # Close the database connection
            self.db.close()
            
            # Create a backup of the current database before restoring
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pre_restore_backup = f"pre_restore_backup_{timestamp}.db"
            pre_restore_path = os.path.join(self.backup_dir, pre_restore_backup)
            shutil.copy2(self.db.db_path, pre_restore_path)
            
            # Restore the database
            shutil.copy2(backup['path'], self.db.db_path)
            
            # Record the restore operation
            self.db.connect()
            self.db.cursor.execute(
                "INSERT INTO backups (filename, path, size, status) VALUES (?, ?, ?, ?)",
                (pre_restore_backup, pre_restore_path, os.path.getsize(pre_restore_path), 
                 f'pre-restore backup before restoring {backup["filename"]}')
            )
            self.db.commit()
            
            return True, f"Database restored successfully from {backup['filename']}"
            
        except Exception as e:
            return False, f"Restore error: {e}"
        finally:
            if hasattr(self, 'db') and self.db.connection:
                self.db.close()
