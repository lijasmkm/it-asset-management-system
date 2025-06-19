"""
User Model for IT Asset Management System
Handles all database operations related to users and authentication
"""
import sqlite3
import hashlib
from datetime import datetime
from src.config.database import db_config

class UserModel:
    def __init__(self):
        """Initialize the user model"""
        self.db = db_config
    
    def _hash_password(self, password):
        """
        Hash a password for secure storage
        
        Args:
            password (str): Plain text password
        
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """
        Authenticate a user
        
        Args:
            username (str): Username
            password (str): Plain text password
        
        Returns:
            dict: User data if authentication successful, None otherwise
        """
        try:
            self.db.connect()
            
            hashed_password = self._hash_password(password)
            
            self.db.cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, hashed_password)
            )
            
            user = self.db.cursor.fetchone()
            
            if user:
                # Update last login time
                self.db.cursor.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user['id'])
                )
                self.db.commit()
                
                # Convert sqlite3.Row to dict
                return dict(user)
            
            return None
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.db.close()
    
    def add_user(self, user_data):
        """
        Add a new user to the database
        
        Args:
            user_data (dict): Dictionary containing user data
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            self.db.connect()
            
            # Check if username already exists
            self.db.cursor.execute("SELECT id FROM users WHERE username = ?", 
                                (user_data.get('username'),))
            if self.db.cursor.fetchone():
                return False, "Username already exists"
            
            # Hash the password
            if 'password' in user_data:
                user_data['password'] = self._hash_password(user_data['password'])
            
            # Prepare fields and values for insertion
            fields = []
            values = []
            placeholders = []
            
            for key, value in user_data.items():
                if key != 'id':  # Skip id for new users
                    fields.append(key)
                    values.append(value)
                    placeholders.append('?')
            
            # Add created_at timestamp
            fields.append('created_at')
            values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            placeholders.append('?')
            
            # Build and execute the query
            query = f"INSERT INTO users ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            self.db.cursor.execute(query, values)
            
            user_id = self.db.cursor.lastrowid
            self.db.commit()
            
            return True, f"User added successfully with ID: {user_id}"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            self.db.close()
    
    def update_user(self, user_id, user_data):
        """
        Update an existing user
        
        Args:
            user_id (int): ID of the user to update
            user_data (dict): Dictionary containing updated user data
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            self.db.connect()
            
            # Check if user exists
            self.db.cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not self.db.cursor.fetchone():
                return False, "User not found"
            
            # Check if updating to a username that already exists
            if 'username' in user_data:
                self.db.cursor.execute(
                    "SELECT id FROM users WHERE username = ? AND id != ?", 
                    (user_data['username'], user_id)
                )
                if self.db.cursor.fetchone():
                    return False, "Username already taken"
            
            # Hash the password if it's being updated
            if 'password' in user_data:
                user_data['password'] = self._hash_password(user_data['password'])
            
            # Prepare fields and values for update
            set_clause = []
            values = []
            
            for key, value in user_data.items():
                if key != 'id':  # Skip id for updates
                    set_clause.append(f"{key} = ?")
                    values.append(value)
            
            # Add user_id to values
            values.append(user_id)
            
            # Build and execute the query
            query = f"UPDATE users SET {', '.join(set_clause)} WHERE id = ?"
            self.db.cursor.execute(query, values)
            
            if self.db.cursor.rowcount == 0:
                return False, "No changes made to the user"
                
            self.db.commit()
            return True, "User updated successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            self.db.close()
    
    def delete_user(self, user_id):
        """
        Delete a user from the database
        
        Args:
            user_id (int): ID of the user to delete
        
        Returns:
            bool: True if successful, False otherwise
            str: Message indicating success or error
        """
        try:
            self.db.connect()
            
            # Check if user exists
            self.db.cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not self.db.cursor.fetchone():
                return False, "User not found"
            
            # Delete the user
            self.db.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.db.commit()
            
            return True, "User deleted successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            self.db.close()
    
    def get_user_by_id(self, user_id):
        """
        Get a user by their ID
        
        Args:
            user_id (int): ID of the user to retrieve
        
        Returns:
            dict: User data if found, None otherwise
        """
        try:
            self.db.connect()
            
            self.db.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = self.db.cursor.fetchone()
            
            if user:
                # Convert sqlite3.Row to dict
                return dict(user)
            return None
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.db.close()
    
    def get_all_users(self):
        """
        Get all users from the database
        
        Returns:
            list: List of user dictionaries
        """
        try:
            self.db.connect()
            
            self.db.cursor.execute("SELECT id, username, role, email, full_name, created_at, last_login FROM users")
            users = self.db.cursor.fetchall()
            
            # Convert sqlite3.Row objects to dictionaries
            return [dict(user) for user in users]
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            self.db.close()
    
    def check_permission(self, user_id, required_role):
        """
        Check if a user has the required role
        
        Args:
            user_id (int): ID of the user
            required_role (str or list): Required role(s)
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        try:
            self.db.connect()
            
            self.db.cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            user = self.db.cursor.fetchone()
            
            if not user:
                return False
            
            # Convert required_role to list if it's a string
            if isinstance(required_role, str):
                required_role = [required_role]
            
            # Check if user's role is in the required roles
            return user['role'] in required_role
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            self.db.close()
