#!/usr/bin/env python3
"""
Localization manager for HomeShow Desktop application.
Handles French/English language switching.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

class LocalizationManager:
    """
    Manages application localization and language switching.
    """
    
    def __init__(self):
        """
        Initialize localization manager
        """
        self.current_language = 'fr'  # Default to French
        self.translations = {}
        self.locales_dir = Path(__file__).parent.parent / 'locales'
        self.load_translations()
    
    def load_translations(self) -> None:
        """
        Load translation files for all supported languages.
        """
        try:
            # Ensure locales directory exists
            self.locales_dir.mkdir(exist_ok=True)
            
            # Load English translations
            en_file = self.locales_dir / 'en.json'
            if en_file.exists():
                with open(en_file, 'r', encoding='utf-8') as f:
                    self.translations['en'] = json.load(f)
            else:
                self.translations['en'] = self._get_default_english_translations()
                self._save_translations('en')
            
            # Load French translations
            fr_file = self.locales_dir / 'fr.json'
            if fr_file.exists():
                with open(fr_file, 'r', encoding='utf-8') as f:
                    self.translations['fr'] = json.load(f)
            else:
                self.translations['fr'] = self._get_default_french_translations()
                self._save_translations('fr')
                
        except Exception as e:
            print(f"Error loading translations: {e}")
            # Fallback to default translations
            self.translations = {
                'en': self._get_default_english_translations(),
                'fr': self._get_default_french_translations()
            }
    
    def _save_translations(self, language: str) -> None:
        """
        Save translations to file.
        
        Args:
            language: Language code ('en' or 'fr')
        """
        try:
            file_path = self.locales_dir / f'{language}.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.translations[language], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving translations for {language}: {e}")
    
    def set_language(self, language: str) -> None:
        """
        Set the current language.
        
        Args:
            language: Language code ('en' or 'fr')
        """
        if language in self.translations:
            self.current_language = language
        else:
            print(f"Language '{language}' not supported. Using English.")
            self.current_language = 'en'
    
    def get_language(self) -> str:
        """
        Get the current language code.
        
        Returns:
            Current language code
        """
        return self.current_language
    
    def translate(self, key: str, **kwargs) -> str:
        """
        Get translated text for the given key.
        
        Args:
            key: Translation key
            **kwargs: Format parameters for the translation
        
        Returns:
            Translated text
        """
        try:
            # Get translation from current language
            translation = self.translations[self.current_language].get(key)
            
            # Fallback to English if not found
            if translation is None:
                translation = self.translations['en'].get(key, key)
            
            # Format with parameters if provided
            if kwargs:
                return translation.format(**kwargs)
            
            return translation
            
        except Exception as e:
            print(f"Error translating key '{key}': {e}")
            return key
    
    def _get_default_english_translations(self) -> Dict[str, str]:
        """
        Get default English translations.
        
        Returns:
            Dictionary of English translations
        """
        return {
            # Application
            "app_title": "HomeShow Desktop",
            "app_subtitle": "Real Estate Property Management",
            
            # Menu
            "menu_file": "File",
            "menu_new": "New Property",
            "menu_import": "Import Property",
            "menu_export": "Export Property",
            "menu_exit": "Exit",
            "menu_edit": "Edit",
            "menu_preferences": "Preferences",
            "menu_view": "View",
            "menu_tools": "Tools",
            "menu_generate_website": "Generate Website",
            "menu_ai_staging": "AI Virtual Staging",
            "menu_backup_database": "Backup Database",
            "menu_help": "Help",
            "menu_about": "About",
            "menu_language": "Language",
            "menu_english": "English",
            "menu_french": "Français",
            
            # Tabs
            "tab_dashboard": "Dashboard",
            "tab_properties": "Properties",
            "tab_projects": "Projects",
            "tab_templates": "Templates",
            
            # Dashboard
            "dashboard_welcome": "Welcome to HomeShow Desktop",
            "dashboard_subtitle": "Create stunning real estate websites with ease",
            "dashboard_stats": "Property Statistics",
            "dashboard_total_properties": "Total Properties",
            "dashboard_active_listings": "Active Listings",
            "dashboard_websites_generated": "Websites Generated",
            "dashboard_quick_actions": "Quick Actions",
            "dashboard_create_property": "Create New Property",
            "dashboard_new_property": "➕ New Property",
            "dashboard_import_data": "Import Property Data",
            "dashboard_import_property": "📁 Import Property",
            "dashboard_generate_website": "Generate Website",
            "dashboard_ai_staging": "🎨 AI Staging",
            "dashboard_recent_properties": "Recent Properties",
            "dashboard_tips": "Tips & Resources",
            "menu_user_guide": "User Guide",
            
            # Property Wizard
            "wizard_title": "Property Creation Wizard",
            "wizard_create_property": "Create New Property",
            "wizard_edit_property": "Edit Property",
            "wizard_create_property_btn": "Create Property",
            "wizard_update_property": "Update Property",
            "wizard_step": "Step",
            "wizard_of": "of",
            "wizard_step_basic": "Basic Information",
            "wizard_step_media": "Media Upload",
            "wizard_step_features": "Property Features",
            "wizard_step_location": "Location",
            "wizard_step_advanced": "Advanced Options",
            "wizard_step_review": "Review",
            "wizard_next": "Next",
            "wizard_previous": "Previous",
            "wizard_back": "Back",
            "wizard_finish": "Finish",
            "wizard_cancel": "Cancel",
            "wizard_basic_info": "Basic Information",
            "wizard_basic_info_desc": "Enter property details",
            "wizard_media_upload": "Media Upload",
            "wizard_media_upload_desc": "Add photos and videos",
            "wizard_features": "Property Features",
            "wizard_features_desc": "Specify features and amenities",
            "wizard_location": "Location & Neighborhood",
            "wizard_location_desc": "Location details and area info",
            "wizard_advanced": "Advanced Options",
            "wizard_advanced_desc": "Additional settings and options",
            "wizard_review": "Review & Create",
            "wizard_review_desc": "Review and finalize property",
            
            # Property Fields
            "property_title": "Property Title",
            "property_description": "Description",
            "property_price": "Price",
            "property_type": "Property Type",
            "property_bedrooms": "Bedrooms",
            "property_bathrooms": "Bathrooms",
            "property_area": "Area (sq ft)",
            "property_address": "Address",
            "property_city": "City",
            "property_state": "State/Province",
            "property_zip": "ZIP/Postal Code",
            "property_country": "Country",
            
            # Buttons
            "btn_save": "Save",
            "btn_cancel": "Cancel",
            "btn_delete": "Delete",
            "btn_edit": "Edit",
            "btn_view": "View",
            "btn_browse": "Browse",
            "btn_add": "Add",
            "btn_remove": "Remove",
            "btn_generate": "Generate",
            "btn_export": "Export",
            "btn_import": "Import",
            "btn_duplicate": "Duplicate",
            "btn_new_property": "New Property",
            "btn_edit_property": "Edit Property",
            "btn_delete_property": "Delete Property",
            "btn_duplicate_property": "Duplicate Property",
            "btn_generate_website": "Generate Website",
            "btn_refresh": "Refresh",
            
            # Messages
            "msg_success": "Operation completed successfully",
            "msg_error": "An error occurred",
            "msg_confirm_delete": "Are you sure you want to delete this item?",
            "msg_confirm_delete_property": "Are you sure you want to delete property '{title}'?\n\nThis action cannot be undone and will remove all associated media files.",
            "msg_property_deleted": "Property deleted successfully",
            "msg_property_duplicated": "Property duplicated successfully (New ID: {new_id})",
            "msg_delete_error": "Failed to delete property",
            "msg_duplicate_error": "Failed to duplicate property",
            "msg_no_selection": "Please select a property",
            "msg_no_selection_edit": "Please select a property to edit",
            "msg_no_selection_delete": "Please select a property to delete",
            "msg_no_selection_duplicate": "Please select a property to duplicate",
            "msg_no_properties": "No properties found",
            "msg_loading": "Loading...",
            "msg_saving": "Saving...",
            "msg_generating": "Generating website...",
            
            # Website Generation
            "website_title": "Website Generation",
            "website_template": "Template",
            "website_options": "Options",
            "website_output": "Output Directory",
            "website_generated": "Website generated successfully!",
            
            # Status
            "status_ready": "Ready",
            "status_processing": "Processing...",
            "status_complete": "Complete",
            "status_error": "Error",
            
            # Property Types
            "property_type_house": "House",
            "property_type_apartment": "Apartment",
            "property_type_condo": "Condominium",
            "property_type_villa": "Villa",
            "property_type_studio": "Studio",
            "property_type_commercial": "Commercial",
            "property_type_land": "Land",
            
            # Transaction Types
            "transaction_sale": "For Sale",
            "transaction_rent": "For Rent",
            "transaction_rent_furnished": "For Rent (Furnished)",
            "transaction_rent_unfurnished": "For Rent (Unfurnished)",
            
            # Features - General
            "feature_parking": "Parking",
            "feature_garage": "Garage",
            "feature_garden": "Garden",
            "feature_terrace": "Terrace",
            "feature_balcony": "Balcony",
            "feature_pool": "Swimming Pool",
            "feature_elevator": "Elevator",
            "feature_security": "Security System",
            "feature_air_conditioning": "Air Conditioning",
            "feature_heating": "Heating",
            "feature_fireplace": "Fireplace",
            
            # Features - Rental Specific
            "feature_washing_machine": "Washing Machine",
            "feature_dishwasher": "Dishwasher",
            "feature_wifi": "WiFi Internet",
            "feature_tv": "Television",
            "feature_furnished": "Furnished",
            "feature_utilities_included": "Utilities Included",
            "feature_pets_allowed": "Pets Allowed",
            "feature_smoking_allowed": "Smoking Allowed",
            
            # Features - Sale Specific
            "feature_new_construction": "New Construction",
            "feature_renovated": "Recently Renovated",
            "feature_investment_property": "Investment Property",
            "feature_mortgage_available": "Mortgage Available",
        }
    
    def _get_default_french_translations(self) -> Dict[str, str]:
        """
        Get default French translations.
        
        Returns:
            Dictionary of French translations
        """
        return {
            # Application
            "app_title": "HomeShow Desktop",
            "app_subtitle": "Gestion de Propriétés Immobilières",
            
            # Menu
            "menu_file": "Fichier",
            "menu_new": "Nouvelle Propriété",
            "menu_import": "Importer Propriété",
            "menu_export": "Exporter Propriété",
            "menu_exit": "Quitter",
            "menu_edit": "Édition",
            "menu_preferences": "Préférences",
            "menu_view": "Affichage",
            "menu_tools": "Outils",
            "menu_generate_website": "Générer Site Web",
            "menu_ai_staging": "Mise en Scène IA",
            "menu_backup_database": "Sauvegarder Base de Données",
            "menu_help": "Aide",
            "menu_about": "À Propos",
            "menu_language": "Langue",
            "menu_english": "English",
            "menu_french": "Français",
            
            # Tabs
            "tab_dashboard": "Tableau de Bord",
            "tab_properties": "Propriétés",
            "tab_projects": "Projets",
            "tab_templates": "Modèles",
            
            # Dashboard
            "dashboard_welcome": "Bienvenue dans HomeShow Desktop",
            "dashboard_subtitle": "Créez de superbes sites web immobiliers en toute simplicité",
            "dashboard_stats": "Statistiques des Propriétés",
            "dashboard_total_properties": "Total des Propriétés",
            "dashboard_active_listings": "Annonces Actives",
            "dashboard_websites_generated": "Sites Web Générés",
            "dashboard_quick_actions": "Actions Rapides",
            "dashboard_create_property": "Créer une Nouvelle Propriété",
            "dashboard_new_property": "➕ Nouvelle Propriété",
            "dashboard_import_data": "Importer des Données de Propriété",
            "dashboard_import_property": "📁 Importer Propriété",
            "dashboard_generate_website": "Générer un Site Web",
            "dashboard_ai_staging": "🎨 Mise en Scène IA",
            "dashboard_recent_properties": "Propriétés Récentes",
            "dashboard_tips": "Conseils et Ressources",
            "menu_user_guide": "Guide Utilisateur",
            
            # Property Wizard
            "wizard_title": "Assistant de Création de Propriété",
            "wizard_create_property": "Créer une Nouvelle Propriété",
            "wizard_edit_property": "Modifier la Propriété",
            "wizard_create_property_btn": "Créer la Propriété",
            "wizard_update_property": "Mettre à Jour la Propriété",
            "wizard_step": "Étape",
            "wizard_of": "de",
            "wizard_step_basic": "Informations de Base",
            "wizard_step_media": "Téléchargement Média",
            "wizard_step_features": "Caractéristiques",
            "wizard_step_location": "Localisation",
            "wizard_step_advanced": "Options Avancées",
            "wizard_step_review": "Révision",
            "wizard_next": "Suivant",
            "wizard_previous": "Précédent",
            "wizard_back": "Retour",
            "wizard_finish": "Terminer",
            "wizard_cancel": "Annuler",
            "wizard_basic_info": "Informations de Base",
            "wizard_basic_info_desc": "Entrer les détails de la propriété",
            "wizard_media_upload": "Téléchargement Média",
            "wizard_media_upload_desc": "Ajouter photos et vidéos",
            "wizard_features": "Caractéristiques de la Propriété",
            "wizard_features_desc": "Spécifier les caractéristiques et commodités",
            "wizard_location": "Localisation et Quartier",
            "wizard_location_desc": "Détails de localisation et infos de zone",
            "wizard_advanced": "Options Avancées",
            "wizard_advanced_desc": "Paramètres et options supplémentaires",
            "wizard_review": "Révision et Création",
            "wizard_review_desc": "Réviser et finaliser la propriété",
            
            # Property Fields
            "property_title": "Titre de la Propriété",
            "property_description": "Description",
            "property_price": "Prix",
            "property_type": "Type de Propriété",
            "property_bedrooms": "Chambres",
            "property_bathrooms": "Salles de Bain",
            "property_area": "Superficie (pi²)",
            "property_address": "Adresse",
            "property_city": "Ville",
            "property_state": "Province/État",
            "property_zip": "Code Postal",
            "property_country": "Pays",
            
            # Buttons
            "btn_save": "Enregistrer",
            "btn_cancel": "Annuler",
            "btn_delete": "Supprimer",
            "btn_edit": "Modifier",
            "btn_view": "Voir",
            "btn_browse": "Parcourir",
            "btn_add": "Ajouter",
            "btn_remove": "Retirer",
            "btn_generate": "Générer",
            "btn_export": "Exporter",
            "btn_import": "Importer",
            "btn_duplicate": "Dupliquer",
            "btn_new_property": "Nouvelle Propriété",
            "btn_edit_property": "Modifier Propriété",
            "btn_delete_property": "Supprimer Propriété",
            "btn_duplicate_property": "Dupliquer Propriété",
            "btn_generate_website": "Générer Site Web",
            "btn_refresh": "Actualiser",
            
            # Messages
            "msg_success": "Opération terminée avec succès",
            "msg_error": "Une erreur s'est produite",
            "msg_confirm_delete": "Êtes-vous sûr de vouloir supprimer cet élément ?",
            "msg_confirm_delete_property": "Êtes-vous sûr de vouloir supprimer la propriété '{title}' ?\n\nCette action est irréversible et supprimera tous les fichiers média associés.",
            "msg_property_deleted": "Propriété supprimée avec succès",
            "msg_property_duplicated": "Propriété dupliquée avec succès (Nouvel ID: {new_id})",
            "msg_delete_error": "Échec de la suppression de la propriété",
            "msg_duplicate_error": "Échec de la duplication de la propriété",
            "msg_no_selection": "Veuillez sélectionner une propriété",
            "msg_no_selection_edit": "Veuillez sélectionner une propriété à modifier",
            "msg_no_selection_delete": "Veuillez sélectionner une propriété à supprimer",
            "msg_no_selection_duplicate": "Veuillez sélectionner une propriété à dupliquer",
            "msg_no_properties": "Aucune propriété trouvée",
            "msg_loading": "Chargement...",
            "msg_saving": "Enregistrement...",
            "msg_generating": "Génération du site web...",
            
            # Website Generation
            "website_title": "Génération de Site Web",
            "website_template": "Modèle",
            "website_options": "Options",
            "website_output": "Répertoire de Sortie",
            "website_generated": "Site web généré avec succès!",
            
            # Status
            "status_ready": "Prêt",
            "status_processing": "Traitement...",
            "status_complete": "Terminé",
            "status_error": "Erreur",
            
            # Property Types
            "property_type_house": "Maison",
            "property_type_apartment": "Appartement",
            "property_type_condo": "Copropriété",
            "property_type_villa": "Villa",
            "property_type_studio": "Studio",
            "property_type_commercial": "Commercial",
            "property_type_land": "Terrain",
            
            # Transaction Types
            "transaction_sale": "À Vendre",
            "transaction_rent": "À Louer",
            "transaction_rent_furnished": "À Louer (Meublé)",
            "transaction_rent_unfurnished": "À Louer (Non Meublé)",
            
            # Features - General
            "feature_parking": "Parking",
            "feature_garage": "Garage",
            "feature_garden": "Jardin",
            "feature_terrace": "Terrasse",
            "feature_balcony": "Balcon",
            "feature_pool": "Piscine",
            "feature_elevator": "Ascenseur",
            "feature_security": "Système de Sécurité",
            "feature_air_conditioning": "Climatisation",
            "feature_heating": "Chauffage",
            "feature_fireplace": "Cheminée",
            
            # Features - Rental Specific
            "feature_washing_machine": "Machine à Laver",
            "feature_dishwasher": "Lave-vaisselle",
            "feature_wifi": "Internet WiFi",
            "feature_tv": "Télévision",
            "feature_furnished": "Meublé",
            "feature_utilities_included": "Charges Comprises",
            "feature_pets_allowed": "Animaux Autorisés",
            "feature_smoking_allowed": "Fumeurs Autorisés",
            
            # Features - Sale Specific
            "feature_new_construction": "Construction Neuve",
            "feature_renovated": "Récemment Rénové",
            "feature_investment_property": "Propriété d'Investissement",
            "feature_mortgage_available": "Prêt Hypothécaire Disponible",
        }

# Global localization manager instance
_localization_manager = None

def get_localization_manager() -> LocalizationManager:
    """
    Get the global localization manager instance.
    
    Returns:
        LocalizationManager instance
    """
    global _localization_manager
    if _localization_manager is None:
        _localization_manager = LocalizationManager()
    return _localization_manager

def translate(key: str, **kwargs) -> str:
    """
    Convenience function to translate a key.
    
    Args:
        key: Translation key
        **kwargs: Format parameters
    
    Returns:
        Translated text
    """
    return get_localization_manager().translate(key, **kwargs)

def set_language(language: str) -> None:
    """
    Convenience function to set the language.
    
    Args:
        language: Language code ('en' or 'fr')
    """
    get_localization_manager().set_language(language)

def get_language() -> str:
    """
    Convenience function to get the current language.
    
    Returns:
        Current language code
    """
    return get_localization_manager().get_language()