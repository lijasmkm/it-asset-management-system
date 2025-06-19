"""
Backup Controller for IT Asset Management System
Handles business logic for database backups
"""
import os
import time
import schedule
import threading
from datetime import datetime
from src.models.backup_model import BackupModel

class BackupController:
    def __init__(self, current_user=None):
        """
        Initialize the backup controller
        
        Args:
            current_user (dict, optional): The currently logged in user
        """
        self.backup_model = BackupModel()
        self.current_user = current_user
        self.backup_thread = None
        self.is_scheduled = False
    
    def create_backup(self):
        """
        Create a backup of the database
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        return self.backup_model.create_backup()
    
    def get_all_backups(self):
        """
        Get all backup records
        
        Returns:
            list: List of backup dictionaries
        """
        return self.backup_model.get_all_backups()
    
    def restore_backup(self, backup_id):
        """
        Restore the database from a backup
        
        Args:
            backup_id (int): ID of the backup to restore
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if user has permission to restore backups
        if self.current_user and self.current_user.get('role') != 'administrator':
            return False, "You don't have permission to restore backups"
        
        return self.backup_model.restore_backup(backup_id)
    
    def schedule_daily_backup(self, time_str="00:00"):
        """
        Schedule a daily backup at the specified time
        
        Args:
            time_str (str): Time to run the backup in 24-hour format (HH:MM)
        
        Returns:
            bool: True if scheduled successfully, False otherwise
        """
        if self.is_scheduled:
            return False
        
        try:
            # Schedule the backup
            schedule.every().day.at(time_str).do(self._run_backup)
            
            # Start the scheduler in a separate thread
            self.backup_thread = threading.Thread(target=self._run_scheduler)
            self.backup_thread.daemon = True
            self.backup_thread.start()
            
            self.is_scheduled = True
            return True
        except Exception as e:
            print(f"Error scheduling backup: {e}")
            return False
    
    def _run_scheduler(self):
        """
        Run the scheduler in a loop
        """
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _run_backup(self):
        """
        Run the backup operation (called by the scheduler)
        """
        print(f"Running scheduled backup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        success, message = self.backup_model.create_backup()
        print(f"Backup result: {message}")
        return success
