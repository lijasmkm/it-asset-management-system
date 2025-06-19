"""
Main View for IT Asset Management System
Central interface after login
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.views.asset_view import AssetView
from src.views.report_view import ReportView
from src.views.user_view import UserView
from src.views.backup_view import BackupView
from src.controllers.asset_controller import AssetController
from src.controllers.report_controller import ReportController
from src.controllers.user_controller import UserController
from src.controllers.backup_controller import BackupController

class MainView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the main view
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent)
        self.controller = controller
        
        # Initialize controllers with current user
        self.asset_controller = AssetController(self.controller.current_user)
        self.report_controller = ReportController(self.controller.current_user)
        self.user_controller = UserController(self.controller.current_user)
        self.backup_controller = BackupController(self.controller.current_user)
        
        # Create main layout
        self.create_layout()
        
        # Show default view (asset view)
        self.show_frame("asset")
    
    def create_layout(self):
        """Create the main application layout"""
        # Create sidebar
        self.sidebar = tk.Frame(self, bg="#333333", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)  # Prevent sidebar from shrinking
        
        # Add logo or title
        logo_frame = tk.Frame(self.sidebar, bg="#333333", height=100)
        logo_frame.pack(fill=tk.X)
        logo_label = tk.Label(
            logo_frame, 
            text="IT Asset\nManagement", 
            font=("Arial", 14, "bold"),
            bg="#333333",
            fg="white",
            pady=20
        )
        logo_label.pack()
        
        # Add user info
        user_frame = tk.Frame(self.sidebar, bg="#333333", height=50)
        user_frame.pack(fill=tk.X)
        user_label = tk.Label(
            user_frame, 
            text=f"User: {self.controller.current_user.get('username')}", 
            font=("Arial", 10),
            bg="#333333",
            fg="#cccccc",
            anchor="w",
            padx=10
        )
        user_label.pack(fill=tk.X)
        role_label = tk.Label(
            user_frame, 
            text=f"Role: {self.controller.current_user.get('role').capitalize()}", 
            font=("Arial", 10),
            bg="#333333",
            fg="#cccccc",
            anchor="w",
            padx=10
        )
        role_label.pack(fill=tk.X)
        
        # Add navigation buttons
        nav_frame = tk.Frame(self.sidebar, bg="#333333")
        nav_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Asset button
        self.asset_button = tk.Button(
            nav_frame,
            text="Assets",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            bd=0,
            padx=10,
            pady=8,
            width=15,
            command=lambda: self.show_frame("asset")
        )
        self.asset_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Reports button
        self.report_button = tk.Button(
            nav_frame,
            text="Reports",
            font=("Arial", 12),
            bg="#555555",
            fg="white",
            bd=0,
            padx=10,
            pady=8,
            width=15,
            command=lambda: self.show_frame("report")
        )
        self.report_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Users button (only for administrators)
        if self.controller.current_user.get('role') == 'administrator':
            self.user_button = tk.Button(
                nav_frame,
                text="Users",
                font=("Arial", 12),
                bg="#555555",
                fg="white",
                bd=0,
                padx=10,
                pady=8,
                width=15,
                command=lambda: self.show_frame("user")
            )
            self.user_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Backup button (only for administrators)
        if self.controller.current_user.get('role') == 'administrator':
            self.backup_button = tk.Button(
                nav_frame,
                text="Backups",
                font=("Arial", 12),
                bg="#555555",
                fg="white",
                bd=0,
                padx=10,
                pady=8,
                width=15,
                command=lambda: self.show_frame("backup")
            )
            self.backup_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Logout button
        self.logout_button = tk.Button(
            self.sidebar,
            text="Logout",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            bd=0,
            padx=10,
            pady=8,
            width=15,
            command=self.logout
        )
        self.logout_button.pack(side=tk.BOTTOM, padx=10, pady=20)
        
        # Create content frame
        self.content_frame = tk.Frame(self, bg="#f0f0f0")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Create frames for each view
        self.frames["asset"] = AssetView(self.content_frame, self)
        self.frames["report"] = ReportView(self.content_frame, self)
        
        if self.controller.current_user.get('role') == 'administrator':
            self.frames["user"] = UserView(self.content_frame, self)
            self.frames["backup"] = BackupView(self.content_frame, self)
    
    def show_frame(self, frame_name):
        """
        Show the specified frame
        
        Args:
            frame_name (str): Name of the frame to show
        """
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Reset all button colors
        self.asset_button.config(bg="#555555")
        self.report_button.config(bg="#555555")
        
        if hasattr(self, 'user_button'):
            self.user_button.config(bg="#555555")
        
        if hasattr(self, 'backup_button'):
            self.backup_button.config(bg="#555555")
        
        # Show the selected frame
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)
        
        # Highlight the selected button
        if frame_name == "asset":
            self.asset_button.config(bg="#4CAF50")
        elif frame_name == "report":
            self.report_button.config(bg="#4CAF50")
        elif frame_name == "user" and hasattr(self, 'user_button'):
            self.user_button.config(bg="#4CAF50")
        elif frame_name == "backup" and hasattr(self, 'backup_button'):
            self.backup_button.config(bg="#4CAF50")
    
    def logout(self):
        """Handle logout button click"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.controller.logout()
