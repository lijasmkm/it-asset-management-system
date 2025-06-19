# IT Asset Management System

**Version:** 1.0.0  
**Date:** April 2025  
**Developed by:** Vinoj Kumar / Meraki Group

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
5. [User Roles](#user-roles)
6. [Asset Management](#asset-management)
7. [Reporting](#reporting)
8. [Excel Import/Export](#excel-importexport)
9. [Backup and Restore](#backup-and-restore)
10. [Troubleshooting](#troubleshooting)

## Introduction

The IT Asset Management System is a comprehensive solution designed to effectively track, manage, and report IT assets within an organization. It provides a centralized system for managing both active (issued) and stock (unassigned) assets with detailed reporting capabilities.

## Installation

### System Requirements
- Windows 7/10/11 or Linux/macOS
- Python 3.8 or higher
- 4GB RAM (minimum)
- 500MB free disk space

### Windows Installation

1. **Automatic Installation**
   - Double-click the `install.bat` file
   - Follow the on-screen instructions
   - The installer will create desktop and start menu shortcuts

2. **Manual Installation**
   - Ensure Python 3.8+ is installed
   - Open Command Prompt in the application directory
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment: `venv\Scripts\activate`
   - Install dependencies: `pip install -r requirements.txt`
   - Initialize the database: `python -c "from src.config.database import db_config; db_config.initialize_database()"`

### Linux/macOS Installation

1. Open Terminal in the application directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize the database: `python -c "from src.config.database import db_config; db_config.initialize_database()"`

## Getting Started

### Running the Application

- **Windows:** Double-click the `run.bat` file or use the created shortcuts
- **Linux/macOS:** In Terminal, activate the virtual environment and run `python run.py`

*Important: Change the default password after first login for security reasons.*

## Features

- **Asset Management:** Track and manage IT assets with 24 customizable fields
- **Differentiated Views:** Separate views for Active (issued) and Stock (unassigned) assets
- **Dashboard:** Overview summary of asset status and distribution
- **Advanced Filtering:** Filter assets by multiple criteria
- **Detailed Reporting:** Generate analytical reports (Depreciation, Ageing, Lifecycle, etc.)
- **Excel Integration:** Import and export asset data in Excel format
- **Form Generation:** Create asset issue and transfer forms
- **Automated Backups:** Daily backups retained for 365 days
- **Role-based Access:** Four user roles with different permission levels
- **Audit Logging:** Track all changes to assets

## User Roles

1. **Administrator (Super User)**
   - Full access to all features
   - Can add, update, move, and delete assets
   - Can manage users and system settings

2. **Standard User**
   - Can add, update, and move assets
   - Cannot delete assets
   - Limited access to system settings

3. **Document Controller (DC)**
   - Can only update specific fields (Employee ID, Designation, Department, LPO, Invoice)
   - Cannot edit other fields or delete assets

4. **View-Only User**
   - Can only view assets and reports
   - Cannot make any changes to the system

## Asset Management

### Asset Fields

The system tracks 24 fields for each asset, with the first 14 visible by default:

1. Company (Meraki, MICL, SALES, EDUCATION, Steel)
2. Location (SS7/SS16/Majan)
3. Category *
4. Status (Active/Stock/Attention)
5. Username
6. Designation
7. Department
8. Model
9. Description
10. Serial Number (Primary Key) *
11. Issue Date
12. Computer ID
13. Working Status (Working/Not Working/Damage/Under Maintenance)
14. Condition (New/Good/Fair/Poor)
15. Audit
16. Employee ID
17. Purchase Date
18. Rack/Tray Number
19. Service Center
20. LPO Number
21. Invoice Number
22. Supplier
23. Estimated Cost
24. Remarks

*Fields marked with * are mandatory*

### Adding Assets

1. Click the "Add Asset" button in the Asset Management screen
2. Fill in the required fields (Serial Number and Category are mandatory)
3. Select the appropriate status (Active or Stock)
4. Click "Save" to add the asset

### Editing Assets

1. Select an asset from the list
2. Click the "Edit Asset" button or double-click the asset
3. Modify the desired fields
4. Click "Save" to update the asset

### Moving Assets

To move an asset from Stock to Active (issue to a user):
1. Select a Stock asset
2. Right-click and select "Move to Active"
3. Enter the user information
4. Click "Save"

To move an asset from Active to Stock (return from a user):
1. Select an Active asset
2. Right-click and select "Move to Stock"
3. Enter the reason for return (optional)
4. Click "Save"

## Reporting

The system provides several analytical reports:

1. **Asset List Report:** List of all assets with filtering options
2. **Depreciation Report:** Track asset value over time
3. **Ageing Report:** Identify assets older than 3/5/7/10 years
4. **Lifecycle Report:** Identify aging assets requiring replacement
5. **Warranty Report:** Track warranty status and expiration
6. **Maintenance Report:** Track maintenance history and schedules

### Generating Reports

1. Go to the Reports tab
2. Select the report type
3. Apply any desired filters
4. Select the export format (CSV or PDF)
5. Click "Generate Report"

## Excel Import/Export

### Exporting Assets to Excel

1. In the Asset Management screen, click "Export to Excel"
2. The system will generate an Excel file with all visible assets
3. The file will be saved in the "exports" folder
4. You will be prompted to open the file

### Importing Assets from Excel

1. In the Asset Management screen, click "Import from Excel"
2. Select the Excel file to import
3. The system will validate the data and report any errors
4. Valid assets will be imported into the system

### Creating Import Templates

1. Click "Get Template" to generate an import template
2. The template will include all required fields and example data
3. The file will be saved in the "templates" folder

### Generating Asset Forms

1. Select an asset in the list
2. Right-click and select "Generate Issue Form" or "Generate Transfer Form"
3. The form will be generated as an Excel file
4. The file will be saved in the "exports" folder

## Backup and Restore

### Automated Backups

The system automatically creates daily backups at midnight. Backups are retained for 365 days and stored in the "backups" folder.

### Manual Backups

1. Go to the Backups tab (Administrator only)
2. Click "Create Backup"
3. The system will create a backup of the database

### Restoring from Backup

1. Go to the Backups tab (Administrator only)
2. Select a backup from the list
3. Click "Restore Backup"
4. Confirm the restoration

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Ensure Python is installed and in the PATH
   - Check that all dependencies are installed
   - Verify that the database file exists

2. **Login issues**
   - Verify username and password
   - Check if the database is corrupted
   - Try resetting the admin password

3. **Import/Export issues**
   - Ensure the Excel file has the correct format
   - Check that all required fields are present
   - Verify that the file is not open in another application

### Getting Help

For additional help or to report issues, please contact:
- Email: support@example.com
- Phone: +123-456-7890

---

© 2025 Vinoj Kumar / Meraki Group. All rights reserved.
