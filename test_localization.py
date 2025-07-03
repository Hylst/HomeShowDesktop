#!/usr/bin/env python3
"""
Test script for localization system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.localization import get_localization_manager, translate, set_language

def test_localization():
    """
    Test the localization system
    """
    print("Testing Localization System")
    print("=" * 40)
    
    # Initialize localization
    localization = get_localization_manager()
    
    # Test English (default)
    print("\n--- English ---")
    set_language('en')
    print(f"Welcome: {translate('dashboard_welcome')}")
    print(f"Subtitle: {translate('dashboard_subtitle')}")
    print(f"Quick Actions: {translate('dashboard_quick_actions')}")
    print(f"New Property: {translate('dashboard_new_property')}")
    print(f"Generate Website: {translate('dashboard_generate_website')}")
    
    # Test French
    print("\n--- French ---")
    set_language('fr')
    print(f"Welcome: {translate('dashboard_welcome')}")
    print(f"Subtitle: {translate('dashboard_subtitle')}")
    print(f"Quick Actions: {translate('dashboard_quick_actions')}")
    print(f"New Property: {translate('dashboard_new_property')}")
    print(f"Generate Website: {translate('dashboard_generate_website')}")
    
    # Test menu items
    print("\n--- Menu Items (French) ---")
    print(f"File: {translate('menu_file')}")
    print(f"Edit: {translate('menu_edit')}")
    print(f"Tools: {translate('menu_tools')}")
    print(f"Language: {translate('menu_language')}")
    print(f"Help: {translate('menu_help')}")
    
    # Test wizard items
    print("\n--- Wizard Items (French) ---")
    print(f"Wizard Title: {translate('wizard_title')}")
    print(f"Create Property: {translate('wizard_create_property')}")
    print(f"Basic Info: {translate('wizard_basic_info')}")
    print(f"Media Upload: {translate('wizard_media_upload')}")
    print(f"Features: {translate('wizard_features')}")
    print(f"Location: {translate('wizard_location')}")
    print(f"Advanced: {translate('wizard_advanced')}")
    print(f"Review: {translate('wizard_review')}")
    
    # Test tabs
    print("\n--- Tabs (French) ---")
    print(f"Dashboard: {translate('tab_dashboard')}")
    print(f"Properties: {translate('tab_properties')}")
    print(f"Projects: {translate('tab_projects')}")
    print(f"Templates: {translate('tab_templates')}")
    
    print("\n--- Test completed successfully! ---")

if __name__ == "__main__":
    test_localization()