#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for property deletion and duplication functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.property_manager import PropertyManager
from core.localization import LocalizationManager
from core.database import DatabaseManager

def test_property_deletion_duplication():
    """
    Test property deletion and duplication functionality
    """
    print("=== Test de suppression et duplication de propriétés ===")
    
    # Initialize components
    db = DatabaseManager()
    db.initialize_database()
    property_manager = PropertyManager(db)
    localization = LocalizationManager()
    
    # Test in both languages
    for lang in ['fr', 'en']:
        print(f"\n--- Test en {lang.upper()} ---")
        localization.set_language(lang)
        
        # Create a test property
        test_property = {
            'title': f'Test Property {lang.upper()}',
            'description': f'Description de test en {lang}',
            'price': 250000,
            'property_type': 'house',
            'transaction_type': 'sale',
            'address': '123 Test Street',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'Test Country',
            'bedrooms': 3,
            'bathrooms': 2,
            'area': 120.5,
            'year_built': 2020,
            'features': ['garage', 'garden', 'terrace']
        }
        
        # Create property
        property_id = property_manager.create_property(test_property)
        print(f"✓ Propriété créée avec ID: {property_id}")
        
        # Test duplication
        print(f"\n{localization.translate('btn_duplicate_property')}:")
        duplicated_id = property_manager.duplicate_property(property_id)
        if duplicated_id:
            print(f"✓ {localization.translate('msg_property_duplicated', new_id=duplicated_id)}")
            
            # Verify duplicated property
            original = property_manager.get_property_by_id(property_id)
            duplicate = property_manager.get_property_by_id(duplicated_id)
            
            if original and duplicate:
                print(f"  - Titre original: {original['title']}")
                print(f"  - Titre dupliqué: {duplicate['title']}")
                print(f"  - Prix identique: {original['price'] == duplicate['price']}")
            
        else:
            print(f"✗ {localization.translate('msg_duplicate_error')}")
        
        # Test deletion
        print(f"\n{localization.translate('btn_delete_property')}:")
        
        # Delete original property
        success = property_manager.delete_property_with_media(property_id)
        if success:
            print(f"✓ {localization.translate('msg_property_deleted')} (ID: {property_id})")
            
            # Verify deletion
            deleted_property = property_manager.get_property_by_id(property_id)
            if not deleted_property:
                print("  - Propriété correctement supprimée de la base de données")
            else:
                print("  - ⚠️ Propriété encore présente dans la base de données")
        else:
            print(f"✗ {localization.translate('msg_delete_error')}")
        
        # Delete duplicated property
        if duplicated_id:
            success = property_manager.delete_property_with_media(duplicated_id)
            if success:
                print(f"✓ Propriété dupliquée supprimée (ID: {duplicated_id})")
    
    print("\n=== Test terminé ===")

def test_localization_messages():
    """
    Test localization messages for deletion and duplication
    """
    print("\n=== Test des messages de localisation ===")
    
    localization = LocalizationManager()
    
    messages_to_test = [
        'btn_duplicate_property',
        'btn_delete_property',
        'msg_confirm_delete_property',
        'msg_property_deleted',
        'msg_property_duplicated',
        'msg_delete_error',
        'msg_duplicate_error',
        'msg_no_selection_delete',
        'msg_no_selection_duplicate'
    ]
    
    for lang in ['fr', 'en']:
        print(f"\n--- Messages en {lang.upper()} ---")
        localization.set_language(lang)
        
        for message_key in messages_to_test:
            text = localization.translate(message_key)
            print(f"  {message_key}: {text}")

if __name__ == "__main__":
    try:
        test_localization_messages()
        test_property_deletion_duplication()
        print("\n🎉 Tous les tests sont passés avec succès!")
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()