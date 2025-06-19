"""
Report Controller for IT Asset Management System
Handles business logic for generating various reports
"""
import os
import csv
import sqlite3
from datetime import datetime, timedelta
from src.models.asset_model import AssetModel

class ReportController:
    def __init__(self, current_user=None):
        """
        Initialize the report controller
        
        Args:
            current_user (dict, optional): The currently logged in user
        """
        self.asset_model = AssetModel()
        self.current_user = current_user
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports')
        
        # Create reports directory if it doesn't exist
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def generate_report(self, report_type, filters=None, export_format='csv'):
        """
        Generate a report based on the specified type and filters
        
        Args:
            report_type (str): Type of report to generate
            filters (dict, optional): Filters to apply to the report
            export_format (str, optional): Format to export the report (csv, pdf)
        
        Returns:
            str: Path to the generated report file
            list: Report data
        """
        # Map report types to their respective generation methods
        report_generators = {
            'asset_list': self._generate_asset_list_report,
            'depreciation': self._generate_depreciation_report,
            'ageing': self._generate_ageing_report,
            'lifecycle': self._generate_lifecycle_report,
            'warranty': self._generate_warranty_report,
            'maintenance': self._generate_maintenance_report
        }
        
        # Check if the requested report type is supported
        if report_type not in report_generators:
            return None, []
        
        # Generate the report
        return report_generators[report_type](filters, export_format)
    
    def _generate_asset_list_report(self, filters=None, export_format='csv'):
        """
        Generate a report of all assets based on filters
        
        Args:
            filters (dict, optional): Filters to apply to the report
            export_format (str, optional): Format to export the report
        
        Returns:
            str: Path to the generated report file
            list: Report data
        """
        # Get the assets based on filters
        assets = self.asset_model.get_all_assets(filters)
        
        if not assets:
            return None, []
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"asset_list_report_{timestamp}.{export_format}"
        file_path = os.path.join(self.reports_dir, filename)
        
        # Export to CSV
        if export_format == 'csv':
            with open(file_path, 'w', newline='') as csvfile:
                # Get field names from the first asset
                fieldnames = assets[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for asset in assets:
                    writer.writerow(asset)
        
        # Export to PDF would be implemented here
        # This would require additional libraries like reportlab
        
        return file_path, assets
    
    def _generate_depreciation_report(self, filters=None, export_format='csv'):
        """
        Generate a depreciation report for assets
        
        Args:
            filters (dict, optional): Filters to apply to the report
            export_format (str, optional): Format to export the report
        
        Returns:
            str: Path to the generated report file
            list: Report data
        """
        # Get the assets based on filters
        assets = self.asset_model.get_all_assets(filters)
        
        if not assets:
            return None, []
        
        # Calculate depreciation for each asset
        depreciation_data = []
        current_date = datetime.now()
        
        for asset in assets:
            # Skip assets without purchase date or cost
            if not asset.get('purchase_date') or not asset.get('estimated_cost'):
                continue
            
            try:
                # Parse purchase date
                purchase_date = datetime.strptime(asset.get('purchase_date'), '%Y-%m-%d')
                
                # Calculate age in years
                age_days = (current_date - purchase_date).days
                age_years = age_days / 365.25
                
                # Assume 5-year straight-line depreciation (20% per year)
                depreciation_rate = 0.2
                
                # Calculate current value
                original_cost = float(asset.get('estimated_cost'))
                depreciation_amount = original_cost * min(age_years * depreciation_rate, 1)
                current_value = max(original_cost - depreciation_amount, 0)
                
                # Add to report data
                asset_data = {
                    'id': asset.get('id'),
                    'serial_number': asset.get('serial_number'),
                    'category': asset.get('category'),
                    'model': asset.get('model'),
                    'purchase_date': asset.get('purchase_date'),
                    'original_cost': original_cost,
                    'age_years': round(age_years, 2),
                    'depreciation_amount': round(depreciation_amount, 2),
                    'current_value': round(current_value, 2),
                    'depreciation_percentage': min(round(age_years * depreciation_rate * 100, 2), 100)
                }
                
                depreciation_data.append(asset_data)
                
            except (ValueError, TypeError) as e:
                print(f"Error calculating depreciation for asset {asset.get('id')}: {e}")
                continue
        
        if not depreciation_data:
            return None, []
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"depreciation_report_{timestamp}.{export_format}"
        file_path = os.path.join(self.reports_dir, filename)
        
        # Export to CSV
        if export_format == 'csv':
            with open(file_path, 'w', newline='') as csvfile:
                # Get field names from the first item
                fieldnames = depreciation_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for item in depreciation_data:
                    writer.writerow(item)
        
        return file_path, depreciation_data
    
    def _generate_ageing_report(self, filters=None, export_format='csv'):
        """
        Generate an ageing report for assets
        
        Args:
            filters (dict, optional): Filters to apply to the report
            export_format (str, optional): Format to export the report
        
        Returns:
            str: Path to the generated report file
            list: Report data
        """
        # Get the assets based on filters
        assets = self.asset_model.get_all_assets(filters)
        
        if not assets:
            return None, []
        
        # Calculate age for each asset
        ageing_data = []
        current_date = datetime.now()
        
        # Age categories in years
        age_categories = {
            'Less than 3 years': 3,
            '3-5 years': 5,
            '5-7 years': 7,
            '7-10 years': 10,
            'Over 10 years': float('inf')
        }
        
        for asset in assets:
            # Skip assets without purchase date
            if not asset.get('purchase_date'):
                continue
            
            try:
                # Parse purchase date
                purchase_date = datetime.strptime(asset.get('purchase_date'), '%Y-%m-%d')
                
                # Calculate age in years
                age_days = (current_date - purchase_date).days
                age_years = age_days / 365.25
                
                # Determine age category
                age_category = 'Unknown'
                for category, threshold in age_categories.items():
                    if age_years < threshold:
                        age_category = category
                        break
                
                # Add to report data
                asset_data = {
                    'id': asset.get('id'),
                    'serial_number': asset.get('serial_number'),
                    'category': asset.get('category'),
                    'model': asset.get('model'),
                    'purchase_date': asset.get('purchase_date'),
                    'age_years': round(age_years, 2),
                    'age_category': age_category
                }
                
                ageing_data.append(asset_data)
                
            except (ValueError, TypeError) as e:
                print(f"Error calculating age for asset {asset.get('id')}: {e}")
                continue
        
        if not ageing_data:
            return None, []
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ageing_report_{timestamp}.{export_format}"
        file_path = os.path.join(self.reports_dir, filename)
        
        # Export to CSV
        if export_format == 'csv':
            with open(file_path, 'w', newline='') as csvfile:
                # Get field names from the first item
                fieldnames = ageing_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for item in ageing_data:
                    writer.writerow(item)
        
        return file_path, ageing_data
    
    def _generate_lifecycle_report(self, filters=None, export_format='csv'):
        """
        Generate a lifecycle report for assets
        
        Args:
            filters (dict, optional): Filters to apply to the report
            export_format (str, optional): Format to export the report
        
        Returns:
            str: Path to the generated report file
            list: Report data
        """
        # Get the assets based on filters
        assets = self.asset_model.get_all_assets(filters)
        
        if not assets:
            return None, []
        
        # Calculate lifecycle data for each asset
        lifecycle_data = []
        current_date = datetime.now()
        
        # Assume 5-year lifecycle for IT assets
        lifecycle_years = 5
        
        for asset in assets:
            # Skip assets without purchase date
            if not asset.get('purchase_date'):
                continue
            
            try:
                # Parse purchase date
                purchase_date = datetime.strptime(asset.get('purchase_date'), '%Y-%m-%d')
                
                # Calculate age in years
                age_days = (current_date - purchase_date).days
                age_years = age_days / 365.25
                
                # Calculate end of lifecycle date
                eol_date = purchase_date + timedelta(days=int(lifecycle_years * 365.25))
                
                # Calculate remaining lifecycle
                remaining_days = (eol_date - current_date).days
                remaining_years = remaining_days / 365.25
                
                # Determine lifecycle status
                if remaining_years <= 0:
                    lifecycle_status = 'End of Life'
                    replacement_priority = 'High'
                elif remaining_years < 1:
                    lifecycle_status = 'Approaching End of Life'
                    replacement_priority = 'Medium'
                else:
                    lifecycle_status = 'Active'
                    replacement_priority = 'Low'
                
                # Add to report data
                asset_data = {
                    'id': asset.get('id'),
                    'serial_number': asset.get('serial_number'),
                    'category': asset.get('category'),
                    'model': asset.get('model'),
                    'purchase_date': asset.get('purchase_date'),
                    'age_years': round(age_years, 2),
                    'eol_date': eol_date.strftime('%Y-%m-%d'),
                    'remaining_years': round(max(remaining_years, 0), 2),
                    'lifecycle_status': lifecycle_status,
                    'replacement_priority': replacement_priority
                }
                
                lifecycle_data.append(asset_data)
                
            except (ValueError, TypeError) as e:
                print(f"Error calculating lifecycle for asset {asset.get('id')}: {e}")
                continue
        
        if not lifecycle_data:
            return None, []
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"lifecycle_report_{timestamp}.{export_format}"
        file_path = os.path.join(self.reports_dir, filename)
        
        # Export to CSV
        if export_format == 'csv':
            with open(file_path, 'w', newline='') as csvfile:
                # Get field names from the first item
                fieldnames = lifecycle_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for item in lifecycle_data:
                    writer.writerow(item)
        
        return file_path, lifecycle_data
    
    def _generate_warranty_report(self, filters=None, export_format='csv'):
        """
        Generate a warranty report for assets
        
        Args:
            filters (dict, optional): Filters to apply to the report
            export_format (str, optional): Format to export the report
        
        Returns:
            str: Path to the generated report file
            list: Report data
        """
        # This is a placeholder for the warranty report
        # In a real implementation, you would need to add warranty information to the assets table
        return None, []
    
    def _generate_maintenance_report(self, filters=None, export_format='csv'):
        """
        Generate a maintenance report for assets
        
        Args:
            filters (dict, optional): Filters to apply to the report
            export_format (str, optional): Format to export the report
        
        Returns:
            str: Path to the generated report file
            list: Report data
        """
        # This is a placeholder for the maintenance report
        # In a real implementation, you would need to add maintenance history to the assets table
        return None, []
