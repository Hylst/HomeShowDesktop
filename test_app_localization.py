#!/usr/bin/env python3
"""
Test script for application localization integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from core.localization import get_localization_manager, translate, set_language
from gui.main_window import MainWindow
from core.database import DatabaseManager
from core.property_manager import PropertyManager
from core.media_handler import MediaHandler

def test_localization_integration():
    """
    Test localization integration in a minimal GUI
    """
    print("Testing Localization Integration")
    print("=" * 40)
    
    # Create test window
    root = tk.Tk()
    root.title("Localization Test")
    root.geometry("600x400")
    
    # Initialize localization
    localization = get_localization_manager()
    
    # Create test interface
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(
        main_frame,
        text=translate('app_title'),
        font=('Segoe UI', 16, 'bold')
    )
    title_label.pack(pady=(0, 20))
    
    # Language selection
    lang_frame = ttk.LabelFrame(main_frame, text="Language / Langue", padding=10)
    lang_frame.pack(fill=tk.X, pady=(0, 20))
    
    def change_language(lang):
        set_language(lang)
        update_interface()
    
    ttk.Button(
        lang_frame,
        text="English",
        command=lambda: change_language('en')
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    ttk.Button(
        lang_frame,
        text="Français",
        command=lambda: change_language('fr')
    ).pack(side=tk.LEFT)
    
    # Test content
    content_frame = ttk.LabelFrame(main_frame, text="Test Content", padding=10)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create labels that will be updated
    labels = {}
    
    # Dashboard items
    labels['welcome'] = ttk.Label(content_frame, text="", font=('Segoe UI', 12, 'bold'))
    labels['welcome'].pack(anchor=tk.W, pady=2)
    
    labels['subtitle'] = ttk.Label(content_frame, text="", foreground='gray')
    labels['subtitle'].pack(anchor=tk.W, pady=2)
    
    ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=10)
    
    # Menu items
    menu_frame = ttk.Frame(content_frame)
    menu_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(menu_frame, text="Menu Items:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
    
    labels['menu_file'] = ttk.Label(menu_frame, text="")
    labels['menu_file'].pack(anchor=tk.W, padx=(20, 0))
    
    labels['menu_tools'] = ttk.Label(menu_frame, text="")
    labels['menu_tools'].pack(anchor=tk.W, padx=(20, 0))
    
    labels['menu_help'] = ttk.Label(menu_frame, text="")
    labels['menu_help'].pack(anchor=tk.W, padx=(20, 0))
    
    ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=10)
    
    # Wizard items
    wizard_frame = ttk.Frame(content_frame)
    wizard_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(wizard_frame, text="Wizard Steps:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
    
    labels['wizard_title'] = ttk.Label(wizard_frame, text="")
    labels['wizard_title'].pack(anchor=tk.W, padx=(20, 0))
    
    labels['wizard_basic'] = ttk.Label(wizard_frame, text="")
    labels['wizard_basic'].pack(anchor=tk.W, padx=(20, 0))
    
    labels['wizard_media'] = ttk.Label(wizard_frame, text="")
    labels['wizard_media'].pack(anchor=tk.W, padx=(20, 0))
    
    def update_interface():
        """Update all interface elements with current language"""
        # Update title
        title_label.config(text=translate('app_title'))
        
        # Update content frame title
        content_frame.config(text=f"Test Content - Current Language: {localization.get_language().upper()}")
        
        # Update labels
        labels['welcome'].config(text=f"Welcome: {translate('dashboard_welcome')}")
        labels['subtitle'].config(text=f"Subtitle: {translate('dashboard_subtitle')}")
        
        labels['menu_file'].config(text=f"• File: {translate('menu_file')}")
        labels['menu_tools'].config(text=f"• Tools: {translate('menu_tools')}")
        labels['menu_help'].config(text=f"• Help: {translate('menu_help')}")
        
        labels['wizard_title'].config(text=f"• Title: {translate('wizard_title')}")
        labels['wizard_basic'].config(text=f"• Basic Info: {translate('wizard_basic_info')}")
        labels['wizard_media'].config(text=f"• Media Upload: {translate('wizard_media_upload')}")
    
    # Initial update
    update_interface()
    
    # Status
    status_frame = ttk.Frame(main_frame)
    status_frame.pack(fill=tk.X, pady=(10, 0))
    
    ttk.Label(
        status_frame,
        text="Click language buttons to test dynamic switching",
        foreground='blue'
    ).pack()
    
    print("Localization test window opened. Test language switching manually.")
    print("Close the window when done testing.")
    
    # Run the test window
    root.mainloop()
    
    print("Localization integration test completed.")

if __name__ == "__main__":
    test_localization_integration()