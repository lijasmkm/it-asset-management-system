"""
User Controller for IT Asset Management System
Handles business logic for user operations and authentication
"""
from src.models.user_model import UserModel

class UserController:
    def __init__(self, current_user=None):
        """
        Initialize the user controller
        
        Args:
            current_user (dict, optional): The currently logged in user
        """
        self.user_model = UserModel()
        self.current_user = current_user
    
    def login(self, username, password):
        """
        Authenticate a user
        
        Args:
            username (str): Username
            password (str): Password
        
        Returns:
            dict: User data if authentication successful, None otherwise
        """
        return self.user_model.authenticate(username, password)
    
    def add_user(self, user_data):
        """
        Add a new user
        
        Args:
            user_data (dict): User data to add
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Validate required fields
        required_fields = ['username', 'password', 'role', 'full_name']
        for field in required_fields:
            if not user_data.get(field):
                return False, f"Missing required field: {field}"
        
        # Validate role
        valid_roles = ['administrator', 'standard', 'document_controller', 'view_only']
        if user_data.get('role') not in valid_roles:
            return False, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        
        # Check if current user has permission to add users
        if self.current_user and self.current_user.get('role') != 'administrator':
            return False, "You don't have permission to add users"
        
        # Add the user
        return self.user_model.add_user(user_data)
    
    def update_user(self, user_id, user_data):
        """
        Update an existing user
        
        Args:
            user_id (int): ID of the user to update
            user_data (dict): Updated user data
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if the user exists
        existing_user = self.user_model.get_user_by_id(user_id)
        if not existing_user:
            return False, "User not found"
        
        # Check if current user has permission to update users
        if self.current_user:
            # Users can update their own profile
            if self.current_user.get('id') != user_id and self.current_user.get('role') != 'administrator':
                return False, "You don't have permission to update other users"
            
            # Only admins can change roles
            if 'role' in user_data and self.current_user.get('role') != 'administrator':
                return False, "Only administrators can change user roles"
        
        # Update the user
        return self.user_model.update_user(user_id, user_data)
    
    def delete_user(self, user_id):
        """
        Delete a user
        
        Args:
            user_id (int): ID of the user to delete
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if the user exists
        existing_user = self.user_model.get_user_by_id(user_id)
        if not existing_user:
            return False, "User not found"
        
        # Check if current user has permission to delete users
        if self.current_user:
            if self.current_user.get('role') != 'administrator':
                return False, "Only administrators can delete users"
            
            # Prevent deleting yourself
            if self.current_user.get('id') == user_id:
                return False, "You cannot delete your own account"
        
        # Delete the user
        return self.user_model.delete_user(user_id)
    
    def get_user(self, user_id):
        """
        Get a user by ID
        
        Args:
            user_id (int): ID of the user to retrieve
        
        Returns:
            dict: User data if found, None otherwise
        """
        return self.user_model.get_user_by_id(user_id)
    
    def get_all_users(self):
        """
        Get all users
        
        Returns:
            list: List of users
        """
        # Check if current user has permission to view all users
        if self.current_user and self.current_user.get('role') not in ['administrator', 'standard']:
            return []
        
        return self.user_model.get_all_users()
    
    def check_permission(self, user_id, required_role):
        """
        Check if a user has the required role
        
        Args:
            user_id (int): ID of the user
            required_role (str or list): Required role(s)
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        return self.user_model.check_permission(user_id, required_role)
    
    def change_password(self, user_id, current_password, new_password):
        """
        Change a user's password
        
        Args:
            user_id (int): ID of the user
            current_password (str): Current password
            new_password (str): New password
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        # Check if the user exists
        user = self.user_model.get_user_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Check if current user has permission to change this password
        if self.current_user:
            # Users can change their own password
            if self.current_user.get('id') != user_id and self.current_user.get('role') != 'administrator':
                return False, "You don't have permission to change other users' passwords"
        
        # Verify current password (except for administrators)
        if self.current_user and self.current_user.get('role') != 'administrator':
            if not self.user_model.authenticate(user.get('username'), current_password):
                return False, "Current password is incorrect"
        
        # Update the password
        return self.user_model.update_user(user_id, {'password': new_password})
