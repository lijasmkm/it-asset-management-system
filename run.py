"""
IT Asset Management System
Run script to start the application
"""
import os
import sys
from src.main import Application

if __name__ == "__main__":
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Create and run the application
    app = Application()
    app.mainloop()
