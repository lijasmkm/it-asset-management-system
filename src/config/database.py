"""
Database configuration for IT Asset Management System
Handles database connection and initialization
"""
import os
import sqlite3
from datetime import datetime

class DatabaseConfig:
    def __init__(self, db_path="assets.db"):
        """Initialize database configuration with path to database file"""
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), db_path)
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable row factory for named columns
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
    
    def commit(self):
        """Commit changes to the database"""
        if self.connection:
            self.connection.commit()
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        if not self.connect():
            return False
        
        try:
            # Create users table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
            ''')
            
            # Create assets table with all required fields from the specification
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT UNIQUE NOT NULL,
                company TEXT,
                location TEXT,
                category TEXT NOT NULL,
                status TEXT,
                username TEXT,
                designation TEXT,
                department TEXT,
                model TEXT,
                description TEXT,
                issue_date DATE,
                computer_id TEXT,
                working_status TEXT,
                condition TEXT,
                audit TEXT,
                employee_id TEXT,
                purchase_date DATE,
                rack_tray_number TEXT,
                service_center TEXT,
                lpo_number TEXT,
                invoice_number TEXT,
                supplier TEXT,
                estimated_cost REAL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create asset_logs table for history and audits
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS asset_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                user_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (asset_id) REFERENCES assets (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')
            
            # Create backups table to track backup history
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                path TEXT NOT NULL,
                size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT
            )
            ''')
            
            # Insert default admin user if not exists
            # Hash the default password using SHA-256
            import hashlib
            default_password = 'admin123'
            hashed_password = hashlib.sha256(default_password.encode()).hexdigest()
            
            self.cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, role, email, full_name)
            VALUES (?, ?, ?, ?, ?)
            ''', ('admin', hashed_password, 'administrator', 'admin@example.com', 'System Administrator'))
            
            self.commit()
            print("Database initialized successfully")
            return True
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            return False
        finally:
            self.close()

# Create an instance for direct usage
db_config = DatabaseConfig()

if __name__ == "__main__":
    # If this script is run directly, initialize the database
    db_config.initialize_database()
