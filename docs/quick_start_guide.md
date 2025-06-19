# IT Asset Management System - Quick Start Guide

This guide provides a quick overview of how to install and start using the IT Asset Management System.

## Installation

### Windows

1. **Automatic Installation**
   - Double-click the `install.bat` file
   - Follow the on-screen instructions
   - The installer will create desktop and start menu shortcuts

2. **Manual Installation**
   - Ensure Python 3.8+ is installed
   - Open Command Prompt in the application directory
   - Run: `python -m venv venv`
   - Run: `venv\Scripts\activate`
   - Run: `pip install -r requirements.txt`
   - Run: `python -c "from src.config.database import db_config; db_config.initialize_database()"`

## Running the Application

- Double-click the `run.bat` file or use the created shortcuts
- Or run: `venv\Scripts\activate` followed by `python run.py`

## First Login

- **Username:** admin
- **Password:** admin123
- Change your password after first login

## Quick Tasks

### Add an Asset
1. Click "Assets" → Select "Active Assets" or "Stock Assets"
2. Click "Add Asset" button
3. Fill in the details (Serial Number and Category are mandatory)
4. Click "Save"

### Export Assets to Excel
1. In the Asset Management screen
2. Click "Export to Excel" in the toolbar
3. The file will be saved in the "exports" folder

### Import Assets from Excel
1. In the Asset Management screen
2. Click "Import from Excel" in the toolbar
3. Select the Excel file to import
4. Review the import summary

### Generate a Report
1. Click "Reports" in the main menu
2. Select the report type
3. Set any filters
4. Click "Generate Report"

### Create a Backup
1. Click "Backups" in the main menu (Admin only)
2. Click "Create Backup"
3. Enter a description (optional)
4. Click "Save"

## Asset Management Tips

- Use the search box to quickly find assets
- Right-click on assets for additional options
- Use "Show More" to view all 24 asset fields
- Filter assets by clicking the "Filter" button

## Need Help?

- See the full User Guide in the docs folder
- Contact support at support@example.com
