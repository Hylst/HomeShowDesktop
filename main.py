#!/usr/bin/env python3
"""
HomeShow Desktop - Real Estate Website Generator
Main entry point for the application

Author: AI Assistant
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from gui.main_window import MainWindow
    from core.database import DatabaseManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all dependencies are installed.")
    sys.exit(1)

def setup_application():
    """
    Initialize application directories and database
    """
    # Create necessary directories
    directories = [
        'data',
        'data/projects',
        'resources/icons',
        'resources/templates'
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    print("Application setup completed successfully.")

def main():
    """
    Main application entry point
    """
    try:
        # Setup application
        setup_application()
        
        # Start GUI application
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()