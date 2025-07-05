#!/usr/bin/env python3
"""
Test script for property editing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.property_manager import PropertyManager
from core.database import DatabaseManager
from pathlib import Path

def test_property_editing():
    """
    Test property editing functionality
    """
    print("Testing property editing functionality...")
    
    # Initialize database and property manager
    db_manager = DatabaseManager()
    property_manager = PropertyManager(db_manager)
    
    # Create a test property
    test_property_data = {
        'title': 'Test Property for Editing',
        'description': 'This is a test property to verify editing functionality',
        'price': 250000,
        'property_type': 'House',
        'transaction_type': 'For Sale',
        'bedrooms': 3,
        'bathrooms': 2,
        'surface_area': 120,
        'address': '123 Test Street',
        'city': 'Test City',
        'postal_code': '12345',
        'country': 'Test Country',
        'features': ['Parking', 'Garden'],
        'additional_features': ['Terrace']
    }
    
    try:
        # Create property
        property_id = property_manager.create_property(test_property_data)
        print(f"✓ Test property created with ID: {property_id}")
        
        # Retrieve the property
        retrieved_property = property_manager.get_property_by_id(property_id)
        print(f"✓ Property retrieved: {retrieved_property['title']}")
        
        # Test editing
        updated_data = retrieved_property.copy()
        updated_data['title'] = 'Updated Test Property'
        updated_data['price'] = 275000
        updated_data['bedrooms'] = 4
        updated_data['description'] = 'This property has been updated successfully'
        
        # Update property
        success = property_manager.update_property(property_id, updated_data)
        if success:
            print("✓ Property updated successfully")
        else:
            print("✗ Failed to update property")
            return False
        
        # Verify the update
        updated_property = property_manager.get_property_by_id(property_id)
        if updated_property['title'] == 'Updated Test Property':
            print("✓ Property title updated correctly")
        else:
            print("✗ Property title not updated")
            return False
            
        if updated_property['price'] == 275000:
            print("✓ Property price updated correctly")
        else:
            print("✗ Property price not updated")
            return False
            
        if updated_property['bedrooms'] == 4:
            print("✓ Property bedrooms updated correctly")
        else:
            print("✗ Property bedrooms not updated")
            return False
        
        # Clean up - delete test property
        property_manager.delete_property(property_id)
        print("✓ Test property cleaned up")
        
        print("\n🎉 All property editing tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_property_editing()
    sys.exit(0 if success else 1)