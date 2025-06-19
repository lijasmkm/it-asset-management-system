"""
User View for IT Asset Management System
Handles user management interface
"""
import tkinter as tk
from tkinter import ttk, messagebox

class UserView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the user view
        
        Args:
            parent: Parent widget
            controller: Main view controller
        """
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.user_controller = controller.user_controller
        
        # Create main layout
        self.create_layout()
        
        # Load users
        self.load_users()
    
    def create_layout(self):
        """Create the user view layout"""
        # Create header frame
        header_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        # Add title
        title_label = tk.Label(
            header_frame, 
            text="User Management", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)
        
        # Create toolbar frame
        toolbar_frame = tk.Frame(self, bg="#e0e0e0", padx=20, pady=10)
        toolbar_frame.pack(fill=tk.X)
        
        # Add buttons
        add_button = tk.Button(
            toolbar_frame,
            text="Add User",
            bg="#4CAF50",
            fg="white",
            command=self.show_add_user_dialog
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        edit_button = tk.Button(
            toolbar_frame,
            text="Edit User",
            command=self.show_edit_user_dialog
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = tk.Button(
            toolbar_frame,
            text="Delete User",
            bg="#f44336",
            fg="white",
            command=self.delete_user
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Create table frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview for users
        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "username", "role", "full_name", "email", "last_login"),
            show="headings"
        )
        
        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")
        self.tree.heading("full_name", text="Full Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("last_login", text="Last Login")
        
        # Define columns
        self.tree.column("id", width=50)
        self.tree.column("username", width=150)
        self.tree.column("role", width=150)
        self.tree.column("full_name", width=200)
        self.tree.column("email", width=200)
        self.tree.column("last_login", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add double-click event
        self.tree.bind("<Double-1>", lambda event: self.show_edit_user_dialog())
    
    def load_users(self):
        """Load users into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get users
        users = self.user_controller.get_all_users()
        
        # Add users to treeview
        for user in users:
            # Format last login
            last_login = user.get("last_login", "Never")
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    user.get("id"),
                    user.get("username"),
                    user.get("role", "").capitalize(),
                    user.get("full_name", ""),
                    user.get("email", ""),
                    last_login
                )
            )
    
    def show_add_user_dialog(self):
        """Show dialog to add a new user"""
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add User")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Add form elements
        form_frame = tk.Frame(dialog, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        tk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        username_var = tk.StringVar()
        username_entry = tk.Entry(form_frame, textvariable=username_var, width=30)
        username_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        # Password
        tk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        password_var = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=password_var, width=30, show="*")
        password_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # Confirm Password
        tk.Label(form_frame, text="Confirm Password:").grid(row=2, column=0, sticky="w", pady=5)
        confirm_password_var = tk.StringVar()
        confirm_password_entry = tk.Entry(form_frame, textvariable=confirm_password_var, width=30, show="*")
        confirm_password_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        # Full Name
        tk.Label(form_frame, text="Full Name:").grid(row=3, column=0, sticky="w", pady=5)
        full_name_var = tk.StringVar()
        full_name_entry = tk.Entry(form_frame, textvariable=full_name_var, width=30)
        full_name_entry.grid(row=3, column=1, sticky="w", pady=5)
        
        # Email
        tk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=5)
        email_var = tk.StringVar()
        email_entry = tk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=4, column=1, sticky="w", pady=5)
        
        # Role
        tk.Label(form_frame, text="Role:").grid(row=5, column=0, sticky="w", pady=5)
        role_var = tk.StringVar(value="standard")
        role_combo = ttk.Combobox(
            form_frame, 
            textvariable=role_var,
            values=["administrator", "standard", "document_controller", "view_only"],
            width=28,
            state="readonly"
        )
        role_combo.grid(row=5, column=1, sticky="w", pady=5)
        
        # Add buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        save_button = tk.Button(
            button_frame,
            text="Save",
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=lambda: self.add_user(
                username_var.get(),
                password_var.get(),
                confirm_password_var.get(),
                full_name_var.get(),
                email_var.get(),
                role_var.get(),
                dialog
            )
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            padx=10,
            pady=5,
            command=dialog.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Set focus to username entry
        username_entry.focus_set()
    
    def add_user(self, username, password, confirm_password, full_name, email, role, dialog):
        """
        Add a new user
        
        Args:
            username (str): Username
            password (str): Password
            confirm_password (str): Confirm password
            full_name (str): Full name
            email (str): Email
            role (str): Role
            dialog: Dialog window to close on success
        """
        # Validate input
        if not username or not password or not full_name:
            messagebox.showerror("Validation Error", "Username, password, and full name are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Validation Error", "Passwords do not match")
            return
        
        # Create user data
        user_data = {
            "username": username,
            "password": password,
            "full_name": full_name,
            "email": email,
            "role": role
        }
        
        # Add the user
        success, message = self.user_controller.add_user(user_data)
        
        if success:
            messagebox.showinfo("Success", message)
            dialog.destroy()
            self.load_users()
        else:
            messagebox.showerror("Error", message)
    
    def show_edit_user_dialog(self):
        """Show dialog to edit the selected user"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to edit")
            return
        
        # Get user ID
        user_id = self.tree.item(selected_item[0], "values")[0]
        
        # Get user data
        user = self.user_controller.get_user(user_id)
        if not user:
            messagebox.showerror("Error", "Failed to get user data")
            return
        
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Edit User")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Add form elements
        form_frame = tk.Frame(dialog, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        tk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        username_var = tk.StringVar(value=user.get("username", ""))
        username_entry = tk.Entry(form_frame, textvariable=username_var, width=30)
        username_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        # Password
        tk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        password_var = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=password_var, width=30, show="*")
        password_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # Confirm Password
        tk.Label(form_frame, text="Confirm Password:").grid(row=2, column=0, sticky="w", pady=5)
        confirm_password_var = tk.StringVar()
        confirm_password_entry = tk.Entry(form_frame, textvariable=confirm_password_var, width=30, show="*")
        confirm_password_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        # Password note
        password_note = tk.Label(
            form_frame, 
            text="Leave password blank to keep current password",
            font=("Arial", 8),
            fg="#999999"
        )
        password_note.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Full Name
        tk.Label(form_frame, text="Full Name:").grid(row=4, column=0, sticky="w", pady=5)
        full_name_var = tk.StringVar(value=user.get("full_name", ""))
        full_name_entry = tk.Entry(form_frame, textvariable=full_name_var, width=30)
        full_name_entry.grid(row=4, column=1, sticky="w", pady=5)
        
        # Email
        tk.Label(form_frame, text="Email:").grid(row=5, column=0, sticky="w", pady=5)
        email_var = tk.StringVar(value=user.get("email", ""))
        email_entry = tk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=5, column=1, sticky="w", pady=5)
        
        # Role
        tk.Label(form_frame, text="Role:").grid(row=6, column=0, sticky="w", pady=5)
        role_var = tk.StringVar(value=user.get("role", "standard"))
        role_combo = ttk.Combobox(
            form_frame, 
            textvariable=role_var,
            values=["administrator", "standard", "document_controller", "view_only"],
            width=28,
            state="readonly"
        )
        role_combo.grid(row=6, column=1, sticky="w", pady=5)
        
        # Add buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        save_button = tk.Button(
            button_frame,
            text="Save",
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=lambda: self.update_user(
                user_id,
                username_var.get(),
                password_var.get(),
                confirm_password_var.get(),
                full_name_var.get(),
                email_var.get(),
                role_var.get(),
                dialog
            )
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            padx=10,
            pady=5,
            command=dialog.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def update_user(self, user_id, username, password, confirm_password, full_name, email, role, dialog):
        """
        Update an existing user
        
        Args:
            user_id (int): User ID
            username (str): Username
            password (str): Password
            confirm_password (str): Confirm password
            full_name (str): Full name
            email (str): Email
            role (str): Role
            dialog: Dialog window to close on success
        """
        # Validate input
        if not username or not full_name:
            messagebox.showerror("Validation Error", "Username and full name are required")
            return
        
        if password and password != confirm_password:
            messagebox.showerror("Validation Error", "Passwords do not match")
            return
        
        # Create user data
        user_data = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "role": role
        }
        
        # Add password if provided
        if password:
            user_data["password"] = password
        
        # Update the user
        success, message = self.user_controller.update_user(user_id, user_data)
        
        if success:
            messagebox.showinfo("Success", message)
            dialog.destroy()
            self.load_users()
        else:
            messagebox.showerror("Error", message)
    
    def delete_user(self):
        """Delete the selected user"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to delete")
            return
        
        # Get user ID
        user_id = self.tree.item(selected_item[0], "values")[0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?"):
            # Delete the user
            success, message = self.user_controller.delete_user(user_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_users()
            else:
                messagebox.showerror("Error", message)
