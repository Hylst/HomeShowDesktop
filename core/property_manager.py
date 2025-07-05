#!/usr/bin/env python3
"""
Property Manager for HomeShow Desktop
Handles business logic for property management operations

Author: AI Assistant
Version: 1.0.0
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime

from .database import DatabaseManager
from .media_handler import MediaHandler

class PropertyManager:
    """
    Manages property-related business logic and operations
    """
    
    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize property manager
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager or DatabaseManager()
        self.media_handler = MediaHandler()
        self.project_root = Path(__file__).parent.parent
        self.projects_dir = self.project_root / "data" / "projects"
        
        # Ensure projects directory exists
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def create_property(self, property_data: Dict[str, Any]) -> int:
        """
        Create a new property without media files
        
        Args:
            property_data: Property information
            
        Returns:
            Property ID
        """
        return self.db_manager.create_property(property_data)
    
    def create_property_with_media(self, property_data: Dict[str, Any], 
                                 media_files: List[str] = None) -> Tuple[int, str]:
        """
        Create a new property with associated media files
        
        Args:
            property_data: Property information
            media_files: List of media file paths to copy
            
        Returns:
            Tuple of (property_id, media_directory_path)
        """
        # Create property in database
        property_id = self.db_manager.create_property(property_data)
        
        # Create media directory for this property
        media_dir = self.projects_dir / f"property_{property_id}" / "media"
        media_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy and process media files
        processed_media = []
        if media_files:
            for file_path in media_files:
                if os.path.exists(file_path):
                    try:
                        # Copy file to media directory
                        filename = os.path.basename(file_path)
                        destination = media_dir / filename
                        shutil.copy2(file_path, destination)
                        
                        # Process image if needed (optimization, thumbnails)
                        if self.media_handler.is_image(file_path):
                            processed_file = self.media_handler.process_image(
                                str(destination), str(media_dir)
                            )
                            processed_media.append({
                                'type': 'image',
                                'original': str(destination.relative_to(self.project_root)),
                                'processed': processed_file,
                                'filename': filename
                            })
                        else:
                            processed_media.append({
                                'type': 'other',
                                'path': str(destination.relative_to(self.project_root)),
                                'filename': filename
                            })
                    except Exception as e:
                        print(f"Error processing media file {file_path}: {e}")
        
        # Update property with media file information
        if processed_media:
            property_data['media_files'] = processed_media
            self.db_manager.update_property(property_id, property_data)
        
        return property_id, str(media_dir)
    
    def update_property_media(self, property_id: int, 
                            new_media_files: List[str] = None) -> bool:
        """
        Update media files for an existing property
        
        Args:
            property_id: Property ID
            new_media_files: List of new media file paths
            
        Returns:
            True if successful, False otherwise
        """
        property_data = self.db_manager.get_property(property_id)
        if not property_data:
            return False
        
        media_dir = self.projects_dir / f"property_{property_id}" / "media"
        media_dir.mkdir(parents=True, exist_ok=True)
        
        # Get existing media files
        existing_media = property_data.get('media_files', [])
        
        # Process new media files
        if new_media_files:
            for file_path in new_media_files:
                if os.path.exists(file_path):
                    try:
                        filename = os.path.basename(file_path)
                        destination = media_dir / filename
                        shutil.copy2(file_path, destination)
                        
                        if self.media_handler.is_image(file_path):
                            processed_file = self.media_handler.process_image(
                                str(destination), str(media_dir)
                            )
                            existing_media.append({
                                'type': 'image',
                                'original': str(destination.relative_to(self.project_root)),
                                'processed': processed_file,
                                'filename': filename
                            })
                        else:
                            existing_media.append({
                                'type': 'other',
                                'path': str(destination.relative_to(self.project_root)),
                                'filename': filename
                            })
                    except Exception as e:
                        print(f"Error processing media file {file_path}: {e}")
        
        # Update property with new media information
        property_data['media_files'] = existing_media
        return self.db_manager.update_property(property_id, property_data)
    
    def remove_media_file(self, property_id: int, filename: str) -> bool:
        """
        Remove a media file from a property
        
        Args:
            property_id: Property ID
            filename: Name of file to remove
            
        Returns:
            True if successful, False otherwise
        """
        property_data = self.db_manager.get_property(property_id)
        if not property_data:
            return False
        
        media_files = property_data.get('media_files', [])
        
        # Remove file from list and filesystem
        updated_media = []
        for media in media_files:
            if media.get('filename') != filename:
                updated_media.append(media)
            else:
                # Remove physical file
                try:
                    if media.get('type') == 'image':
                        # Remove original and processed files
                        original_path = self.project_root / media.get('original', '')
                        if original_path.exists():
                            original_path.unlink()
                        
                        processed_info = media.get('processed', {})
                        if isinstance(processed_info, dict):
                            for size, path in processed_info.items():
                                processed_path = self.project_root / path
                                if processed_path.exists():
                                    processed_path.unlink()
                    else:
                        file_path = self.project_root / media.get('path', '')
                        if file_path.exists():
                            file_path.unlink()
                except Exception as e:
                    print(f"Error removing file {filename}: {e}")
        
        # Update property
        property_data['media_files'] = updated_media
        return self.db_manager.update_property(property_id, property_data)
    
    def get_property_by_id(self, property_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a property by its ID
        
        Args:
            property_id: Property ID
            
        Returns:
            Property data dictionary or None if not found
        """
        return self.db_manager.get_property(property_id)
    
    def update_property(self, property_id: int, property_data: Dict[str, Any]) -> bool:
        """
        Update an existing property
        
        Args:
            property_id: Property ID
            property_data: Updated property information
            
        Returns:
            True if successful, False otherwise
        """
        return self.db_manager.update_property(property_id, property_data)
    
    def delete_property(self, property_id: int) -> bool:
        """
        Delete a property from the database
        
        Args:
            property_id: Property ID
            
        Returns:
            True if successful, False otherwise
        """
        return self.db_manager.delete_property(property_id)
    
    def get_property_summary(self, property_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a summary of property information for display
        
        Args:
            property_id: Property ID
            
        Returns:
            Property summary dictionary
        """
        property_data = self.db_manager.get_property(property_id)
        if not property_data:
            return None
        
        # Calculate summary statistics
        media_count = len(property_data.get('media_files', []))
        image_count = sum(1 for media in property_data.get('media_files', []) 
                         if media.get('type') == 'image')
        
        # Get primary image (first image in the list)
        primary_image = None
        for media in property_data.get('media_files', []):
            if media.get('type') == 'image':
                processed = media.get('processed', {})
                if isinstance(processed, dict) and 'thumbnail' in processed:
                    primary_image = processed['thumbnail']
                else:
                    primary_image = media.get('original')
                break
        
        return {
            'id': property_data['id'],
            'title': property_data['title'],
            'property_type': property_data['property_type'],
            'price': property_data['price'],
            'currency': property_data['currency'],
            'surface_area': property_data['surface_area'],
            'rooms': property_data['rooms'],
            'bedrooms': property_data['bedrooms'],
            'bathrooms': property_data['bathrooms'],
            'city': property_data['city'],
            'status': property_data['status'],
            'media_count': media_count,
            'image_count': image_count,
            'primary_image': primary_image,
            'created_at': property_data['created_at'],
            'updated_at': property_data['updated_at']
        }
    
    def get_all_property_summaries(self) -> List[Dict[str, Any]]:
        """
        Get summaries of all properties
        
        Returns:
            List of property summary dictionaries
        """
        properties = self.db_manager.get_all_properties()
        summaries = []
        
        for property_data in properties:
            summary = self.get_property_summary(property_data['id'])
            if summary:
                summaries.append(summary)
        
        return summaries
    
    def get_filtered_properties(self, filters: Dict[str, Any] = None, 
                              sort_column: str = "updated_at", 
                              sort_direction: str = "desc") -> List[Dict[str, Any]]:
        """
        Get filtered and sorted properties
        
        Args:
            filters: Dictionary of filters to apply
            sort_column: Column to sort by
            sort_direction: Sort direction (asc/desc)
            
        Returns:
            List of filtered property summaries
        """
        # Get all properties
        properties = self.get_all_property_summaries()
        
        # Apply filters if provided
        if filters:
            filtered_properties = []
            
            for prop in properties:
                include_property = True
                
                # Search filter (searches in title, description, city)
                if 'search' in filters and filters['search']:
                    search_term = filters['search'].lower()
                    searchable_text = f"{prop.get('title', '')} {prop.get('city', '')}".lower()
                    if search_term not in searchable_text:
                        include_property = False
                
                # Property type filter
                if 'property_type' in filters and filters['property_type']:
                    if prop.get('property_type', '').lower() != filters['property_type'].lower():
                        include_property = False
                
                # Price range filters
                if 'min_price' in filters and filters['min_price'] is not None:
                    prop_price = prop.get('price', 0) or 0
                    if prop_price < filters['min_price']:
                        include_property = False
                
                if 'max_price' in filters and filters['max_price'] is not None:
                    prop_price = prop.get('price', 0) or 0
                    if prop_price > filters['max_price']:
                        include_property = False
                
                # City filter
                if 'city' in filters and filters['city']:
                    prop_city = prop.get('city', '').lower()
                    filter_city = filters['city'].lower()
                    if filter_city not in prop_city:
                        include_property = False
                
                # Status filter
                if 'status' in filters and filters['status']:
                    if prop.get('status', '').lower() != filters['status'].lower():
                        include_property = False
                
                if include_property:
                    filtered_properties.append(prop)
            
            properties = filtered_properties
        
        # Apply sorting
        if sort_column and properties:
            reverse_sort = sort_direction.lower() == 'desc'
            
            # Define sort key function
            def sort_key(prop):
                value = prop.get(sort_column)
                
                # Handle different data types
                if value is None:
                    return '' if sort_column in ['title', 'city', 'property_type', 'status'] else 0
                
                if sort_column in ['price', 'surface_area', 'bedrooms', 'bathrooms', 'rooms']:
                    try:
                        return float(value) if value else 0
                    except (ValueError, TypeError):
                        return 0
                
                if sort_column in ['updated_at', 'created_at']:
                    try:
                        return datetime.fromisoformat(value.replace('Z', '+00:00')) if value else datetime.min
                    except (ValueError, TypeError):
                        return datetime.min
                
                return str(value).lower() if value else ''
            
            properties.sort(key=sort_key, reverse=reverse_sort)
        
        return properties
    
    def duplicate_property(self, property_id: int, new_title: str = None) -> Optional[int]:
        """
        Create a duplicate of an existing property
        
        Args:
            property_id: ID of property to duplicate
            new_title: New title for duplicated property
            
        Returns:
            ID of new property or None if failed
        """
        original_property = self.db_manager.get_property(property_id)
        if not original_property:
            return None
        
        # Prepare new property data
        new_property_data = original_property.copy()
        del new_property_data['id']  # Remove ID to create new record
        del new_property_data['created_at']
        del new_property_data['updated_at']
        
        # Update title
        if new_title:
            new_property_data['title'] = new_title
        else:
            new_property_data['title'] = f"{original_property['title']} (Copy)"
        
        # Reset status to draft
        new_property_data['status'] = 'draft'
        
        # Create new property
        new_property_id = self.db_manager.create_property(new_property_data)
        
        # Copy media files
        original_media_dir = self.projects_dir / f"property_{property_id}" / "media"
        new_media_dir = self.projects_dir / f"property_{new_property_id}" / "media"
        
        if original_media_dir.exists():
            try:
                shutil.copytree(original_media_dir, new_media_dir)
                
                # Update media file paths in new property
                media_files = new_property_data.get('media_files', [])
                updated_media = []
                
                for media in media_files:
                    updated_media_item = media.copy()
                    if media.get('type') == 'image':
                        # Update paths to point to new property directory
                        original_path = media.get('original', '')
                        updated_media_item['original'] = original_path.replace(
                            f"property_{property_id}", f"property_{new_property_id}"
                        )
                        
                        processed = media.get('processed', {})
                        if isinstance(processed, dict):
                            updated_processed = {}
                            for size, path in processed.items():
                                updated_processed[size] = path.replace(
                                    f"property_{property_id}", f"property_{new_property_id}"
                                )
                            updated_media_item['processed'] = updated_processed
                    else:
                        path = media.get('path', '')
                        updated_media_item['path'] = path.replace(
                            f"property_{property_id}", f"property_{new_property_id}"
                        )
                    
                    updated_media.append(updated_media_item)
                
                # Update property with corrected media paths
                new_property_data['media_files'] = updated_media
                self.db_manager.update_property(new_property_id, new_property_data)
                
            except Exception as e:
                print(f"Error copying media files: {e}")
        
        return new_property_id
    
    def delete_property_with_media(self, property_id: int) -> bool:
        """
        Delete a property and all associated media files
        
        Args:
            property_id: Property ID
            
        Returns:
            True if successful, False otherwise
        """
        # Remove media directory
        property_dir = self.projects_dir / f"property_{property_id}"
        if property_dir.exists():
            try:
                shutil.rmtree(property_dir)
            except Exception as e:
                print(f"Error removing property directory: {e}")
        
        # Delete from database
        return self.db_manager.delete_property(property_id)
    
    def export_property_data(self, property_id: int, export_path: str) -> bool:
        """
        Export property data and media to a specified location
        
        Args:
            property_id: Property ID
            export_path: Destination path for export
            
        Returns:
            True if successful, False otherwise
        """
        property_data = self.db_manager.get_property(property_id)
        if not property_data:
            return False
        
        try:
            export_dir = Path(export_path)
            export_dir.mkdir(parents=True, exist_ok=True)
            
            # Export property data as JSON
            import json
            data_file = export_dir / "property_data.json"
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(property_data, f, indent=2, ensure_ascii=False, default=str)
            
            # Copy media files
            property_media_dir = self.projects_dir / f"property_{property_id}" / "media"
            if property_media_dir.exists():
                export_media_dir = export_dir / "media"
                shutil.copytree(property_media_dir, export_media_dir, dirs_exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"Error exporting property data: {e}")
            return False
    
    def import_property_data(self, import_path: str) -> Optional[int]:
        """
        Import property data from an exported directory
        
        Args:
            import_path: Path to exported property directory
            
        Returns:
            ID of imported property or None if failed
        """
        try:
            import_dir = Path(import_path)
            data_file = import_dir / "property_data.json"
            
            if not data_file.exists():
                return None
            
            # Load property data
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                property_data = json.load(f)
            
            # Remove ID and timestamps to create new record
            if 'id' in property_data:
                del property_data['id']
            if 'created_at' in property_data:
                del property_data['created_at']
            if 'updated_at' in property_data:
                del property_data['updated_at']
            
            # Create new property
            property_id = self.db_manager.create_property(property_data)
            
            # Copy media files
            import_media_dir = import_dir / "media"
            if import_media_dir.exists():
                property_media_dir = self.projects_dir / f"property_{property_id}" / "media"
                shutil.copytree(import_media_dir, property_media_dir, dirs_exist_ok=True)
            
            return property_id
            
        except Exception as e:
            print(f"Error importing property data: {e}")
            return None
    
    def get_property_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about all properties
        
        Returns:
            Dictionary containing various statistics
        """
        properties = self.db_manager.get_all_properties()
        
        if not properties:
            return {
                'total_properties': 0,
                'by_type': {},
                'by_status': {},
                'total_value': 0,
                'average_price': 0,
                'total_media_files': 0
            }
        
        # Calculate statistics
        total_properties = len(properties)
        by_type = {}
        by_status = {}
        total_value = 0
        total_media_files = 0
        
        for prop in properties:
            # Count by type
            prop_type = prop.get('property_type', 'Unknown')
            by_type[prop_type] = by_type.get(prop_type, 0) + 1
            
            # Count by status
            status = prop.get('status', 'Unknown')
            by_status[status] = by_status.get(status, 0) + 1
            
            # Sum values
            price = prop.get('price', 0) or 0
            total_value += price
            
            # Count media files
            media_files = prop.get('media_files', [])
            total_media_files += len(media_files)
        
        average_price = total_value / total_properties if total_properties > 0 else 0
        
        return {
            'total_properties': total_properties,
            'by_type': by_type,
            'by_status': by_status,
            'total_value': total_value,
            'average_price': average_price,
            'total_media_files': total_media_files
        }