"""
Backup View for IT Asset Management System
Handles database backup and restore interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

class BackupView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the backup view
        
        Args:
            parent: Parent widget
            controller: Main view controller
        """
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.backup_controller = controller.backup_controller
        
        # Create main layout
        self.create_layout()
        
        # Load backups
        self.load_backups()
    
    def create_layout(self):
        """Create the backup view layout"""
        # Create header frame
        header_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        # Add title
        title_label = tk.Label(
            header_frame, 
            text="Database Backup and Restore", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)
        
        # Create toolbar frame
        toolbar_frame = tk.Frame(self, bg="#e0e0e0", padx=20, pady=10)
        toolbar_frame.pack(fill=tk.X)
        
        # Add buttons
        create_button = tk.Button(
            toolbar_frame,
            text="Create Backup",
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.create_backup
        )
        create_button.pack(side=tk.LEFT, padx=5)
        
        restore_button = tk.Button(
            toolbar_frame,
            text="Restore Backup",
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=5,
            command=self.restore_backup
        )
        restore_button.pack(side=tk.LEFT, padx=5)
        
        refresh_button = tk.Button(
            toolbar_frame,
            text="Refresh",
            padx=10,
            pady=5,
            command=self.load_backups
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Create info frame
        info_frame = tk.LabelFrame(self, text="Backup Information", padx=20, pady=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Add info labels
        self.total_backups_var = tk.StringVar(value="Total Backups: 0")
        total_backups_label = tk.Label(
            info_frame,
            textvariable=self.total_backups_var,
            font=("Arial", 10),
            pady=5
        )
        total_backups_label.pack(side=tk.LEFT, padx=20)
        
        self.latest_backup_var = tk.StringVar(value="Latest Backup: None")
        latest_backup_label = tk.Label(
            info_frame,
            textvariable=self.latest_backup_var,
            font=("Arial", 10),
            pady=5
        )
        latest_backup_label.pack(side=tk.LEFT, padx=20)
        
        self.backup_status_var = tk.StringVar(value="Backup Status: Not scheduled")
        backup_status_label = tk.Label(
            info_frame,
            textvariable=self.backup_status_var,
            font=("Arial", 10),
            pady=5
        )
        backup_status_label.pack(side=tk.LEFT, padx=20)
        
        # Create table frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview for backups
        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "filename", "date", "size", "status"),
            show="headings"
        )
        
        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("filename", text="Filename")
        self.tree.heading("date", text="Date")
        self.tree.heading("size", text="Size")
        self.tree.heading("status", text="Status")
        
        # Define columns
        self.tree.column("id", width=50)
        self.tree.column("filename", width=300)
        self.tree.column("date", width=150)
        self.tree.column("size", width=100)
        self.tree.column("status", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add double-click event
        self.tree.bind("<Double-1>", lambda event: self.show_backup_details())
    
    def load_backups(self):
        """Load backups into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get backups
        backups = self.backup_controller.get_all_backups()
        
        # Update info labels
        self.total_backups_var.set(f"Total Backups: {len(backups)}")
        
        if backups:
            latest_backup = backups[0]  # Assuming backups are sorted by date
            latest_date = latest_backup.get("created_at", "Unknown")
            self.latest_backup_var.set(f"Latest Backup: {latest_date}")
        else:
            self.latest_backup_var.set("Latest Backup: None")
        
        # Check if backup is scheduled
        if self.backup_controller.is_scheduled:
            self.backup_status_var.set("Backup Status: Scheduled (Daily at 00:00)")
        else:
            self.backup_status_var.set("Backup Status: Not scheduled")
        
        # Add backups to treeview
        for backup in backups:
            # Format size
            size_bytes = backup.get("size", 0)
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.2f} KB"
            else:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    backup.get("id"),
                    backup.get("filename"),
                    backup.get("created_at"),
                    size_str,
                    backup.get("status", "")
                )
            )
    
    def create_backup(self):
        """Create a new backup"""
        # Confirm backup creation
        if messagebox.askyesno("Create Backup", "Are you sure you want to create a new backup?"):
            # Create the backup
            success, message = self.backup_controller.create_backup()
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_backups()
            else:
                messagebox.showerror("Error", message)
    
    def restore_backup(self):
        """Restore from the selected backup"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a backup to restore")
            return
        
        # Get backup ID
        backup_id = self.tree.item(selected_item[0], "values")[0]
        
        # Confirm restoration
        if messagebox.askyesno(
            "Confirm Restore", 
            "Are you sure you want to restore from this backup?\n\nWARNING: This will overwrite the current database. All changes made since this backup will be lost."
        ):
            # Restore the backup
            success, message = self.backup_controller.restore_backup(backup_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_backups()
            else:
                messagebox.showerror("Error", message)
    
    def show_backup_details(self):
        """Show details of the selected backup"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Get backup ID and filename
        backup_id = self.tree.item(selected_item[0], "values")[0]
        filename = self.tree.item(selected_item[0], "values")[1]
        date = self.tree.item(selected_item[0], "values")[2]
        size = self.tree.item(selected_item[0], "values")[3]
        status = self.tree.item(selected_item[0], "values")[4]
        
        # Show details
        messagebox.showinfo(
            "Backup Details",
            f"ID: {backup_id}\nFilename: {filename}\nDate: {date}\nSize: {size}\nStatus: {status}"
        )
