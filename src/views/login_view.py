"""
Login View for IT Asset Management System
Handles user authentication interface
"""
import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the login view
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # Create a frame for the login form
        login_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Add a title
        title_label = tk.Label(
            login_frame, 
            text="IT Asset Management System", 
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#333333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Add login form elements
        username_label = tk.Label(
            login_frame, 
            text="Username:", 
            font=("Arial", 12),
            bg="white",
            fg="#333333"
        )
        username_label.grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        self.username_entry = tk.Entry(
            login_frame, 
            font=("Arial", 12),
            width=25
        )
        self.username_entry.grid(row=1, column=1, sticky="w", pady=(0, 10))
        
        password_label = tk.Label(
            login_frame, 
            text="Password:", 
            font=("Arial", 12),
            bg="white",
            fg="#333333"
        )
        password_label.grid(row=2, column=0, sticky="w", pady=(0, 20))
        
        self.password_entry = tk.Entry(
            login_frame, 
            font=("Arial", 12),
            width=25,
            show="*"
        )
        self.password_entry.grid(row=2, column=1, sticky="w", pady=(0, 20))
        
        # Add login button
        login_button = tk.Button(
            login_frame,
            text="Login",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.login
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Add version information
        version_label = tk.Label(
            login_frame,
            text="Version 1.0",
            font=("Arial", 8),
            bg="white",
            fg="#999999"
        )
        version_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Set focus to username entry
        self.username_entry.focus()
    
    def login(self):
        """Handle login button click"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password")
            return
        
        # Attempt to login
        self.controller.login(username, password)
