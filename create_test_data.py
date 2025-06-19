"""
Create test data for IT Asset Management System and export to Excel
"""
import os
import sys
import sqlite3
from datetime import datetime, timedelta
import random

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.asset_model import AssetModel
from src.utils.excel_utils import ExcelUtils

def create_test_data():
    """Create test data and export to Excel"""
    # Initialize asset model
    asset_model = AssetModel()
    
    # Sample data
    companies = ["Meraki", "MICL", "SALES", "EDUCATION", "Steel"]
    locations = ["SS7", "SS16", "Majan"]
    categories = ["Laptop", "Desktop", "Server", "Printer", "Network Device", "Mobile Device"]
    statuses = ["Active", "Stock"]
    models = {
        "Laptop": ["Dell Latitude 5420", "HP EliteBook 840", "Lenovo ThinkPad T14", "MacBook Pro"],
        "Desktop": ["Dell OptiPlex 7090", "HP EliteDesk 800", "Lenovo ThinkCentre M70q"],
        "Server": ["Dell PowerEdge R740", "HP ProLiant DL380", "Lenovo ThinkSystem SR650"],
        "Printer": ["HP LaserJet Pro M404", "Epson WorkForce Pro WF-C5790", "Brother MFC-L8900CDW"],
        "Network Device": ["Cisco Catalyst 9200", "HP Aruba 2930F", "Ubiquiti UniFi Switch"],
        "Mobile Device": ["iPhone 13", "Samsung Galaxy S21", "Google Pixel 6"]
    }
    working_statuses = ["Working", "Not Working", "Damage", "Under Maintenance"]
    conditions = ["New", "Good", "Fair", "Poor"]
    departments = ["IT", "Finance", "HR", "Sales", "Marketing", "Operations"]
    designations = ["Manager", "Assistant", "Director", "Coordinator", "Specialist", "Analyst"]
    
    # Generate test assets
    test_assets = []
    for i in range(1, 21):  # Create 20 test assets
        # Generate random data
        category = random.choice(categories)
        status = random.choice(statuses)
        company = random.choice(companies)
        location = random.choice(locations)
        model = random.choice(models[category])
        working_status = random.choice(working_statuses)
        condition = random.choice(conditions)
        
        # Generate serial number
        serial_prefix = category[:3].upper()
        serial_number = f"{serial_prefix}{company[:2].upper()}{i:06d}"
        
        # Generate purchase date (between 1 and 5 years ago)
        days_ago = random.randint(365, 365 * 5)
        purchase_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Create asset data
        asset_data = {
            "serial_number": serial_number,
            "company": company,
            "location": location,
            "category": category,
            "status": status,
            "model": model,
            "description": f"{model} - Test Asset {i}",
            "working_status": working_status,
            "condition": condition,
            "purchase_date": purchase_date,
            "estimated_cost": round(random.uniform(500, 3000), 2)
        }
        
        # Add user information for active assets
        if status == "Active":
            asset_data["username"] = f"User{i}"
            asset_data["department"] = random.choice(departments)
            asset_data["designation"] = random.choice(designations)
            asset_data["employee_id"] = f"EMP{i:04d}"
            asset_data["issue_date"] = (datetime.now() - timedelta(days=random.randint(1, 300))).strftime('%Y-%m-%d')
        
        # Add the asset
        success, message = asset_model.add_asset(asset_data)
        if success:
            print(f"Added asset: {serial_number}")
            test_assets.append(asset_model.get_asset_by_serial(serial_number))
        else:
            print(f"Failed to add asset {serial_number}: {message}")
    
    # Export assets to Excel
    if test_assets:
        excel_utils = ExcelUtils()
        export_path = excel_utils.export_assets_to_excel(test_assets, "test_assets_export.xlsx")
        print(f"\nExported test assets to: {export_path}")
        return export_path
    else:
        print("No assets to export")
        return None

if __name__ == "__main__":
    export_path = create_test_data()
    if export_path:
        print("\nTest data creation and export completed successfully.")
        print(f"You can find the export file at: {export_path}")
    else:
        print("\nFailed to create test data or export file.")
