#!/usr/bin/env python3
"""
Database Manager for HomeShow Desktop
Handles SQLite database operations for property management

Author: AI Assistant
Version: 1.0.0
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

class DatabaseManager:
    """
    Manages SQLite database operations for property data
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "database.db"
        
        self.db_path = str(db_path)
        self.connection = None
    
    def connect(self) -> sqlite3.Connection:
        """
        Create database connection
        
        Returns:
            SQLite connection object
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """
        Close database connection
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """
        Create database tables if they don't exist
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Properties table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                property_type TEXT NOT NULL,
                price REAL,
                currency TEXT DEFAULT 'EUR',
                surface_area REAL,
                rooms INTEGER,
                bedrooms INTEGER,
                bathrooms INTEGER,
                address TEXT,
                city TEXT,
                postal_code TEXT,
                country TEXT,
                latitude REAL,
                longitude REAL,
                features TEXT, -- JSON string
                amenities TEXT, -- JSON string
                media_files TEXT, -- JSON string
                floor_plan TEXT, -- JSON string
                virtual_staging BOOLEAN DEFAULT 0,
                template_id TEXT,
                status TEXT DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                preview_image TEXT,
                config TEXT, -- JSON string
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                property_id INTEGER,
                template_id TEXT,
                output_path TEXT,
                config TEXT, -- JSON string
                status TEXT DEFAULT 'created',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties (id),
                FOREIGN KEY (template_id) REFERENCES templates (id)
            )
        """)
        
        # Insert default templates
        self._insert_default_templates(cursor)
        
        conn.commit()
        print("Database initialized successfully.")
    
    def _insert_default_templates(self, cursor):
        """
        Insert default website templates
        
        Args:
            cursor: Database cursor
        """
        default_templates = [
            {
                'id': 'modern',
                'name': 'Modern',
                'description': 'Clean and contemporary design with minimalist aesthetics',
                'category': 'residential',
                'config': json.dumps({
                    'color_scheme': 'light',
                    'layout': 'grid',
                    'animations': True,
                    'responsive': True
                })
            },
            {
                'id': 'luxury',
                'name': 'Luxury',
                'description': 'Elegant and sophisticated design for high-end properties',
                'category': 'luxury',
                'config': json.dumps({
                    'color_scheme': 'dark',
                    'layout': 'fullscreen',
                    'animations': True,
                    'responsive': True
                })
            },
            {
                'id': 'minimal',
                'name': 'Minimal',
                'description': 'Simple and clean design focusing on content',
                'category': 'residential',
                'config': json.dumps({
                    'color_scheme': 'light',
                    'layout': 'single_column',
                    'animations': False,
                    'responsive': True
                })
            },
            {
                'id': 'bold',
                'name': 'Bold',
                'description': 'Eye-catching design with vibrant colors and dynamic layouts',
                'category': 'commercial',
                'config': json.dumps({
                    'color_scheme': 'colorful',
                    'layout': 'masonry',
                    'animations': True,
                    'responsive': True
                })
            }
        ]
        
        for template in default_templates:
            cursor.execute("""
                INSERT OR IGNORE INTO templates 
                (id, name, description, category, config)
                VALUES (?, ?, ?, ?, ?)
            """, (
                template['id'],
                template['name'],
                template['description'],
                template['category'],
                template['config']
            ))
    
    def create_property(self, property_data: Dict[str, Any]) -> int:
        """
        Create a new property record
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            ID of the created property
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Convert lists/dicts to JSON strings
        features = json.dumps(property_data.get('features', []))
        amenities = json.dumps(property_data.get('amenities', []))
        media_files = json.dumps(property_data.get('media_files', []))
        floor_plan = json.dumps(property_data.get('floor_plan', {}))
        
        cursor.execute("""
            INSERT INTO properties (
                title, description, property_type, price, currency,
                surface_area, rooms, bedrooms, bathrooms,
                address, city, postal_code, country,
                latitude, longitude, features, amenities,
                media_files, floor_plan, virtual_staging,
                template_id, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            property_data.get('title'),
            property_data.get('description'),
            property_data.get('property_type'),
            property_data.get('price'),
            property_data.get('currency', 'EUR'),
            property_data.get('surface_area'),
            property_data.get('rooms'),
            property_data.get('bedrooms'),
            property_data.get('bathrooms'),
            property_data.get('address'),
            property_data.get('city'),
            property_data.get('postal_code'),
            property_data.get('country'),
            property_data.get('latitude'),
            property_data.get('longitude'),
            features,
            amenities,
            media_files,
            floor_plan,
            property_data.get('virtual_staging', False),
            property_data.get('template_id'),
            property_data.get('status', 'draft')
        ))
        
        property_id = cursor.lastrowid
        conn.commit()
        
        return property_id
    
    def get_property(self, property_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a property by ID
        
        Args:
            property_id: Property ID
            
        Returns:
            Property data dictionary or None if not found
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
        row = cursor.fetchone()
        
        if row:
            property_data = dict(row)
            # Parse JSON fields
            property_data['features'] = json.loads(property_data['features'] or '[]')
            property_data['amenities'] = json.loads(property_data['amenities'] or '[]')
            property_data['media_files'] = json.loads(property_data['media_files'] or '[]')
            property_data['floor_plan'] = json.loads(property_data['floor_plan'] or '{}')
            return property_data
        
        return None
    
    def get_all_properties(self) -> List[Dict[str, Any]]:
        """
        Retrieve all properties
        
        Returns:
            List of property dictionaries
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM properties ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        
        properties = []
        for row in rows:
            property_data = dict(row)
            # Parse JSON fields
            property_data['features'] = json.loads(property_data['features'] or '[]')
            property_data['amenities'] = json.loads(property_data['amenities'] or '[]')
            property_data['media_files'] = json.loads(property_data['media_files'] or '[]')
            property_data['floor_plan'] = json.loads(property_data['floor_plan'] or '{}')
            properties.append(property_data)
        
        return properties
    
    def update_property(self, property_id: int, property_data: Dict[str, Any]) -> bool:
        """
        Update an existing property
        
        Args:
            property_id: Property ID
            property_data: Updated property data
            
        Returns:
            True if successful, False otherwise
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Convert lists/dicts to JSON strings
        features = json.dumps(property_data.get('features', []))
        amenities = json.dumps(property_data.get('amenities', []))
        media_files = json.dumps(property_data.get('media_files', []))
        floor_plan = json.dumps(property_data.get('floor_plan', {}))
        
        cursor.execute("""
            UPDATE properties SET
                title = ?, description = ?, property_type = ?, price = ?,
                currency = ?, surface_area = ?, rooms = ?, bedrooms = ?,
                bathrooms = ?, address = ?, city = ?, postal_code = ?,
                country = ?, latitude = ?, longitude = ?, features = ?,
                amenities = ?, media_files = ?, floor_plan = ?,
                virtual_staging = ?, template_id = ?, status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            property_data.get('title'),
            property_data.get('description'),
            property_data.get('property_type'),
            property_data.get('price'),
            property_data.get('currency', 'EUR'),
            property_data.get('surface_area'),
            property_data.get('rooms'),
            property_data.get('bedrooms'),
            property_data.get('bathrooms'),
            property_data.get('address'),
            property_data.get('city'),
            property_data.get('postal_code'),
            property_data.get('country'),
            property_data.get('latitude'),
            property_data.get('longitude'),
            features,
            amenities,
            media_files,
            floor_plan,
            property_data.get('virtual_staging', False),
            property_data.get('template_id'),
            property_data.get('status', 'draft'),
            property_id
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        
        return success
    
    def delete_property(self, property_id: int) -> bool:
        """
        Delete a property
        
        Args:
            property_id: Property ID
            
        Returns:
            True if successful, False otherwise
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        
        return success
    
    def get_templates(self) -> List[Dict[str, Any]]:
        """
        Retrieve all available templates
        
        Returns:
            List of template dictionaries
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM templates ORDER BY name")
        rows = cursor.fetchall()
        
        templates = []
        for row in rows:
            template_data = dict(row)
            template_data['config'] = json.loads(template_data['config'] or '{}')
            templates.append(template_data)
        
        return templates
    
    def create_project(self, project_data: Dict[str, Any]) -> int:
        """
        Create a new project
        
        Args:
            project_data: Project information
            
        Returns:
            ID of the created project
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        config = json.dumps(project_data.get('config', {}))
        
        cursor.execute("""
            INSERT INTO projects (
                name, description, property_id, template_id,
                output_path, config, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            project_data.get('name'),
            project_data.get('description'),
            project_data.get('property_id'),
            project_data.get('template_id'),
            project_data.get('output_path'),
            config,
            project_data.get('status', 'created')
        ))
        
        project_id = cursor.lastrowid
        conn.commit()
        
        return project_id
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Retrieve all projects
        
        Returns:
            List of project dictionaries
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.*, pr.title as property_title, t.name as template_name
            FROM projects p
            LEFT JOIN properties pr ON p.property_id = pr.id
            LEFT JOIN templates t ON p.template_id = t.id
            ORDER BY p.updated_at DESC
        """)
        rows = cursor.fetchall()
        
        projects = []
        for row in rows:
            project_data = dict(row)
            project_data['config'] = json.loads(project_data['config'] or '{}')
            projects.append(project_data)
        
        return projects