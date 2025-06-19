"""
Setup script for IT Asset Management System
This script will create an installer for the application
"""
from setuptools import setup, find_packages

setup(
    name="it-asset-management",
    version="1.0.0",
    description="IT Asset Management System",
    author="Vinoj Kumar / Meraki Group",
    author_email="admin@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "schedule>=1.1.0",
        "pillow>=9.5.0",
        "reportlab>=3.6.12",
        "openpyxl>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "it-asset-management=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
