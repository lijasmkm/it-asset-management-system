"""
Asset View for IT Asset Management System
Handles asset management interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from src.utils.excel_utils import ExcelUtils

class AssetView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the asset view
        
        Args:
            parent: Parent widget
            controller: Main view controller
        """
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.asset_controller = controller.asset_controller
        
        # Initialize Excel utilities
        self.excel_utils = ExcelUtils(self.asset_controller)
        
        # Initialize sliding panel variables
        self.sliding_panel = None
        self.panel_visible = False
        self.animation_running = False
        
        # Create main layout
        self.create_layout()
        
        # Load assets
        self.load_assets()
    
    def create_layout(self):
        """Create the asset view layout"""
        # Create main container with relative positioning for overlay
        self.main_container = tk.Frame(self, bg="#f0f0f0")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header frame
        header_frame = tk.Frame(self.main_container, bg="#f0f0f0", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        # Add title
        title_label = tk.Label(
            header_frame, 
            text="Asset Management", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)
        
        # Add asset type selector
        self.asset_type_var = tk.StringVar(value="all")
        asset_type_frame = tk.Frame(header_frame, bg="#f0f0f0")
        asset_type_frame.pack(side=tk.RIGHT)
        
        tk.Radiobutton(
            asset_type_frame,
            text="All Assets",
            variable=self.asset_type_var,
            value="all",
            bg="#f0f0f0",
            command=self.load_assets
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            asset_type_frame,
            text="Active Assets",
            variable=self.asset_type_var,
            value="active",
            bg="#f0f0f0",
            command=self.load_assets
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            asset_type_frame,
            text="Stock Assets",
            variable=self.asset_type_var,
            value="stock",
            bg="#f0f0f0",
            command=self.load_assets
        ).pack(side=tk.LEFT, padx=5)
        
        # Create toolbar frame
        toolbar_frame = tk.Frame(self.main_container, bg="#e0e0e0", padx=20, pady=10)
        toolbar_frame.pack(fill=tk.X)
        
        # Add search field
        search_label = tk.Label(
            toolbar_frame,
            text="Search:",
            bg="#e0e0e0"
        )
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            toolbar_frame,
            textvariable=self.search_var,
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        search_button = tk.Button(
            toolbar_frame,
            text="Search",
            command=self.search_assets
        )
        search_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # Add buttons
        add_button = tk.Button(
            toolbar_frame,
            text="Add Asset",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.show_add_asset_panel
        )
        add_button.pack(side=tk.RIGHT, padx=5)
        
        edit_button = tk.Button(
            toolbar_frame,
            text="Edit Asset",
            command=self.show_edit_asset_dialog
        )
        edit_button.pack(side=tk.RIGHT, padx=5)
        
        delete_button = tk.Button(
            toolbar_frame,
            text="Delete Asset",
            bg="#f44336",
            fg="white",
            command=self.delete_asset
        )
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        # Add Excel import/export buttons
        export_button = tk.Button(
            toolbar_frame,
            text="Export to Excel",
            bg="#2196F3",
            fg="white",
            command=self.export_to_excel
        )
        export_button.pack(side=tk.RIGHT, padx=5)
        
        import_button = tk.Button(
            toolbar_frame,
            text="Import from Excel",
            bg="#9C27B0",
            fg="white",
            command=self.import_from_excel
        )
        import_button.pack(side=tk.RIGHT, padx=5)
        
        template_button = tk.Button(
            toolbar_frame,
            text="Get Template",
            bg="#FF9800",
            fg="white",
            command=self.create_import_template
        )
        template_button.pack(side=tk.RIGHT, padx=5)
        
        # Create filter frame
        filter_frame = tk.Frame(self.main_container, bg="#f0f0f0", padx=20, pady=10)
        filter_frame.pack(fill=tk.X)
        
        # Add filter fields
        tk.Label(filter_frame, text="Company:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.company_var = tk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.company_var, values=["", "Meraki", "MICL", "SALES", "EDUCATION", "Steel"], width=15).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Location:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.location_var = tk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.location_var, values=["", "SS7", "SS16", "Majan"], width=15).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Category:", bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.category_var, values=["", "Laptop", "Desktop", "Server", "Printer", "Network", "Mobile", "Other"], width=15).grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Status:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.status_var = tk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.status_var, values=["", "Active", "Stock", "Attention"], width=15).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Working Status:", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.working_status_var = tk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.working_status_var, values=["", "Working", "Not Working", "Damage", "Under Maintenance"], width=15).grid(row=1, column=3, padx=5, pady=5)
        
        filter_button = tk.Button(
            filter_frame,
            text="Apply Filters",
            command=self.apply_filters
        )
        filter_button.grid(row=1, column=4, padx=5, pady=5)
        
        clear_button = tk.Button(
            filter_frame,
            text="Clear Filters",
            command=self.clear_filters
        )
        clear_button.grid(row=1, column=5, padx=5, pady=5)
        
        # Create table frame
        table_frame = tk.Frame(self.main_container, bg="#f0f0f0", padx=20, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for assets
        columns = ("ID", "Serial Number", "Company", "Location", "Category", "Status", "Username", "Model", "Working Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.column("ID", width=50)
        self.tree.column("Serial Number", width=120)
        self.tree.column("Company", width=100)
        self.tree.column("Location", width=100)
        self.tree.column("Category", width=100)
        self.tree.column("Status", width=80)
        self.tree.column("Username", width=120)
        self.tree.column("Model", width=120)
        self.tree.column("Working Status", width=120)
        
        # Configure headings
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Create context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit Asset", command=self.show_edit_asset_dialog)
        self.context_menu.add_command(label="Delete Asset", command=self.delete_asset)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Generate Issue Form", command=lambda: self.generate_asset_form("issue"))
        self.context_menu.add_command(label="Generate Transfer Form", command=lambda: self.generate_asset_form("transfer"))
        
        # Bind events
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", lambda e: self.show_edit_asset_dialog())

    def create_sliding_panel(self):
        """Create the sliding panel for adding assets"""
        # Create overlay frame
        self.overlay = tk.Frame(self.main_container, bg="black")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.configure(bg="black")
        
        # Make overlay semi-transparent by binding click to close
        self.overlay.bind("<Button-1>", lambda e: self.hide_add_asset_panel())
        
        # Create sliding panel with increased width
        panel_width = 650  # Increased from 400 to 650 for better layout
        window_width = self.main_container.winfo_width()
        
        self.sliding_panel = tk.Frame(
            self.overlay, 
            bg="white", 
            relief="raised", 
            bd=2,
            width=panel_width
        )
        
        # Position panel off-screen initially (to the right)
        self.sliding_panel.place(x=window_width, y=0, height=self.main_container.winfo_height())
        
        # Prevent panel from shrinking
        self.sliding_panel.pack_propagate(False)
        
        return panel_width, window_width

    def create_asset_form(self):
        """Create the asset form inside the sliding panel"""
        if not self.sliding_panel:
            return
            
        # Clear any existing content
        for widget in self.sliding_panel.winfo_children():
            widget.destroy()
        
        # Create modern header with gradient effect
        header_frame = tk.Frame(self.sliding_panel, bg="#2E7D32", height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_label = tk.Label(
            header_frame,
            text="📝 Add New Asset",
            font=("Segoe UI", 18, "bold"),
            bg="#2E7D32",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=25, pady=20)
        
        # Modern close button
        close_btn = tk.Button(
            header_frame,
            text="✕",
            font=("Segoe UI", 16, "bold"),
            bg="#2E7D32",
            fg="white",
            bd=0,
            command=self.hide_add_asset_panel,
            cursor="hand2",
            activebackground="#1B5E20",
            activeforeground="white"
        )
        close_btn.pack(side=tk.RIGHT, padx=25, pady=20)
        
        # Create modern form container with subtle background
        form_container = tk.Frame(self.sliding_panel, bg="#FAFAFA")
        form_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create scrollable form with modern styling
        canvas = tk.Canvas(form_container, bg="#FAFAFA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FAFAFA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=25, pady=25)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=25)
        
        # Form fields based on assets table structure
        self.form_vars = {}
        
        # Define all asset fields with their properties - organized for 2-column layout
        asset_fields = [
            # Column 1 (Left side)
            [
                ("serial_number", "Serial Number", "entry", True),  # Required
                ("category", "Category", "combo", True),  # Required
                ("company", "Company", "combo", False),
                ("location", "Location", "combo", False),
                ("status", "Status", "combo", False),
                ("username", "Username", "entry", False),
                ("designation", "Designation", "entry", False),
                ("department", "Department", "entry", False),
                ("model", "Model", "entry", False),
                ("issue_date", "Issue Date", "date", False),
                ("computer_id", "Computer ID", "entry", False),
                ("working_status", "Working Status", "combo", False),
            ],
            # Column 2 (Right side)
            [
                ("condition", "Condition", "combo", False),
                ("audit", "Audit", "entry", False),
                ("employee_id", "Employee ID", "entry", False),
                ("purchase_date", "Purchase Date", "date", False),
                ("rack_tray_number", "Rack/Tray Number", "entry", False),
                ("service_center", "Service Center", "entry", False),
                ("lpo_number", "LPO Number", "entry", False),
                ("invoice_number", "Invoice Number", "entry", False),
                ("supplier", "Supplier", "entry", False),
                ("estimated_cost", "Estimated Cost", "entry", False),
                ("description", "Description", "text", False),
                ("remarks", "Remarks", "text", False),
            ]
        ]
        
        # Combo box values
        combo_values = {
            "category": ["Laptop", "Desktop", "Server", "Printer", "Network", "Mobile", "Other"],
            "company": ["Meraki", "MICL", "SALES", "EDUCATION", "Steel"],
            "location": ["SS7", "SS16", "Majan"],
            "status": ["Active", "Stock", "Attention"],
            "working_status": ["Working", "Not Working", "Damage", "Under Maintenance"],
            "condition": ["New", "Good", "Fair", "Poor"]
        }
        
        # Configure scrollable frame for 2-column layout
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        # Create two-column layout with proper tab order (left-to-right, row-by-row)
        max_rows = max(len(asset_fields[0]), len(asset_fields[1]))
        
        # Create fields row by row to ensure proper tab order
        for row_index in range(max_rows):
            for col_index in range(2):
                # Check if this row/column combination has a field
                if row_index < len(asset_fields[col_index]):
                    field_name, label_text, field_type, required = asset_fields[col_index][row_index]
                    
                    # Create clean field frame without borders
                    field_frame = tk.Frame(scrollable_frame, bg="#FAFAFA")
                    field_frame.grid(row=row_index, column=col_index, sticky="ew", 
                                   padx=(0, 20 if col_index == 0 else 0), pady=6)
                    
                    # Modern label with better typography
                    label_display = f"{label_text} *" if required else label_text
                    label = tk.Label(
                        field_frame,
                        text=label_display,
                        font=("Segoe UI", 10, "bold" if required else "normal"),
                        bg="#FAFAFA",
                        fg="#C62828" if required else "#424242"
                    )
                    label.pack(anchor="w", padx=2, pady=(5, 2))
                    
                    # Create clean input widgets without outer borders
                    if field_type == "entry":
                        var = tk.StringVar()
                        widget = tk.Entry(
                            field_frame, 
                            textvariable=var, 
                            font=("Segoe UI", 10), 
                            relief="solid",
                            bd=1,
                            bg="#FFFFFF",
                            fg="#212121",
                            insertbackground="#2E7D32",
                            highlightthickness=1,
                            highlightcolor="#4CAF50",
                            highlightbackground="#E0E0E0"
                        )
                        
                    elif field_type == "combo":
                        var = tk.StringVar()
                        widget = ttk.Combobox(
                            field_frame, 
                            textvariable=var, 
                            values=combo_values.get(field_name, []),
                            font=("Segoe UI", 10),
                            state="readonly"
                        )
                        if field_name == "status":
                            var.set("Stock")  # Default status
                            
                    elif field_type == "text":
                        var = tk.StringVar()
                        widget = tk.Text(
                            field_frame, 
                            height=2, 
                            font=("Segoe UI", 10),
                            relief="solid",
                            bd=1,
                            bg="#FFFFFF",
                            fg="#212121",
                            insertbackground="#2E7D32",
                            wrap=tk.WORD,
                            highlightthickness=1,
                            highlightcolor="#4CAF50",
                            highlightbackground="#E0E0E0"
                        )
                        
                    elif field_type == "date":
                        var = tk.StringVar()
                        widget = tk.Entry(
                            field_frame, 
                            textvariable=var, 
                            font=("Segoe UI", 10), 
                            relief="solid",
                            bd=1,
                            bg="#FFFFFF",
                            fg="#757575",
                            insertbackground="#2E7D32",
                            highlightthickness=1,
                            highlightcolor="#4CAF50",
                            highlightbackground="#E0E0E0"
                        )
                        # Add placeholder text with better styling
                        widget.insert(0, "YYYY-MM-DD")
                        def on_focus_in(event, w=widget):
                            if w.get() == "YYYY-MM-DD":
                                w.delete(0, tk.END)
                                w.configure(fg="#212121")
                        
                        def on_focus_out(event, w=widget):
                            if not w.get():
                                w.insert(0, "YYYY-MM-DD")
                                w.configure(fg="#757575")
                        
                        widget.bind("<FocusIn>", on_focus_in)
                        widget.bind("<FocusOut>", on_focus_out)
                        
                    widget.pack(fill="x", padx=2, pady=(0, 8))
                    
                    # Store variable reference (except for Text widgets)
                    if field_type != "text":
                        self.form_vars[field_name] = var
                    else:
                        self.form_vars[field_name] = widget
        
        # Add elegant separator gradient
        separator = tk.Frame(self.sliding_panel, height=3, bg="#E0E0E0")
        separator.pack(fill=tk.X, pady=(15, 0))
        
        # Modern buttons frame with gradient background
        button_frame = tk.Frame(self.sliding_panel, bg="#F5F5F5", height=90)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=0)
        button_frame.pack_propagate(False)
        
        # Create modern button style function
        def create_modern_button(parent, text, bg_color, hover_color, command):
            button = tk.Button(
                parent,
                text=text,
                bg=bg_color,
                fg="white",
                font=("Segoe UI", 12, "bold"),
                command=command,
                cursor="hand2",
                width=16,
                height=2,
                relief="flat",
                bd=0,
                activebackground=hover_color,
                activeforeground="white"
            )
            
            # Add hover effects
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=bg_color)
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            return button
        
        # Create modern buttons with icons and hover effects
        add_btn = create_modern_button(
            button_frame,
            "✓ Add Asset",
            "#4CAF50",
            "#45a049",
            self.add_asset_to_database
        )
        add_btn.pack(side=tk.RIGHT, padx=25, pady=20)
        
        cancel_btn = create_modern_button(
            button_frame,
            "✕ Cancel",
            "#757575",
            "#616161", 
            self.hide_add_asset_panel
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 15), pady=20)
        
        # Add helpful text
        help_text = tk.Label(
            button_frame,
            text="* Required fields must be filled",
            font=("Segoe UI", 9, "italic"),
            bg="#F5F5F5",
            fg="#757575"
        )
        help_text.pack(side=tk.LEFT, padx=25, pady=20)

    def show_add_asset_panel(self):
        """Show the sliding panel with animation"""
        if self.animation_running:
            return
            
        self.animation_running = True
        
        # Update geometry to get current dimensions
        self.main_container.update_idletasks()
        
        # Create sliding panel
        panel_width, window_width = self.create_sliding_panel()
        
        # Create form
        self.create_asset_form()
        
        # Start animation
        self.animate_panel_in(panel_width, window_width)

    def animate_panel_in(self, panel_width, window_width):
        """Animate panel sliding in from right to left"""
        start_x = window_width
        end_x = window_width - panel_width
        duration = 300  # milliseconds
        steps = 20
        step_delay = duration // steps
        step_distance = (start_x - end_x) / steps
        
        def animate_step(step):
            if step <= steps:
                current_x = start_x - (step_distance * step)
                self.sliding_panel.place(x=int(current_x), y=0)
                
                # Set overlay opacity effect
                alpha = min(0.3, step / steps * 0.3)
                
                if step < steps:
                    self.after(step_delay, lambda: animate_step(step + 1))
                else:
                    self.panel_visible = True
                    self.animation_running = False
        
        animate_step(0)

    def hide_add_asset_panel(self):
        """Hide the sliding panel with animation"""
        if self.animation_running or not self.panel_visible:
            return
            
        self.animation_running = True
        
        # Get current position and dimensions
        current_x = self.sliding_panel.winfo_x()
        panel_width = self.sliding_panel.winfo_width()
        window_width = self.main_container.winfo_width()
        
        # Animate panel sliding out
        self.animate_panel_out(current_x, window_width)

    def animate_panel_out(self, start_x, window_width):
        """Animate panel sliding out from left to right"""
        end_x = window_width
        duration = 300  # milliseconds
        steps = 20
        step_delay = duration // steps
        step_distance = (end_x - start_x) / steps
        
        def animate_step(step):
            if step <= steps:
                current_x = start_x + (step_distance * step)
                self.sliding_panel.place(x=int(current_x), y=0)
                
                if step < steps:
                    self.after(step_delay, lambda: animate_step(step + 1))
                else:
                    # Remove overlay and panel
                    self.overlay.destroy()
                    self.sliding_panel = None
                    self.panel_visible = False
                    self.animation_running = False
        
        animate_step(0)

    def add_asset_to_database(self):
        """Add the asset data to the database"""
        try:
            print("Starting asset addition process...")  # Debug log
            
            # Collect form data
            asset_data = {}
            
            for field_name, widget in self.form_vars.items():
                if isinstance(widget, tk.Text):
                    # Handle text widgets
                    value = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, tk.StringVar):
                    # Handle entry and combobox widgets
                    value = widget.get().strip()
                else:
                    value = ""
                
                # Skip empty values and placeholder dates
                if value and value != "YYYY-MM-DD":
                    asset_data[field_name] = value
            
            print(f"Collected asset data: {asset_data}")  # Debug log
            
            # Validate required fields
            required_fields = ['serial_number', 'category']
            missing_fields = []
            
            for field in required_fields:
                if field not in asset_data or not asset_data[field]:
                    missing_fields.append(field.replace('_', ' ').title())
            
            if missing_fields:
                messagebox.showerror(
                    "Missing Required Fields",
                    f"Please fill in the following required fields:\n• " + "\n• ".join(missing_fields)
                )
                return
            
            # Validate serial number uniqueness
            existing_asset = self.asset_controller.get_asset_by_serial(asset_data['serial_number'])
            if existing_asset:
                messagebox.showerror(
                    "Duplicate Serial Number",
                    f"An asset with serial number '{asset_data['serial_number']}' already exists!"
                )
                return
            
            # Validate numeric fields
            if 'estimated_cost' in asset_data:
                try:
                    float(asset_data['estimated_cost'])
                except ValueError:
                    messagebox.showerror("Invalid Input", "Estimated Cost must be a valid number")
                    return
            
            # Validate date fields
            date_fields = ['issue_date', 'purchase_date']
            for date_field in date_fields:
                if date_field in asset_data:
                    date_value = asset_data[date_field]
                    try:
                        # Try to parse the date to validate format
                        from datetime import datetime
                        datetime.strptime(date_value, '%Y-%m-%d')
                    except ValueError:
                        messagebox.showerror(
                            "Invalid Date Format",
                            f"Please enter {date_field.replace('_', ' ').title()} in YYYY-MM-DD format"
                        )
                        return
            
            print("Validation passed, adding asset to database...")  # Debug log
            
            # Add the asset to database
            success, message = self.asset_controller.add_asset(asset_data)
            
            print(f"Asset addition result: success={success}, message={message}")  # Debug log
            
            if success:
                messagebox.showinfo("Success", f"Asset '{asset_data['serial_number']}' added successfully!")
                self.hide_add_asset_panel()
                self.load_assets()  # Refresh the asset list
                print("Asset added successfully and UI refreshed")
            else:
                messagebox.showerror("Error", f"Failed to add asset: {message}")
                print(f"Failed to add asset: {message}")
                
        except Exception as e:
            error_msg = f"An error occurred while adding the asset: {str(e)}"
            print(f"Exception in add_asset_to_database: {error_msg}")
            messagebox.showerror("Error", error_msg)

    def load_assets(self):
        """Load assets into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get assets based on selected type
        asset_type = self.asset_type_var.get()
        if asset_type == "active":
            assets = self.asset_controller.get_active_assets()
        elif asset_type == "stock":
            assets = self.asset_controller.get_stock_assets()
        else:
            assets = self.asset_controller.search_assets()
        
        # Add assets to treeview
        for asset in assets:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    asset.get("id"),
                    asset.get("serial_number"),
                    asset.get("company", ""),
                    asset.get("location", ""),
                    asset.get("category", ""),
                    asset.get("status", ""),
                    asset.get("username", ""),
                    asset.get("model", ""),
                    asset.get("working_status", "")
                )
            )
    
    def search_assets(self):
        """Search assets based on search term"""
        search_term = self.search_var.get()
        if not search_term:
            self.load_assets()
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search assets
        filters = {
            "serial_number": search_term
        }
        assets = self.asset_controller.search_assets(filters)
        
        # Add assets to treeview
        for asset in assets:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    asset.get("id"),
                    asset.get("serial_number"),
                    asset.get("company", ""),
                    asset.get("location", ""),
                    asset.get("category", ""),
                    asset.get("status", ""),
                    asset.get("username", ""),
                    asset.get("model", ""),
                    asset.get("working_status", "")
                )
            )
    
    def apply_filters(self):
        """Apply filters to assets"""
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
        
        if self.working_status_var.get():
            filters["working_status"] = self.working_status_var.get()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered assets
        assets = self.asset_controller.search_assets(filters)
        
        # Add assets to treeview
        for asset in assets:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    asset.get("id"),
                    asset.get("serial_number"),
                    asset.get("company", ""),
                    asset.get("location", ""),
                    asset.get("category", ""),
                    asset.get("status", ""),
                    asset.get("username", ""),
                    asset.get("model", ""),
                    asset.get("working_status", "")
                )
            )
    
    def clear_filters(self):
        """Clear all filters"""
        self.company_var.set("")
        self.location_var.set("")
        self.category_var.set("")
        self.status_var.set("")
        self.working_status_var.set("")
        self.search_var.set("")
        
        # Reload assets
        self.load_assets()
    
    def show_edit_asset_dialog(self):
        """Show dialog to edit the selected asset"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an asset to edit")
            return
        
        # Get asset ID
        asset_id = self.tree.item(selected_item[0], "values")[0]
        
        # This would be implemented with a custom dialog
        # For simplicity, we'll use a basic implementation
        messagebox.showinfo("Edit Asset", f"Edit Asset dialog for asset ID {asset_id} would be shown here")
    
    def delete_asset(self):
        """Delete the selected asset"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an asset to delete")
            return
        
        # Get asset ID
        asset_id = self.tree.item(selected_item[0], "values")[0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this asset?"):
            # Delete the asset
            success, message = self.asset_controller.delete_asset(asset_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_assets()
            else:
                messagebox.showerror("Error", message)
    
    def export_to_excel(self):
        """Export assets to Excel"""
        # Get current assets in the treeview
        assets = []
        for item in self.tree.get_children():
            asset_id = self.tree.item(item, "values")[0]
            asset = self.asset_controller.get_asset(asset_id)
            if asset:
                assets.append(asset)
        
        if not assets:
            messagebox.showinfo("No Assets", "There are no assets to export.")
            return
        
        try:
            # Export assets to Excel
            file_path = self.excel_utils.export_assets_to_excel(assets)
            
            # Show success message with option to open the file
            if messagebox.askyesno(
                "Export Successful", 
                f"Assets exported successfully to:\n{file_path}\n\nDo you want to open the file?"
            ):
                self.excel_utils.open_file(file_path)
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export assets: {str(e)}")
    
    def import_from_excel(self):
        """Import assets from Excel"""
        try:
            # Import assets from Excel
            success, message, imported_count = self.excel_utils.import_assets_from_excel()
            
            if success and imported_count > 0:
                messagebox.showinfo("Import Successful", message)
                self.load_assets()
            elif success and imported_count == 0:
                messagebox.showinfo("Import Result", message)
            else:
                messagebox.showerror("Import Error", message)
        
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import assets: {str(e)}")
    
    def create_import_template(self):
        """Create an import template"""
        try:
            # Create import template
            file_path = self.excel_utils.create_import_template()
            
            # Show success message with option to open the file
            if messagebox.askyesno(
                "Template Created", 
                f"Import template created successfully at:\n{file_path}\n\nDo you want to open the file?"
            ):
                self.excel_utils.open_file(file_path)
        
        except Exception as e:
            messagebox.showerror("Template Error", f"Failed to create template: {str(e)}")
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under the cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def generate_asset_form(self, form_type):
        """Generate an asset form"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an asset to generate a form")
            return
        
        # Get asset ID
        asset_id = self.tree.item(selected_item[0], "values")[0]
        asset = self.asset_controller.get_asset(asset_id)
        
        if not asset:
            messagebox.showerror("Error", "Failed to get asset data")
            return
        
        try:
            # Generate the form
            if form_type == "issue":
                file_path = self.excel_utils.create_asset_issue_form(asset)
                form_name = "Issue Form"
            elif form_type == "transfer":
                file_path = self.excel_utils.create_asset_transfer_form(asset)
                form_name = "Transfer Form"
            else:
                return
            
            # Show success message with option to open the file
            if messagebox.askyesno(
                f"{form_name} Created", 
                f"Asset {form_name.lower()} created successfully at:\n{file_path}\n\nDo you want to open the file?"
            ):
                self.excel_utils.open_file(file_path)
        
        except Exception as e:
            messagebox.showerror("Form Error", f"Failed to create form: {str(e)}")
