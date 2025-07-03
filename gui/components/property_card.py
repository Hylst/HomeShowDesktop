#!/usr/bin/env python3
"""
Property Card Component for HomeShow Desktop
Custom widget for displaying property information in card format

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from PIL import Image, ImageTk
import threading

class PropertyCard:
    """
    Custom property card widget for displaying property summaries
    """
    
    def __init__(self, parent, property_data: Dict[str, Any], 
                 on_click: Optional[Callable] = None,
                 on_edit: Optional[Callable] = None,
                 on_delete: Optional[Callable] = None,
                 on_generate: Optional[Callable] = None):
        """
        Initialize property card
        
        Args:
            parent: Parent widget
            property_data: Property data dictionary
            on_click: Callback when card is clicked
            on_edit: Callback when edit button is clicked
            on_delete: Callback when delete button is clicked
            on_generate: Callback when generate button is clicked
        """
        self.parent = parent
        self.property_data = property_data
        self.on_click = on_click
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_generate = on_generate
        
        self.thumbnail_image = None
        
        self.create_card()
        self.load_thumbnail()
    
    def create_card(self):
        """
        Create property card interface
        """
        # Main card frame
        self.card_frame = ttk.Frame(
            self.parent,
            style='Card.TFrame',
            relief=tk.RAISED,
            borderwidth=1
        )
        self.card_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Bind click event to card
        if self.on_click:
            self.card_frame.bind("<Button-1>", lambda e: self.on_click(self.property_data))
        
        # Card content
        content_frame = ttk.Frame(self.card_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left side - Image
        self.create_image_section(content_frame)
        
        # Middle - Property info
        self.create_info_section(content_frame)
        
        # Right side - Actions and status
        self.create_actions_section(content_frame)
    
    def create_image_section(self, parent):
        """
        Create image section
        
        Args:
            parent: Parent widget
        """
        self.image_frame = ttk.Frame(parent)
        self.image_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        # Placeholder image
        self.image_label = ttk.Label(
            self.image_frame,
            text="📷",
            font=('Segoe UI', 24),
            width=8,
            anchor=tk.CENTER,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.image_label.pack()
        
        # Image count badge
        image_count = self.property_data.get('image_count', 0)
        if image_count > 0:
            count_label = ttk.Label(
                self.image_frame,
                text=f"{image_count} photos",
                font=('Segoe UI', 8),
                foreground='gray'
            )
            count_label.pack(pady=(2, 0))
    
    def create_info_section(self, parent):
        """
        Create property information section
        
        Args:
            parent: Parent widget
        """
        info_frame = ttk.Frame(parent)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Property title
        title_label = ttk.Label(
            info_frame,
            text=self.property_data.get('title', 'Untitled Property'),
            font=('Segoe UI', 14, 'bold'),
            foreground='#2c3e50'
        )
        title_label.pack(anchor=tk.W)
        
        # Property type and location
        type_location = []
        if self.property_data.get('property_type'):
            type_location.append(self.property_data['property_type'])
        if self.property_data.get('city'):
            type_location.append(self.property_data['city'])
        
        if type_location:
            type_location_text = " • ".join(type_location)
            type_label = ttk.Label(
                info_frame,
                text=type_location_text,
                font=('Segoe UI', 10),
                foreground='#7f8c8d'
            )
            type_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Price
        if self.property_data.get('price'):
            price_text = f"€{self.property_data['price']:,.0f}"
            price_label = ttk.Label(
                info_frame,
                text=price_text,
                font=('Segoe UI', 16, 'bold'),
                foreground='#27ae60'
            )
            price_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Property details
        details_frame = ttk.Frame(info_frame)
        details_frame.pack(anchor=tk.W, pady=(8, 0))
        
        # Rooms, surface area, etc.
        details = []
        if self.property_data.get('bedrooms'):
            details.append(f"{self.property_data['bedrooms']} bed")
        if self.property_data.get('bathrooms'):
            details.append(f"{self.property_data['bathrooms']} bath")
        if self.property_data.get('surface_area'):
            details.append(f"{self.property_data['surface_area']} m²")
        
        if details:
            details_text = " • ".join(details)
            details_label = ttk.Label(
                details_frame,
                text=details_text,
                font=('Segoe UI', 9),
                foreground='#95a5a6'
            )
            details_label.pack(side=tk.LEFT)
        
        # Description preview
        if self.property_data.get('description'):
            desc_text = self.property_data['description'][:100]
            if len(self.property_data['description']) > 100:
                desc_text += "..."
            
            desc_label = ttk.Label(
                info_frame,
                text=desc_text,
                font=('Segoe UI', 9),
                foreground='#7f8c8d',
                wraplength=300
            )
            desc_label.pack(anchor=tk.W, pady=(8, 0))
        
        # Features preview
        features = self.property_data.get('features', [])
        if features:
            features_text = ", ".join(features[:3])
            if len(features) > 3:
                features_text += f" +{len(features) - 3} more"
            
            features_label = ttk.Label(
                info_frame,
                text=f"Features: {features_text}",
                font=('Segoe UI', 8),
                foreground='#95a5a6'
            )
            features_label.pack(anchor=tk.W, pady=(5, 0))
    
    def create_actions_section(self, parent):
        """
        Create actions and status section
        
        Args:
            parent: Parent widget
        """
        actions_frame = ttk.Frame(parent)
        actions_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status badge
        status = self.property_data.get('status', 'draft')
        status_colors = {
            'draft': '#f39c12',
            'published': '#27ae60',
            'archived': '#95a5a6'
        }
        
        status_frame = ttk.Frame(actions_frame)
        status_frame.pack(anchor=tk.NE, pady=(0, 10))
        
        status_label = tk.Label(
            status_frame,
            text=status.upper(),
            font=('Segoe UI', 8, 'bold'),
            fg='white',
            bg=status_colors.get(status, '#95a5a6'),
            padx=8,
            pady=2
        )
        status_label.pack()
        
        # Last modified
        if self.property_data.get('updated_at'):
            updated_label = ttk.Label(
                actions_frame,
                text=f"Updated: {self.property_data['updated_at'][:10]}",
                font=('Segoe UI', 8),
                foreground='#95a5a6'
            )
            updated_label.pack(anchor=tk.NE, pady=(0, 15))
        
        # Action buttons
        buttons_frame = ttk.Frame(actions_frame)
        buttons_frame.pack(anchor=tk.NE)
        
        # Edit button
        if self.on_edit:
            edit_btn = ttk.Button(
                buttons_frame,
                text="✏️ Edit",
                command=lambda: self.on_edit(self.property_data),
                width=10
            )
            edit_btn.pack(pady=2)
        
        # Generate button
        if self.on_generate:
            generate_btn = ttk.Button(
                buttons_frame,
                text="🌐 Generate",
                command=lambda: self.on_generate(self.property_data),
                width=10,
                style='Primary.TButton'
            )
            generate_btn.pack(pady=2)
        
        # Delete button
        if self.on_delete:
            delete_btn = ttk.Button(
                buttons_frame,
                text="🗑️ Delete",
                command=lambda: self.on_delete(self.property_data),
                width=10,
                style='Danger.TButton'
            )
            delete_btn.pack(pady=2)
        
        # Quick stats
        stats_frame = ttk.Frame(actions_frame)
        stats_frame.pack(anchor=tk.NE, pady=(15, 0))
        
        # Property ID
        id_label = ttk.Label(
            stats_frame,
            text=f"ID: {self.property_data.get('id', 'N/A')}",
            font=('Segoe UI', 8),
            foreground='#bdc3c7'
        )
        id_label.pack(anchor=tk.E)
        
        # Creation date
        if self.property_data.get('created_at'):
            created_label = ttk.Label(
                stats_frame,
                text=f"Created: {self.property_data['created_at'][:10]}",
                font=('Segoe UI', 8),
                foreground='#bdc3c7'
            )
            created_label.pack(anchor=tk.E)
    
    def load_thumbnail(self):
        """
        Load property thumbnail image
        """
        # Get first image from property
        thumbnail_path = self.property_data.get('thumbnail_path')
        if not thumbnail_path and self.property_data.get('media_files'):
            # Use first image as thumbnail
            media_files = self.property_data['media_files']
            image_files = [f for f in media_files if f.get('type') == 'image']
            if image_files:
                thumbnail_path = image_files[0].get('path')
        
        if thumbnail_path and Path(thumbnail_path).exists():
            # Load thumbnail in background thread
            threading.Thread(
                target=self._load_thumbnail_thread,
                args=(thumbnail_path,),
                daemon=True
            ).start()
    
    def _load_thumbnail_thread(self, image_path: str):
        """
        Load thumbnail in background thread
        
        Args:
            image_path: Path to image file
        """
        try:
            # Load and resize image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create thumbnail
                img.thumbnail((80, 80), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Update UI in main thread
                self.parent.after(
                    0,
                    lambda: self._set_thumbnail(photo)
                )
                
        except Exception as e:
            print(f"Error loading thumbnail for {image_path}: {e}")
    
    def _set_thumbnail(self, photo):
        """
        Set thumbnail image (called from main thread)
        
        Args:
            photo: PhotoImage object
        """
        self.thumbnail_image = photo
        self.image_label.config(
            image=photo,
            text=""
        )
    
    def update_data(self, property_data: Dict[str, Any]):
        """
        Update property data and refresh display
        
        Args:
            property_data: Updated property data
        """
        self.property_data = property_data
        
        # Recreate card with new data
        self.card_frame.destroy()
        self.create_card()
        self.load_thumbnail()
    
    def get_widget(self) -> ttk.Frame:
        """
        Get main widget frame
        
        Returns:
            ttk.Frame: Main card frame
        """
        return self.card_frame
    
    def destroy(self):
        """
        Destroy the card widget
        """
        if self.card_frame:
            self.card_frame.destroy()

class PropertyGrid:
    """
    Grid container for multiple property cards
    """
    
    def __init__(self, parent, properties: list = None,
                 on_property_click: Optional[Callable] = None,
                 on_property_edit: Optional[Callable] = None,
                 on_property_delete: Optional[Callable] = None,
                 on_property_generate: Optional[Callable] = None):
        """
        Initialize property grid
        
        Args:
            parent: Parent widget
            properties: List of property data dictionaries
            on_property_click: Callback when property is clicked
            on_property_edit: Callback when property edit is clicked
            on_property_delete: Callback when property delete is clicked
            on_property_generate: Callback when property generate is clicked
        """
        self.parent = parent
        self.properties = properties or []
        self.on_property_click = on_property_click
        self.on_property_edit = on_property_edit
        self.on_property_delete = on_property_delete
        self.on_property_generate = on_property_generate
        
        self.property_cards = []
        
        self.create_grid()
    
    def create_grid(self):
        """
        Create property grid interface
        """
        # Main container with scrollbar
        self.canvas = tk.Canvas(self.parent, bg='white')
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Load properties
        self.load_properties()
    
    def _on_mousewheel(self, event):
        """
        Handle mouse wheel scrolling
        
        Args:
            event: Mouse wheel event
        """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_properties(self):
        """
        Load property cards
        """
        # Clear existing cards
        self.clear_cards()
        
        if not self.properties:
            # Show empty state
            self.show_empty_state()
            return
        
        # Create property cards
        for property_data in self.properties:
            card = PropertyCard(
                self.scrollable_frame,
                property_data,
                on_click=self.on_property_click,
                on_edit=self.on_property_edit,
                on_delete=self.on_property_delete,
                on_generate=self.on_property_generate
            )
            self.property_cards.append(card)
    
    def show_empty_state(self):
        """
        Show empty state when no properties
        """
        empty_frame = ttk.Frame(self.scrollable_frame)
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        # Empty icon
        icon_label = ttk.Label(
            empty_frame,
            text="🏠",
            font=('Segoe UI', 48),
            foreground='#bdc3c7'
        )
        icon_label.pack()
        
        # Empty message
        message_label = ttk.Label(
            empty_frame,
            text="No properties found",
            font=('Segoe UI', 16),
            foreground='#7f8c8d'
        )
        message_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(
            empty_frame,
            text="Create your first property to get started",
            font=('Segoe UI', 12),
            foreground='#95a5a6'
        )
        subtitle_label.pack()
    
    def clear_cards(self):
        """
        Clear all property cards
        """
        for card in self.property_cards:
            card.destroy()
        self.property_cards.clear()
        
        # Clear scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def update_properties(self, properties: list):
        """
        Update properties list and refresh display
        
        Args:
            properties: Updated list of property data
        """
        self.properties = properties
        self.load_properties()
    
    def add_property(self, property_data: Dict[str, Any]):
        """
        Add new property to grid
        
        Args:
            property_data: Property data dictionary
        """
        self.properties.append(property_data)
        
        # If this is the first property, reload grid
        if len(self.properties) == 1:
            self.load_properties()
        else:
            # Add single card
            card = PropertyCard(
                self.scrollable_frame,
                property_data,
                on_click=self.on_property_click,
                on_edit=self.on_property_edit,
                on_delete=self.on_property_delete,
                on_generate=self.on_property_generate
            )
            self.property_cards.append(card)
    
    def remove_property(self, property_id: int):
        """
        Remove property from grid
        
        Args:
            property_id: Property ID to remove
        """
        # Find and remove property
        self.properties = [p for p in self.properties if p.get('id') != property_id]
        
        # Reload grid
        self.load_properties()
    
    def get_widget(self) -> tk.Canvas:
        """
        Get main widget
        
        Returns:
            tk.Canvas: Main canvas widget
        """
        return self.canvas