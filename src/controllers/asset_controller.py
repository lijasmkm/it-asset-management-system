"""
Asset Controller for IT Asset Management System
Handles business logic for asset operations
"""
from src.models.asset_model import AssetModel

class AssetController:
    def __init__(self, current_user=None):
        """
        Initialize the asset controller
        
        Args:
            current_user (dict, optional): The currently logged in user
        """
        self.asset_model = AssetModel()
        self.current_user = current_user
    
    def add_asset(self, asset_data):
        """
        Add a new asset
        
        Args:
            asset_data (dict): Asset data to add
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Validate required fields
        required_fields = ['serial_number', 'category']
        for field in required_fields:
            if not asset_data.get(field):
                return False, f"Missing required field: {field}"
        
        # Add the asset
        success, message = self.asset_model.add_asset(asset_data)
        
        # Log the action if successful
        if success and self.current_user:
            asset_id = int(message.split(':')[-1].strip())
            self.asset_model.log_asset_action(
                asset_id, 
                'create', 
                f"Asset created by {self.current_user.get('username')}", 
                self.current_user.get('id')
            )
        
        return success, message
    
    def update_asset(self, asset_id, asset_data):
        """
        Update an existing asset
        
        Args:
            asset_id (int): ID of the asset to update
            asset_data (dict): Updated asset data
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if the asset exists
        existing_asset = self.asset_model.get_asset_by_id(asset_id)
        if not existing_asset:
            return False, "Asset not found"
        
        # Update the asset
        success, message = self.asset_model.update_asset(asset_id, asset_data)
        
        # Log the action if successful
        if success and self.current_user:
            self.asset_model.log_asset_action(
                asset_id, 
                'update', 
                f"Asset updated by {self.current_user.get('username')}", 
                self.current_user.get('id')
            )
        
        return success, message
    
    def delete_asset(self, asset_id):
        """
        Delete an asset
        
        Args:
            asset_id (int): ID of the asset to delete
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if the asset exists
        existing_asset = self.asset_model.get_asset_by_id(asset_id)
        if not existing_asset:
            return False, "Asset not found"
        
        # Check if user has permission to delete
        if self.current_user and self.current_user.get('role') != 'administrator':
            return False, "You don't have permission to delete assets"
        
        # Log the action before deleting
        if self.current_user:
            self.asset_model.log_asset_action(
                asset_id, 
                'delete', 
                f"Asset deleted by {self.current_user.get('username')}", 
                self.current_user.get('id')
            )
        
        # Delete the asset
        return self.asset_model.delete_asset(asset_id)
    
    def get_asset(self, asset_id):
        """
        Get an asset by ID
        
        Args:
            asset_id (int): ID of the asset to retrieve
        
        Returns:
            dict: Asset data if found, None otherwise
        """
        return self.asset_model.get_asset_by_id(asset_id)
    
    def get_asset_by_serial(self, serial_number):
        """
        Get an asset by serial number
        
        Args:
            serial_number (str): Serial number of the asset
        
        Returns:
            dict: Asset data if found, None otherwise
        """
        return self.asset_model.get_asset_by_serial(serial_number)
    
    def search_assets(self, filters=None):
        """
        Search for assets with filters
        
        Args:
            filters (dict, optional): Search filters
        
        Returns:
            list: List of matching assets
        """
        return self.asset_model.get_all_assets(filters)
    
    def get_active_assets(self):
        """
        Get all active (issued) assets
        
        Returns:
            list: List of active assets
        """
        return self.asset_model.get_active_assets()
    
    def get_stock_assets(self):
        """
        Get all stock (unassigned) assets
        
        Returns:
            list: List of stock assets
        """
        return self.asset_model.get_stock_assets()
    
    def move_to_active(self, asset_id, user_data):
        """
        Move an asset from stock to active (issue to a user)
        
        Args:
            asset_id (int): ID of the asset to move
            user_data (dict): User data to assign the asset to
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if the asset exists
        asset = self.asset_model.get_asset_by_id(asset_id)
        if not asset:
            return False, "Asset not found"
        
        # Check if the asset is in stock
        if asset.get('status') != 'Stock':
            return False, "Asset is not in stock"
        
        # Update asset data
        update_data = {
            'status': 'Active',
            'username': user_data.get('username'),
            'department': user_data.get('department'),
            'designation': user_data.get('designation'),
            'employee_id': user_data.get('employee_id'),
            'issue_date': user_data.get('issue_date')
        }
        
        # Update the asset
        success, message = self.asset_model.update_asset(asset_id, update_data)
        
        # Log the action if successful
        if success and self.current_user:
            self.asset_model.log_asset_action(
                asset_id, 
                'move_to_active', 
                f"Asset issued to {user_data.get('username')} by {self.current_user.get('username')}", 
                self.current_user.get('id')
            )
        
        return success, message
    
    def move_to_stock(self, asset_id, reason=None):
        """
        Move an asset from active to stock (return from a user)
        
        Args:
            asset_id (int): ID of the asset to move
            reason (str, optional): Reason for returning to stock
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if the asset exists
        asset = self.asset_model.get_asset_by_id(asset_id)
        if not asset:
            return False, "Asset not found"
        
        # Check if the asset is active
        if asset.get('status') != 'Active':
            return False, "Asset is not active"
        
        # Update asset data
        update_data = {
            'status': 'Stock',
            'username': None,
            'department': None,
            'designation': None,
            'employee_id': None
        }
        
        if reason:
            update_data['remarks'] = reason
        
        # Update the asset
        success, message = self.asset_model.update_asset(asset_id, update_data)
        
        # Log the action if successful
        if success and self.current_user:
            self.asset_model.log_asset_action(
                asset_id, 
                'move_to_stock', 
                f"Asset returned to stock by {self.current_user.get('username')}. Reason: {reason or 'Not specified'}", 
                self.current_user.get('id')
            )
        
        return success, message
    
    def get_asset_history(self, asset_id):
        """
        Get the history of an asset
        
        Args:
            asset_id (int): ID of the asset
        
        Returns:
            list: List of asset history records
        """
        # Check if the asset exists
        asset = self.asset_model.get_asset_by_id(asset_id)
        if not asset:
            return []
        
        # Get the asset logs
        try:
            self.asset_model.db.connect()
            
            query = """
                SELECT al.*, u.username 
                FROM asset_logs al
                LEFT JOIN users u ON al.user_id = u.id
                WHERE al.asset_id = ?
                ORDER BY al.timestamp DESC
            """
            
            self.asset_model.db.cursor.execute(query, (asset_id,))
            logs = self.asset_model.db.cursor.fetchall()
            
            # Convert sqlite3.Row objects to dictionaries
            return [dict(log) for log in logs]
            
        except Exception as e:
            print(f"Error getting asset history: {e}")
            return []
        finally:
            self.asset_model.db.close()
