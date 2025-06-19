"""
Report View for IT Asset Management System
Handles report generation interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

class ReportView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the report view
        
        Args:
            parent: Parent widget
            controller: Main view controller
        """
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.report_controller = controller.report_controller
        
        # Create main layout
        self.create_layout()
    
    def create_layout(self):
        """Create the report view layout"""
        # Create header frame
        header_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        # Add title
        title_label = tk.Label(
            header_frame, 
            text="Report Generation", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)
        
        # Create content frame
        content_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add report options
        options_frame = tk.LabelFrame(content_frame, text="Report Options", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Report type selection
        tk.Label(options_frame, text="Report Type:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.report_type_var = tk.StringVar(value="asset_list")
        report_type_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.report_type_var,
            values=[
                "asset_list", 
                "depreciation", 
                "ageing", 
                "lifecycle", 
                "warranty", 
                "maintenance"
            ],
            width=20,
            state="readonly"
        )
        report_type_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Export format selection
        tk.Label(options_frame, text="Export Format:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.export_format_var = tk.StringVar(value="csv")
        export_format_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.export_format_var,
            values=["csv", "pdf"],
            width=10,
            state="readonly"
        )
        export_format_combo.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Add filter frame
        filter_frame = tk.LabelFrame(content_frame, text="Filters", padx=10, pady=10)
        filter_frame.pack(fill=tk.X, pady=10)
        
        # Company filter
        tk.Label(filter_frame, text="Company:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.company_var = tk.StringVar()
        ttk.Combobox(
            filter_frame, 
            textvariable=self.company_var,
            values=["", "Meraki", "MICL", "SALES", "EDUCATION", "Steel"],
            width=15
        ).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Location filter
        tk.Label(filter_frame, text="Location:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.location_var = tk.StringVar()
        ttk.Combobox(
            filter_frame, 
            textvariable=self.location_var,
            values=["", "SS7", "SS16", "Majan"],
            width=15
        ).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Category filter
        tk.Label(filter_frame, text="Category:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.category_var = tk.StringVar()
        ttk.Combobox(
            filter_frame, 
            textvariable=self.category_var,
            values=["", "Laptop", "Desktop", "Server", "Printer", "Network", "Mobile", "Other"],
            width=15
        ).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Status filter
        tk.Label(filter_frame, text="Status:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.status_var = tk.StringVar()
        ttk.Combobox(
            filter_frame, 
            textvariable=self.status_var,
            values=["", "Active", "Stock", "Attention"],
            width=15
        ).grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        # Date range filters
        date_frame = tk.Frame(filter_frame)
        date_frame.grid(row=2, column=0, columnspan=4, sticky="w", padx=5, pady=5)
        
        tk.Label(date_frame, text="Date Range:").pack(side=tk.LEFT, padx=5)
        
        tk.Label(date_frame, text="From:").pack(side=tk.LEFT, padx=5)
        self.from_date_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.from_date_var, width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Label(date_frame, text="To:").pack(side=tk.LEFT, padx=5)
        self.to_date_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.to_date_var, width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Label(date_frame, text="(YYYY-MM-DD)").pack(side=tk.LEFT, padx=5)
        
        # Add buttons
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        generate_button = tk.Button(
            button_frame,
            text="Generate Report",
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.generate_report
        )
        generate_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Clear Filters",
            padx=10,
            pady=5,
            command=self.clear_filters
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Add report history frame
        history_frame = tk.LabelFrame(content_frame, text="Recent Reports", padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview for report history
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=("id", "report_type", "date", "format", "file"),
            show="headings"
        )
        
        # Define headings
        self.history_tree.heading("id", text="ID")
        self.history_tree.heading("report_type", text="Report Type")
        self.history_tree.heading("date", text="Date Generated")
        self.history_tree.heading("format", text="Format")
        self.history_tree.heading("file", text="File")
        
        # Define columns
        self.history_tree.column("id", width=50)
        self.history_tree.column("report_type", width=150)
        self.history_tree.column("date", width=150)
        self.history_tree.column("format", width=100)
        self.history_tree.column("file", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add double-click event to open report
        self.history_tree.bind("<Double-1>", self.open_report)
        
        # Populate with sample data (would be replaced with actual data)
        self.load_report_history()
    
    def generate_report(self):
        """Generate a report based on selected options"""
        # Get report type and export format
        report_type = self.report_type_var.get()
        export_format = self.export_format_var.get()
        
        # Build filters dictionary
        filters = {}
        
        if self.company_var.get():
            filters["company"] = self.company_var.get()
        
        if self.location_var.get():
            filters["location"] = self.location_var.get()
        
        if self.category_var.get():
            filters["category"] = self.category_var.get()
        
        if self.status_var.get():
            filters["status"] = self.status_var.get()
        
        # Generate the report
        report_path, report_data = self.report_controller.generate_report(
            report_type, 
            filters, 
            export_format
        )
        
        if report_path and os.path.exists(report_path):
            messagebox.showinfo(
                "Report Generated", 
                f"Report has been generated successfully.\nFile: {report_path}"
            )
            
            # Reload report history
            self.load_report_history()
        else:
            messagebox.showerror(
                "Report Generation Failed", 
                "Failed to generate the report. Please check your filters and try again."
            )
    
    def clear_filters(self):
        """Clear all filters"""
        self.company_var.set("")
        self.location_var.set("")
        self.category_var.set("")
        self.status_var.set("")
        self.from_date_var.set("")
        self.to_date_var.set("")
    
    def load_report_history(self):
        """Load report history into the treeview"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get report directory
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports')
        
        # Check if directory exists
        if not os.path.exists(reports_dir):
            return
        
        # Get report files
        report_files = os.listdir(reports_dir)
        
        # Add report files to treeview
        for i, filename in enumerate(report_files):
            if filename.endswith('.csv') or filename.endswith('.pdf'):
                # Parse report type from filename
                parts = filename.split('_')
                if len(parts) >= 2:
                    report_type = parts[0]
                    
                    # Parse date from filename
                    date_parts = parts[-1].split('.')
                    if len(date_parts) >= 2:
                        date_str = date_parts[0]
                        
                        # Format date
                        try:
                            year = date_str[:4]
                            month = date_str[4:6]
                            day = date_str[6:8]
                            time = date_str[9:].replace('_', ':')
                            formatted_date = f"{year}-{month}-{day} {time}"
                        except:
                            formatted_date = date_str
                        
                        # Get file format
                        file_format = filename.split('.')[-1].upper()
                        
                        # Add to treeview
                        self.history_tree.insert(
                            "",
                            tk.END,
                            values=(
                                i + 1,
                                report_type,
                                formatted_date,
                                file_format,
                                filename
                            )
                        )
    
    def open_report(self, event):
        """Open the selected report"""
        # Get selected item
        selected_item = self.history_tree.selection()
        if not selected_item:
            return
        
        # Get filename
        filename = self.history_tree.item(selected_item[0], "values")[4]
        
        # Get full path
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports')
        file_path = os.path.join(reports_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            messagebox.showerror("File Not Found", f"The file {filename} could not be found.")
            return
        
        # Open the file with default application
        try:
            os.startfile(file_path)
        except:
            messagebox.showerror("Error", f"Failed to open the file {filename}.")
