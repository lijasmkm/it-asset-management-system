"""
IT Asset Management System
Main application entry point
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from src.config.database import db_config
from src.views.login_view import LoginView
from src.views.main_view import MainView
from src.controllers.user_controller import UserController
from src.controllers.backup_controller import BackupController

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize the database
        self.initialize_database()
        
        # Set up the application window
        self.title("IT Asset Management System")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Set application icon if available
        try:
            self.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Initialize user session
        self.current_user = None
        
        # Set up controllers
        self.user_controller = UserController()
        self.backup_controller = BackupController()
        
        # Set up the container frame
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Show login view
        self.show_login()
        
        # Schedule daily backup
        self.schedule_backup()
    
    def initialize_database(self):
        """Initialize the database"""
        if not db_config.initialize_database():
            messagebox.showerror("Database Error", "Failed to initialize the database. The application will now exit.")
            sys.exit(1)
    
    def show_login(self):
        """Show the login view"""
        login_frame = LoginView(self.container, self)
        self.frames["login"] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")
        login_frame.tkraise()
    
    def show_main(self):
        """Show the main application view"""
        main_frame = MainView(self.container, self)
        self.frames["main"] = main_frame
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.tkraise()
    
    def login(self, username, password):
        """
        Authenticate user and show main view if successful
        
        Args:
            username (str): Username
            password (str): Password
        
        Returns:
            bool: True if login successful, False otherwise
        """
        user = self.user_controller.login(username, password)
        
        if user:
            self.current_user = user
            self.user_controller.current_user = user
            self.backup_controller.current_user = user
            
            # Show main view
            self.show_main()
            return True
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return False
    
    def logout(self):
        """Log out the current user and show login view"""
        self.current_user = None
        self.user_controller.current_user = None
        self.backup_controller.current_user = None
        
        # Show login view
        self.show_login()
    
    def schedule_backup(self):
        """Schedule daily backup at midnight"""
        self.backup_controller.schedule_daily_backup("00:00")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
