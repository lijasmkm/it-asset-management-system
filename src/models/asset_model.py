"""
Asset Model for IT Asset Management System
Handles all database operations related to assets
"""
import sqlite3
from datetime import datetime
from src.config.database import db_config

class AssetModel:
    def __init__(self):
        """Initialize the asset model"""
        self.db = db_config
    
    def add_asset(self, asset_data):
        """
        Add a new asset to the database
        
        Args:
            asset_data (dict): Dictionary containing asset data
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            self.db.connect()
            
            # Check if serial number already exists
            self.db.cursor.execute("SELECT id FROM assets WHERE serial_number = ?", 
                                (asset_data.get('serial_number'),))
            if self.db.cursor.fetchone():
                return False, "Asset with this serial number already exists"
            
            # Prepare fields and values for insertion
            fields = []
            values = []
            placeholders = []
            
            for key, value in asset_data.items():
                if key != 'id':  # Skip id for new assets
                    fields.append(key)
                    values.append(value)
                    placeholders.append('?')
            
            # Add timestamps
            fields.extend(['created_at', 'updated_at'])
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            values.extend([current_time, current_time])
            placeholders.extend(['?', '?'])
            
            # Build and execute the query
            query = f"INSERT INTO assets ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            self.db.cursor.execute(query, values)
            
            asset_id = self.db.cursor.lastrowid
            self.db.commit()
            
            return True, f"Asset added successfully with ID: {asset_id}"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            self.db.close()
    
    def update_asset(self, asset_id, asset_data):
        """
        Update an existing asset
        
        Args:
            asset_id (int): ID of the asset to update
            asset_data (dict): Dictionary containing updated asset data
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            self.db.connect()
            
            # Check if asset exists
            self.db.cursor.execute("SELECT id FROM assets WHERE id = ?", (asset_id,))
            if not self.db.cursor.fetchone():
                return False, "Asset not found"
            
            # Check if updating to a serial number that already exists
            if 'serial_number' in asset_data:
                self.db.cursor.execute(
                    "SELECT id FROM assets WHERE serial_number = ? AND id != ?", 
                    (asset_data['serial_number'], asset_id)
                )
                if self.db.cursor.fetchone():
                    return False, "Another asset with this serial number already exists"
            
            # Prepare fields and values for update
            set_clause = []
            values = []
            
            for key, value in asset_data.items():
                if key != 'id':  # Skip id for updates
                    set_clause.append(f"{key} = ?")
                    values.append(value)
            
            # Add updated_at timestamp
            set_clause.append("updated_at = ?")
            values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # Add asset_id to values
            values.append(asset_id)
            
            # Build and execute the query
            query = f"UPDATE assets SET {', '.join(set_clause)} WHERE id = ?"
            self.db.cursor.execute(query, values)
            
            if self.db.cursor.rowcount == 0:
                return False, "No changes made to the asset"
                
            self.db.commit()
            return True, "Asset updated successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            self.db.close()
    
    def delete_asset(self, asset_id):
        """
        Delete an asset from the database
        
        Args:
            asset_id (int): ID of the asset to delete
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            self.db.connect()
            
            # Check if asset exists
            self.db.cursor.execute("SELECT id FROM assets WHERE id = ?", (asset_id,))
            if not self.db.cursor.fetchone():
                return False, "Asset not found"
            
            # Delete the asset
            self.db.cursor.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
            self.db.commit()
            
            return True, "Asset deleted successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            self.db.close()
    
    def get_asset_by_id(self, asset_id):
        """
        Get an asset by its ID
        
        Args:
            asset_id (int): ID of the asset to retrieve
        
        Returns:
            dict: Asset data if found, None otherwise
        """
        try:
            self.db.connect()
            
            self.db.cursor.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
            asset = self.db.cursor.fetchone()
            
            if asset:
                # Convert sqlite3.Row to dict
                return dict(asset)
            return None
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.db.close()
    
    def get_asset_by_serial(self, serial_number):
        """
        Get an asset by its serial number
        
        Args:
            serial_number (str): Serial number of the asset to retrieve
        
        Returns:
            dict: Asset data if found, None otherwise
        """
        try:
            self.db.connect()
            
            self.db.cursor.execute("SELECT * FROM assets WHERE serial_number = ?", (serial_number,))
            asset = self.db.cursor.fetchone()
            
            if asset:
                # Convert sqlite3.Row to dict
                return dict(asset)
            return None
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.db.close()
    
    def get_all_assets(self, filters=None):
        """
        Get all assets with optional filtering
        
        Args:
            filters (dict, optional): Dictionary of field:value pairs to filter by
        
        Returns:
            list: List of asset dictionaries
        """
        try:
            self.db.connect()
            
            query = "SELECT * FROM assets"
            params = []
            
            # Apply filters if provided
            if filters:
                where_clauses = []
                for key, value in filters.items():
                    if value:  # Only add non-empty filters
                        where_clauses.append(f"{key} LIKE ?")
                        params.append(f"%{value}%")
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
            
            self.db.cursor.execute(query, params)
            assets = self.db.cursor.fetchall()
            
            # Convert sqlite3.Row objects to dictionaries
            return [dict(asset) for asset in assets]
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            self.db.close()
    
    def get_active_assets(self):
        """
        Get all active (issued) assets
        
        Returns:
            list: List of active asset dictionaries
        """
        return self.get_all_assets({'status': 'Active'})
    
    def get_stock_assets(self):
        """
        Get all stock (unassigned) assets
        
        Returns:
            list: List of stock asset dictionaries
        """
        return self.get_all_assets({'status': 'Stock'})
    
    def log_asset_action(self, asset_id, action, details, user_id):
        """
        Log an action performed on an asset
        
        Args:
            asset_id (int): ID of the asset
            action (str): Type of action performed
            details (str): Details of the action
            user_id (int): ID of the user who performed the action
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.db.connect()
            
            self.db.cursor.execute(
                "INSERT INTO asset_logs (asset_id, action, details, user_id) VALUES (?, ?, ?, ?)",
                (asset_id, action, details, user_id)
            )
            
            self.db.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            self.db.close()
