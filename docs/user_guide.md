# IT Asset Management System - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [User Interface Overview](#user-interface-overview)
4. [Asset Management](#asset-management)
5. [User Management](#user-management)
6. [Reporting](#reporting)
7. [Excel Import/Export](#excel-importexport)
8. [Backup and Restore](#backup-and-restore)
9. [Troubleshooting](#troubleshooting)

## Introduction

The IT Asset Management System is designed to help organizations efficiently track, manage, and report on their IT assets. This guide provides detailed instructions on how to use the system effectively.

## Getting Started

### Logging In

1. Launch the application by double-clicking the desktop shortcut or running `run.bat`
2. Enter your username and password in the login screen
3. Click "Login" or press Enter

Default administrator credentials:
- Username: admin
- Password: admin123

### Changing Your Password

1. After logging in, click on your username in the top-right corner
2. Select "Change Password"
3. Enter your current password and new password
4. Click "Save" to update your password

## User Interface Overview

The main interface consists of the following components:

### Main Menu
- **Dashboard**: Overview of asset status and distribution
- **Assets**: Manage IT assets (Active and Stock)
- **Users**: Manage system users (Admin only)
- **Reports**: Generate and view reports
- **Backups**: Manage database backups (Admin only)
- **Settings**: Configure system settings (Admin only)

### Toolbar
Located at the top of most screens, providing quick access to common functions:
- Add
- Edit
- Delete
- Refresh
- Export to Excel
- Import from Excel
- Get Template

### Status Bar
Located at the bottom of the screen, showing:
- Current user
- Database status
- Last backup date

## Asset Management

### Viewing Assets

1. Click "Assets" in the main menu
2. Select "Active Assets" or "Stock Assets" from the dropdown
3. The asset list will display with the first 14 fields visible by default
4. Click "Show More" to view all 24 fields
5. Use the search box to find specific assets
6. Click on column headers to sort the list

### Adding a New Asset

1. Click "Assets" in the main menu
2. Select "Active Assets" or "Stock Assets"
3. Click the "Add Asset" button in the toolbar
4. Fill in the asset details (fields marked with * are mandatory)
5. Click "Save" to add the asset

### Editing an Asset

1. Select the asset in the list
2. Click the "Edit Asset" button or double-click the asset
3. Modify the asset details
4. Click "Save" to update the asset

### Deleting an Asset

*Note: Only administrators can delete assets*

1. Select the asset in the list
2. Click the "Delete Asset" button
3. Confirm the deletion

### Moving Assets Between Active and Stock

To move an asset from Stock to Active (issue to a user):
1. In the Stock Assets view, select an asset
2. Right-click and select "Move to Active"
3. Enter the user information (Username, Department, etc.)
4. Set the Issue Date
5. Click "Save"

To move an asset from Active to Stock (return from a user):
1. In the Active Assets view, select an asset
2. Right-click and select "Move to Stock"
3. Enter the reason for return (optional)
4. Click "Save"

### Filtering Assets

1. Click the "Filter" button in the toolbar
2. Select the filter criteria (Company, Location, Category, etc.)
3. Click "Apply Filter" to show matching assets
4. Click "Clear Filter" to show all assets

## User Management

*Note: Only administrators can manage users*

### Viewing Users

1. Click "Users" in the main menu
2. The user list will display showing username, role, and email

### Adding a New User

1. Click "Users" in the main menu
2. Click the "Add User" button
3. Enter the user details:
   - Username
   - Password
   - Confirm Password
   - Role (Administrator, Standard User, Document Controller, View-Only)
   - Email
   - Full Name
4. Click "Save" to add the user

### Editing a User

1. Select the user in the list
2. Click the "Edit User" button
3. Modify the user details
4. Click "Save" to update the user

### Deleting a User

1. Select the user in the list
2. Click the "Delete User" button
3. Confirm the deletion

## Reporting

### Generating Reports

1. Click "Reports" in the main menu
2. Select the report type:
   - Asset List Report
   - Depreciation Report
   - Ageing Report
   - Lifecycle Report
   - Warranty Report
   - Maintenance Report
3. Set the report parameters (date range, filters, etc.)
4. Click "Generate Report"

### Exporting Reports

1. After generating a report, click "Export"
2. Select the export format (CSV or Excel)
3. Choose the save location
4. Click "Save"

## Excel Import/Export

### Exporting Assets to Excel

1. In the Asset Management screen, click "Export to Excel" in the toolbar
2. The system will generate an Excel file with all visible assets
3. The file will be saved in the "exports" folder
4. You will be prompted to open the file

### Importing Assets from Excel

1. In the Asset Management screen, click "Import from Excel" in the toolbar
2. Select the Excel file to import
3. The system will validate the data and report any errors
4. Valid assets will be imported into the system
5. Review the import summary

### Creating Import Templates

1. Click "Get Template" in the toolbar
2. The template will include all required fields and example data
3. The file will be saved in the "templates" folder
4. You will be prompted to open the file

### Generating Asset Forms

1. Select an asset in the list
2. Right-click and select "Generate Issue Form" or "Generate Transfer Form"
3. The form will be generated as an Excel file
4. The file will be saved in the "exports" folder
5. You will be prompted to open the file

## Backup and Restore

### Automated Backups

The system automatically creates daily backups at midnight. Backups are retained for 365 days and stored in the "backups" folder.

### Manual Backups

1. Click "Backups" in the main menu (Administrator only)
2. Click "Create Backup"
3. Enter a description for the backup (optional)
4. Click "Save" to create the backup

### Restoring from Backup

1. Click "Backups" in the main menu (Administrator only)
2. Select a backup from the list
3. Click "Restore Backup"
4. Confirm the restoration
5. The system will restart after restoration is complete

## Troubleshooting

### Common Issues and Solutions

#### Application Won't Start

- Ensure Python is installed and in the PATH
- Check that all dependencies are installed
- Verify that the database file exists
- Check the log file in the "logs" folder for error messages

#### Login Issues

- Verify username and password
- Check if the database is corrupted
- Try resetting the admin password:
  1. Delete the database file (data.db)
  2. Run `python -c "from src.config.database import db_config; db_config.initialize_database()"`
  3. Log in with the default admin credentials

#### Import/Export Issues

- Ensure the Excel file has the correct format
- Check that all required fields are present
- Verify that the file is not open in another application
- Check for duplicate serial numbers

### Error Messages

- **"Serial number already exists"**: Each asset must have a unique serial number
- **"Missing required field"**: All mandatory fields must be filled
- **"Database error"**: The database may be corrupted or inaccessible
- **"Permission denied"**: Your user role does not have permission for this action

### Getting Help

For additional help or to report issues, please contact:
- Email: support@example.com
- Phone: +123-456-7890
