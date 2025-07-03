#!/usr/bin/env python3
"""
Property Creation Wizard for HomeShow Desktop
Guided interface for creating new properties with step-by-step process

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
import json
from PIL import Image, ImageTk
import threading
from core.localization import translate

class PropertyWizard:
    """
    Multi-step wizard for creating new properties
    """
    
    def __init__(self, parent, property_manager, media_handler, on_complete: Optional[Callable] = None):
        """
        Initialize property wizard
        
        Args:
            parent: Parent window
            property_manager: PropertyManager instance
            media_handler: MediaHandler instance
            on_complete: Callback function when wizard completes
        """
        self.parent = parent
        self.property_manager = property_manager
        self.media_handler = media_handler
        self.on_complete = on_complete
        
        # Wizard data
        self.property_data = {}
        self.media_files = []
        self.current_step = 0
        
        # Wizard steps
        self.steps = [
            {
                'title': translate('wizard_basic_info'),
                'description': translate('wizard_basic_info_desc'),
                'create_func': self.create_basic_info_step
            },
            {
                'title': translate('wizard_media_upload'),
                'description': translate('wizard_media_upload_desc'),
                'create_func': self.create_media_step
            },
            {
                'title': translate('wizard_features'),
                'description': translate('wizard_features_desc'),
                'create_func': self.create_features_step
            },
            {
                'title': translate('wizard_location'),
                'description': translate('wizard_location_desc'),
                'create_func': self.create_location_step
            },
            {
                'title': translate('wizard_advanced'),
                'description': translate('wizard_advanced_desc'),
                'create_func': self.create_advanced_step
            },
            {
                'title': translate('wizard_review'),
                'description': translate('wizard_review_desc'),
                'create_func': self.create_review_step
            }
        ]
        
        self.create_wizard_window()
    
    def create_wizard_window(self):
        """
        Create wizard window
        """
        self.window = tk.Toplevel(self.parent)
        self.window.title(translate('wizard_title'))
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        # Center window
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Main container
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Progress bar
        self.create_progress_bar(main_frame)
        
        # Content area
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Navigation buttons
        self.create_navigation(main_frame)
        
        # Load first step
        self.load_step(0)
    
    def create_header(self, parent):
        """
        Create wizard header
        
        Args:
            parent: Parent widget
        """
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        self.title_label = ttk.Label(
            header_frame,
            text=translate('wizard_create_property'),
            font=('Segoe UI', 18, 'bold')
        )
        self.title_label.pack(anchor=tk.W)
        
        # Subtitle
        self.subtitle_label = ttk.Label(
            header_frame,
            text=f"{translate('wizard_step')} 1 {translate('wizard_of')} 6: {translate('wizard_basic_info')}",
            font=('Segoe UI', 12),
            foreground='gray'
        )
        self.subtitle_label.pack(anchor=tk.W, pady=(5, 0))
    
    def create_progress_bar(self, parent):
        """
        Create progress bar
        
        Args:
            parent: Parent widget
        """
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=len(self.steps),
            length=400
        )
        self.progress_bar.pack()
        
        # Update progress
        self.update_progress()
    
    def create_navigation(self, parent):
        """
        Create navigation buttons
        
        Args:
            parent: Parent widget
        """
        nav_frame = ttk.Frame(parent)
        nav_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Cancel button
        self.cancel_btn = ttk.Button(
            nav_frame,
            text=translate('wizard_cancel'),
            command=self.cancel_wizard
        )
        self.cancel_btn.pack(side=tk.LEFT)
        
        # Navigation buttons (right side)
        nav_right = ttk.Frame(nav_frame)
        nav_right.pack(side=tk.RIGHT)
        
        self.back_btn = ttk.Button(
            nav_right,
            text=f"← {translate('wizard_back')}",
            command=self.previous_step,
            state=tk.DISABLED
        )
        self.back_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.next_btn = ttk.Button(
            nav_right,
            text=f"{translate('wizard_next')} →",
            command=self.next_step,
            style='Primary.TButton'
        )
        self.next_btn.pack(side=tk.LEFT)
    
    def load_step(self, step_index: int):
        """
        Load specific wizard step
        
        Args:
            step_index: Step index to load
        """
        if 0 <= step_index < len(self.steps):
            self.current_step = step_index
            
            # Clear content frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Update header
            step = self.steps[step_index]
            self.subtitle_label.config(
                text=f"Step {step_index + 1} of {len(self.steps)}: {step['title']}"
            )
            
            # Create step content
            step['create_func']()
            
            # Update navigation
            self.update_navigation()
            
            # Update progress
            self.update_progress()
    
    def update_navigation(self):
        """
        Update navigation button states
        """
        # Back button
        self.back_btn.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        
        # Next/Finish button
        if self.current_step == len(self.steps) - 1:
            self.next_btn.config(text="Create Property")
        else:
            self.next_btn.config(text="Next →")
    
    def update_progress(self):
        """
        Update progress bar
        """
        self.progress_var.set(self.current_step + 1)
    
    def next_step(self):
        """
        Move to next step
        """
        # Validate current step
        if not self.validate_current_step():
            return
        
        # Save current step data
        self.save_current_step()
        
        if self.current_step < len(self.steps) - 1:
            self.load_step(self.current_step + 1)
        else:
            # Final step - create property
            self.create_property()
    
    def previous_step(self):
        """
        Move to previous step
        """
        if self.current_step > 0:
            self.save_current_step()
            self.load_step(self.current_step - 1)
    
    def validate_current_step(self) -> bool:
        """
        Validate current step data
        
        Returns:
            bool: True if valid, False otherwise
        """
        if self.current_step == 0:  # Basic info
            return self.validate_basic_info()
        elif self.current_step == 1:  # Media
            return self.validate_media()
        elif self.current_step == 2:  # Features
            return self.validate_features()
        elif self.current_step == 3:  # Location
            return self.validate_location()
        elif self.current_step == 4:  # Advanced
            return self.validate_advanced()
        elif self.current_step == 5:  # Review
            return True
        
        return True
    
    def save_current_step(self):
        """
        Save current step data
        """
        if self.current_step == 0:
            self.save_basic_info()
        elif self.current_step == 1:
            self.save_media()
        elif self.current_step == 2:
            self.save_features()
        elif self.current_step == 3:
            self.save_location()
        elif self.current_step == 4:
            self.save_advanced()
    
    # Step 1: Basic Information
    def create_basic_info_step(self):
        """
        Create basic information step
        """
        # Scrollable frame
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        form_frame = ttk.Frame(scrollable_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Property title
        ttk.Label(form_frame, text="Property Title *", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.title_var = tk.StringVar(value=self.property_data.get('title', ''))
        title_entry = ttk.Entry(form_frame, textvariable=self.title_var, font=('Segoe UI', 11))
        title_entry.pack(fill=tk.X, pady=(5, 15))
        
        # Property type
        ttk.Label(form_frame, text="Property Type *", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.type_var = tk.StringVar(value=self.property_data.get('property_type', ''))
        type_combo = ttk.Combobox(
            form_frame,
            textvariable=self.type_var,
            values=['House', 'Apartment', 'Condo', 'Townhouse', 'Villa', 'Studio', 'Loft', 'Commercial', 'Land'],
            state='readonly'
        )
        type_combo.pack(fill=tk.X, pady=(5, 15))
        
        # Price
        ttk.Label(form_frame, text="Price (€) *", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.price_var = tk.StringVar(value=str(self.property_data.get('price', '')))
        price_entry = ttk.Entry(form_frame, textvariable=self.price_var, font=('Segoe UI', 11))
        price_entry.pack(fill=tk.X, pady=(5, 15))
        
        # Surface area
        ttk.Label(form_frame, text="Surface Area (m²)", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.surface_var = tk.StringVar(value=str(self.property_data.get('surface_area', '')))
        surface_entry = ttk.Entry(form_frame, textvariable=self.surface_var, font=('Segoe UI', 11))
        surface_entry.pack(fill=tk.X, pady=(5, 15))
        
        # Rooms
        rooms_frame = ttk.Frame(form_frame)
        rooms_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Bedrooms
        bed_frame = ttk.Frame(rooms_frame)
        bed_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Label(bed_frame, text="Bedrooms", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.bedrooms_var = tk.StringVar(value=str(self.property_data.get('bedrooms', '')))
        bed_entry = ttk.Entry(bed_frame, textvariable=self.bedrooms_var, font=('Segoe UI', 11))
        bed_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Bathrooms
        bath_frame = ttk.Frame(rooms_frame)
        bath_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        ttk.Label(bath_frame, text="Bathrooms", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.bathrooms_var = tk.StringVar(value=str(self.property_data.get('bathrooms', '')))
        bath_entry = ttk.Entry(bath_frame, textvariable=self.bathrooms_var, font=('Segoe UI', 11))
        bath_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Description
        ttk.Label(form_frame, text="Description", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.description_text = tk.Text(
            form_frame,
            height=6,
            font=('Segoe UI', 10),
            wrap=tk.WORD
        )
        self.description_text.pack(fill=tk.X, pady=(5, 15))
        self.description_text.insert('1.0', self.property_data.get('description', ''))
        
        # Status
        ttk.Label(form_frame, text="Status", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.status_var = tk.StringVar(value=self.property_data.get('status', 'draft'))
        status_combo = ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=['draft', 'published', 'archived'],
            state='readonly'
        )
        status_combo.pack(fill=tk.X, pady=(5, 0))
    
    def validate_basic_info(self) -> bool:
        """
        Validate basic information
        
        Returns:
            bool: True if valid
        """
        if not self.title_var.get().strip():
            messagebox.showerror("Validation Error", "Property title is required.")
            return False
        
        if not self.type_var.get():
            messagebox.showerror("Validation Error", "Property type is required.")
            return False
        
        try:
            price = float(self.price_var.get()) if self.price_var.get() else 0
            if price <= 0:
                messagebox.showerror("Validation Error", "Price must be greater than 0.")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Price must be a valid number.")
            return False
        
        return True
    
    def save_basic_info(self):
        """
        Save basic information
        """
        self.property_data.update({
            'title': self.title_var.get().strip(),
            'property_type': self.type_var.get(),
            'price': float(self.price_var.get()) if self.price_var.get() else 0,
            'surface_area': float(self.surface_var.get()) if self.surface_var.get() else None,
            'bedrooms': int(self.bedrooms_var.get()) if self.bedrooms_var.get() else None,
            'bathrooms': int(self.bathrooms_var.get()) if self.bathrooms_var.get() else None,
            'description': self.description_text.get('1.0', tk.END).strip(),
            'status': self.status_var.get()
        })
    
    # Step 2: Media Upload
    def create_media_step(self):
        """
        Create media upload step
        """
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="Add photos and videos to showcase your property. High-quality images improve engagement.",
            font=('Segoe UI', 10),
            foreground='gray'
        )
        instructions.pack(anchor=tk.W, pady=(0, 20))
        
        # Upload buttons
        upload_frame = ttk.Frame(main_frame)
        upload_frame.pack(fill=tk.X, pady=(0, 20))
        
        add_photos_btn = ttk.Button(
            upload_frame,
            text="📷 Add Photos",
            command=self.add_photos,
            style='Primary.TButton'
        )
        add_photos_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        add_videos_btn = ttk.Button(
            upload_frame,
            text="🎥 Add Videos",
            command=self.add_videos
        )
        add_videos_btn.pack(side=tk.LEFT)
        
        # Media list
        list_frame = ttk.LabelFrame(main_frame, text="Uploaded Media", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Media listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.media_listbox = tk.Listbox(
            listbox_frame,
            font=('Segoe UI', 10),
            selectmode=tk.SINGLE
        )
        media_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.media_listbox.yview)
        self.media_listbox.configure(yscrollcommand=media_scrollbar.set)
        
        self.media_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        media_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Media actions
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        remove_btn = ttk.Button(
            actions_frame,
            text="Remove Selected",
            command=self.remove_selected_media
        )
        remove_btn.pack(side=tk.LEFT)
        
        clear_btn = ttk.Button(
            actions_frame,
            text="Clear All",
            command=self.clear_all_media
        )
        clear_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Load existing media
        self.refresh_media_list()
    
    def add_photos(self):
        """
        Add photo files
        """
        files = filedialog.askopenfilenames(
            title="Select Photos",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        for file_path in files:
            if file_path not in [media['path'] for media in self.media_files]:
                self.media_files.append({
                    'path': file_path,
                    'type': 'image',
                    'name': Path(file_path).name
                })
        
        self.refresh_media_list()
    
    def add_videos(self):
        """
        Add video files
        """
        files = filedialog.askopenfilenames(
            title="Select Videos",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.wmv *.flv *.webm"),
                ("All files", "*.*")
            ]
        )
        
        for file_path in files:
            if file_path not in [media['path'] for media in self.media_files]:
                self.media_files.append({
                    'path': file_path,
                    'type': 'video',
                    'name': Path(file_path).name
                })
        
        self.refresh_media_list()
    
    def refresh_media_list(self):
        """
        Refresh media list display
        """
        self.media_listbox.delete(0, tk.END)
        
        for i, media in enumerate(self.media_files):
            icon = "📷" if media['type'] == 'image' else "🎥"
            self.media_listbox.insert(tk.END, f"{icon} {media['name']}")
    
    def remove_selected_media(self):
        """
        Remove selected media file
        """
        selection = self.media_listbox.curselection()
        if selection:
            index = selection[0]
            del self.media_files[index]
            self.refresh_media_list()
    
    def clear_all_media(self):
        """
        Clear all media files
        """
        if messagebox.askyesno("Clear Media", "Remove all media files?"):
            self.media_files.clear()
            self.refresh_media_list()
    
    def validate_media(self) -> bool:
        """
        Validate media step
        
        Returns:
            bool: True if valid
        """
        # Media is optional, so always valid
        return True
    
    def save_media(self):
        """
        Save media data
        """
        self.property_data['media_files'] = self.media_files.copy()
    
    # Step 3: Property Features
    def create_features_step(self):
        """
        Create property features step
        """
        # Scrollable frame
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Features checklist
        features_frame = ttk.LabelFrame(main_frame, text="Property Features", padding=15)
        features_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Initialize feature variables
        self.feature_vars = {}
        
        # Get dynamic features based on property type and transaction type
        features = self.get_dynamic_features()
        
        # Create checkboxes in grid
        for i, feature in enumerate(features):
            self.feature_vars[feature] = tk.BooleanVar(
                value=feature in self.property_data.get('features', [])
            )
            
            cb = ttk.Checkbutton(
                features_frame,
                text=feature,
                variable=self.feature_vars[feature]
            )
            cb.grid(row=i//3, column=i%3, sticky='w', padx=10, pady=5)
        
        # Configure grid weights
        for i in range(3):
            features_frame.grid_columnconfigure(i, weight=1)
        
        # Additional features
        additional_frame = ttk.LabelFrame(main_frame, text="Additional Features", padding=15)
        additional_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(additional_frame, text="Custom features (one per line):").pack(anchor=tk.W)
        self.additional_features_text = tk.Text(
            additional_frame,
            height=4,
            font=('Segoe UI', 10)
        )
        self.additional_features_text.pack(fill=tk.X, pady=(5, 0))
        
        # Load existing additional features
        additional_features = self.property_data.get('additional_features', [])
        if additional_features:
            self.additional_features_text.insert('1.0', '\n'.join(additional_features))
        
        # Energy efficiency
        energy_frame = ttk.LabelFrame(main_frame, text="Energy Efficiency", padding=15)
        energy_frame.pack(fill=tk.X)
        
        ttk.Label(energy_frame, text="Energy Rating:").pack(anchor=tk.W)
        self.energy_var = tk.StringVar(value=self.property_data.get('energy_rating', ''))
        energy_combo = ttk.Combobox(
            energy_frame,
            textvariable=self.energy_var,
            values=['A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'Not Rated'],
            state='readonly'
        )
        energy_combo.pack(fill=tk.X, pady=(5, 0))
    
    def get_dynamic_features(self) -> List[str]:
        """
        Get features list based on property type and transaction type
        
        Returns:
            List[str]: Appropriate features for the property
        """
        property_type = self.property_data.get('property_type', '').lower()
        transaction_type = self.property_data.get('transaction_type', '').lower()
        
        # Base features for all properties
        base_features = ['Parking', 'Garage', 'Elevator', 'Security System']
        
        # Features for residential properties
        residential_features = [
            'Air Conditioning', 'Heating', 'Fireplace', 'Balcony', 'Terrace', 
            'Garden', 'Swimming Pool'
        ]
        
        # Features specific to rental properties
        rental_features = [
            'Furnished', 'Washing Machine', 'Dishwasher', 'WiFi Internet', 
            'Television', 'Utilities Included', 'Pets Allowed', 'Smoking Allowed'
        ]
        
        # Features specific to sale properties
        sale_features = [
            'New Construction', 'Recently Renovated', 'Investment Property', 
            'Mortgage Available'
        ]
        
        # Features for commercial properties
        commercial_features = [
            'Conference Room', 'Reception Area', 'Kitchen Facilities', 
            'Storage Space', 'Loading Dock', 'Handicap Accessible'
        ]
        
        # Start with base features
        features = base_features.copy()
        
        # Add residential features for non-commercial properties
        if property_type not in ['commercial', 'office', 'warehouse']:
            features.extend(residential_features)
        
        # Add commercial features for commercial properties
        if property_type in ['commercial', 'office', 'warehouse']:
            features.extend(commercial_features)
        
        # Add transaction-specific features
        if 'rent' in transaction_type or 'location' in transaction_type:
            features.extend(rental_features)
        elif 'sale' in transaction_type or 'vente' in transaction_type:
            features.extend(sale_features)
        
        # Remove duplicates and sort
        return sorted(list(set(features)))
    
    def validate_features(self) -> bool:
        """
        Validate features step
        
        Returns:
            bool: True if valid
        """
        return True
    
    def save_features(self):
        """
        Save features data
        """
        # Selected features
        selected_features = [feature for feature, var in self.feature_vars.items() if var.get()]
        
        # Additional features
        additional_text = self.additional_features_text.get('1.0', tk.END).strip()
        additional_features = [f.strip() for f in additional_text.split('\n') if f.strip()]
        
        self.property_data.update({
            'features': selected_features,
            'additional_features': additional_features,
            'energy_rating': self.energy_var.get()
        })
    
    # Step 4: Location & Neighborhood
    def create_location_step(self):
        """
        Create location step
        """
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Address section
        address_frame = ttk.LabelFrame(main_frame, text="Address", padding=15)
        address_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Street address
        ttk.Label(address_frame, text="Street Address", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.address_var = tk.StringVar(value=self.property_data.get('address', ''))
        address_entry = ttk.Entry(address_frame, textvariable=self.address_var, font=('Segoe UI', 11))
        address_entry.pack(fill=tk.X, pady=(5, 15))
        
        # City and postal code
        city_frame = ttk.Frame(address_frame)
        city_frame.pack(fill=tk.X, pady=(0, 15))
        
        # City
        city_left = ttk.Frame(city_frame)
        city_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Label(city_left, text="City", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.city_var = tk.StringVar(value=self.property_data.get('city', ''))
        city_entry = ttk.Entry(city_left, textvariable=self.city_var, font=('Segoe UI', 11))
        city_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Postal code
        postal_right = ttk.Frame(city_frame)
        postal_right.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        ttk.Label(postal_right, text="Postal Code", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.postal_var = tk.StringVar(value=self.property_data.get('postal_code', ''))
        postal_entry = ttk.Entry(postal_right, textvariable=self.postal_var, font=('Segoe UI', 11))
        postal_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Country
        ttk.Label(address_frame, text="Country", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.country_var = tk.StringVar(value=self.property_data.get('country', 'France'))
        country_combo = ttk.Combobox(
            address_frame,
            textvariable=self.country_var,
            values=['France', 'Belgium', 'Switzerland', 'Luxembourg', 'Spain', 'Italy', 'Germany', 'Other'],
            state='readonly'
        )
        country_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Neighborhood info
        neighborhood_frame = ttk.LabelFrame(main_frame, text="Neighborhood Information", padding=15)
        neighborhood_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(neighborhood_frame, text="Describe the neighborhood, nearby amenities, transportation, etc.").pack(anchor=tk.W)
        self.neighborhood_text = tk.Text(
            neighborhood_frame,
            height=8,
            font=('Segoe UI', 10),
            wrap=tk.WORD
        )
        self.neighborhood_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.neighborhood_text.insert('1.0', self.property_data.get('neighborhood_info', ''))
    
    def validate_location(self) -> bool:
        """
        Validate location step
        
        Returns:
            bool: True if valid
        """
        return True
    
    def save_location(self):
        """
        Save location data
        """
        self.property_data.update({
            'address': self.address_var.get().strip(),
            'city': self.city_var.get().strip(),
            'postal_code': self.postal_var.get().strip(),
            'country': self.country_var.get(),
            'neighborhood_info': self.neighborhood_text.get('1.0', tk.END).strip()
        })
    
    # Step 5: Advanced Options
    def create_advanced_step(self):
        """
        Create advanced options step
        """
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Website options
        website_frame = ttk.LabelFrame(main_frame, text="Website Options", padding=15)
        website_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Template selection
        ttk.Label(website_frame, text="Website Template", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.template_var = tk.StringVar(value=self.property_data.get('template', 'modern'))
        template_combo = ttk.Combobox(
            website_frame,
            textvariable=self.template_var,
            values=['modern', 'luxury', 'minimal', 'bold'],
            state='readonly'
        )
        template_combo.pack(fill=tk.X, pady=(5, 15))
        
        # SEO options
        seo_frame = ttk.LabelFrame(main_frame, text="SEO Settings", padding=15)
        seo_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Meta description
        ttk.Label(seo_frame, text="Meta Description").pack(anchor=tk.W)
        self.meta_desc_text = tk.Text(
            seo_frame,
            height=3,
            font=('Segoe UI', 10),
            wrap=tk.WORD
        )
        self.meta_desc_text.pack(fill=tk.X, pady=(5, 15))
        self.meta_desc_text.insert('1.0', self.property_data.get('meta_description', ''))
        
        # Keywords
        ttk.Label(seo_frame, text="Keywords (comma-separated)").pack(anchor=tk.W)
        self.keywords_var = tk.StringVar(value=self.property_data.get('keywords', ''))
        keywords_entry = ttk.Entry(seo_frame, textvariable=self.keywords_var, font=('Segoe UI', 11))
        keywords_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Contact options
        contact_frame = ttk.LabelFrame(main_frame, text="Contact Information", padding=15)
        contact_frame.pack(fill=tk.X)
        
        # Agent name
        ttk.Label(contact_frame, text="Agent/Contact Name").pack(anchor=tk.W)
        self.agent_var = tk.StringVar(value=self.property_data.get('agent_name', ''))
        agent_entry = ttk.Entry(contact_frame, textvariable=self.agent_var, font=('Segoe UI', 11))
        agent_entry.pack(fill=tk.X, pady=(5, 15))
        
        # Contact details
        contact_details_frame = ttk.Frame(contact_frame)
        contact_details_frame.pack(fill=tk.X)
        
        # Phone
        phone_frame = ttk.Frame(contact_details_frame)
        phone_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Label(phone_frame, text="Phone").pack(anchor=tk.W)
        self.phone_var = tk.StringVar(value=self.property_data.get('agent_phone', ''))
        phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_var, font=('Segoe UI', 11))
        phone_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Email
        email_frame = ttk.Frame(contact_details_frame)
        email_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        ttk.Label(email_frame, text="Email").pack(anchor=tk.W)
        self.email_var = tk.StringVar(value=self.property_data.get('agent_email', ''))
        email_entry = ttk.Entry(email_frame, textvariable=self.email_var, font=('Segoe UI', 11))
        email_entry.pack(fill=tk.X, pady=(5, 0))
    
    def validate_advanced(self) -> bool:
        """
        Validate advanced options step
        
        Returns:
            bool: True if valid
        """
        return True
    
    def save_advanced(self):
        """
        Save advanced options data
        """
        self.property_data.update({
            'template': self.template_var.get(),
            'meta_description': self.meta_desc_text.get('1.0', tk.END).strip(),
            'keywords': self.keywords_var.get().strip(),
            'agent_name': self.agent_var.get().strip(),
            'agent_phone': self.phone_var.get().strip(),
            'agent_email': self.email_var.get().strip()
        })
    
    # Step 6: Review & Create
    def create_review_step(self):
        """
        Create review step
        """
        # Scrollable frame
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Review header
        ttk.Label(
            main_frame,
            text="Review Property Information",
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Property summary
        self.create_property_summary(main_frame)
    
    def create_property_summary(self, parent):
        """
        Create property summary for review
        
        Args:
            parent: Parent widget
        """
        # Basic info
        basic_frame = ttk.LabelFrame(parent, text="Basic Information", padding=10)
        basic_frame.pack(fill=tk.X, pady=(0, 15))
        
        basic_info = [
            ('Title', self.property_data.get('title', 'N/A')),
            ('Type', self.property_data.get('property_type', 'N/A')),
            ('Price', f"€{self.property_data.get('price', 0):,.0f}"),
            ('Surface Area', f"{self.property_data.get('surface_area', 'N/A')} m²" if self.property_data.get('surface_area') else 'N/A'),
            ('Bedrooms', str(self.property_data.get('bedrooms', 'N/A'))),
            ('Bathrooms', str(self.property_data.get('bathrooms', 'N/A'))),
            ('Status', self.property_data.get('status', 'draft').title())
        ]
        
        for label, value in basic_info:
            info_frame = ttk.Frame(basic_frame)
            info_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(info_frame, text=f"{label}:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)
            ttk.Label(info_frame, text=str(value), font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Media summary
        media_frame = ttk.LabelFrame(parent, text="Media Files", padding=10)
        media_frame.pack(fill=tk.X, pady=(0, 15))
        
        media_count = len(self.media_files)
        image_count = len([m for m in self.media_files if m['type'] == 'image'])
        video_count = len([m for m in self.media_files if m['type'] == 'video'])
        
        ttk.Label(
            media_frame,
            text=f"Total: {media_count} files ({image_count} images, {video_count} videos)",
            font=('Segoe UI', 9)
        ).pack(anchor=tk.W)
        
        # Features summary
        if self.property_data.get('features') or self.property_data.get('additional_features'):
            features_frame = ttk.LabelFrame(parent, text="Features", padding=10)
            features_frame.pack(fill=tk.X, pady=(0, 15))
            
            all_features = self.property_data.get('features', []) + self.property_data.get('additional_features', [])
            features_text = ', '.join(all_features) if all_features else 'None'
            
            ttk.Label(
                features_frame,
                text=features_text,
                font=('Segoe UI', 9),
                wraplength=600
            ).pack(anchor=tk.W)
        
        # Location summary
        if any([self.property_data.get('address'), self.property_data.get('city')]):
            location_frame = ttk.LabelFrame(parent, text="Location", padding=10)
            location_frame.pack(fill=tk.X, pady=(0, 15))
            
            location_parts = []
            if self.property_data.get('address'):
                location_parts.append(self.property_data['address'])
            if self.property_data.get('city'):
                location_parts.append(self.property_data['city'])
            if self.property_data.get('postal_code'):
                location_parts.append(self.property_data['postal_code'])
            if self.property_data.get('country'):
                location_parts.append(self.property_data['country'])
            
            location_text = ', '.join(location_parts)
            ttk.Label(
                location_frame,
                text=location_text,
                font=('Segoe UI', 9)
            ).pack(anchor=tk.W)
    
    def validate_property_data(self) -> tuple[bool, str]:
        """
        Validate all property data before creation
        
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        errors = []
        
        # Required fields validation
        required_fields = {
            'title': 'Property title is required',
            'property_type': 'Property type must be selected',
            'price': 'Price is required',
            'transaction_type': 'Transaction type must be selected'
        }
        
        for field, error_msg in required_fields.items():
            value = self.property_data.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                errors.append(error_msg)
        
        # Numeric fields validation
        numeric_fields = ['price', 'surface_area', 'bedrooms', 'bathrooms']
        for field in numeric_fields:
            value = self.property_data.get(field)
            if value is not None:
                try:
                    num_value = float(value) if field in ['price', 'surface_area'] else int(value)
                    if num_value < 0:
                        errors.append(f"{field.replace('_', ' ').title()} cannot be negative")
                    elif field == 'price' and num_value == 0:
                        errors.append("Price must be greater than 0")
                except (ValueError, TypeError):
                    errors.append(f"{field.replace('_', ' ').title()} must be a valid number")
        
        # Title length validation
        title = self.property_data.get('title', '')
        if len(title.strip()) < 3:
            errors.append("Property title must be at least 3 characters long")
        elif len(title.strip()) > 200:
            errors.append("Property title cannot exceed 200 characters")
        
        # Description validation
        description = self.property_data.get('description', '')
        if description and len(description.strip()) > 5000:
            errors.append("Description cannot exceed 5000 characters")
        
        # Location validation
        if self.property_data.get('city') and len(self.property_data['city'].strip()) < 2:
            errors.append("City name must be at least 2 characters long")
        
        # Postal code validation (basic format check)
        postal_code = self.property_data.get('postal_code', '')
        if postal_code and not postal_code.strip().replace(' ', '').replace('-', '').isalnum():
            errors.append("Postal code contains invalid characters")
        
        # Media validation
        if not self.media_files:
            errors.append("At least one image is required for the property")
        else:
            # Check if at least one image exists
            has_image = any(media.get('type') == 'image' for media in self.media_files)
            if not has_image:
                errors.append("At least one image file is required")
        
        # Features validation
        features = self.property_data.get('features', [])
        additional_features = self.property_data.get('additional_features', [])
        total_features = len(features) + len(additional_features)
        if total_features > 50:
            errors.append("Too many features selected (maximum 50)")
        
        # Check for duplicate features
        all_features = features + additional_features
        if len(all_features) != len(set(all_features)):
            errors.append("Duplicate features detected")
        
        # Property type specific validation
        property_type = self.property_data.get('property_type', '').lower()
        if property_type in ['apartment', 'house', 'villa', 'condo']:
            if not self.property_data.get('bedrooms'):
                errors.append(f"{property_type.title()} must have at least one bedroom specified")
        
        # Transaction type specific validation
        transaction_type = self.property_data.get('transaction_type', '').lower()
        if 'rent' in transaction_type or 'location' in transaction_type:
            # For rental properties, ensure reasonable price range
            price = self.property_data.get('price', 0)
            try:
                price_val = float(price)
                if price_val > 50000:  # Monthly rent over 50k seems unrealistic
                    errors.append("Rental price seems unusually high. Please verify.")
            except (ValueError, TypeError):
                pass
        
        if errors:
            return False, "\n• ".join(["Validation errors:"] + errors)
        
        return True, ""
    
    def create_property(self):
        """
        Create the property in database with validation
        """
        try:
            # Save current step data
            self.save_current_step()
            
            # Validate property data
            is_valid, error_message = self.validate_property_data()
            if not is_valid:
                messagebox.showerror("Validation Error", error_message)
                return
            
            # Show progress dialog
            progress_window = self.show_progress_dialog()
            
            # Create property in separate thread
            def create_thread():
                try:
                    # Prepare media file paths
                    media_file_paths = [media['path'] for media in self.media_files] if self.media_files else None
                    
                    # Create property with media
                    property_id, media_dir = self.property_manager.create_property_with_media(
                        self.property_data, 
                        media_file_paths
                    )
                    
                    # Close progress dialog
                    progress_window.destroy()
                    
                    # Show success message
                    messagebox.showinfo(
                        "Success",
                        f"Property '{self.property_data['title']}' created successfully!"
                    )
                    
                    # Close wizard
                    self.window.destroy()
                    
                    # Call completion callback
                    if self.on_complete:
                        self.on_complete(property_id)
                        
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Failed to create property: {str(e)}")
            
            # Start creation thread
            threading.Thread(target=create_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create property: {str(e)}")
    
    def show_progress_dialog(self):
        """
        Show progress dialog
        
        Returns:
            tk.Toplevel: Progress window
        """
        progress_window = tk.Toplevel(self.window)
        progress_window.title("Creating Property")
        progress_window.geometry("300x100")
        progress_window.resizable(False, False)
        progress_window.transient(self.window)
        progress_window.grab_set()
        
        # Center the window
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (300 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (100 // 2)
        progress_window.geometry(f"300x100+{x}+{y}")
        
        # Progress content
        ttk.Label(
            progress_window,
            text="Creating property...",
            font=('Segoe UI', 12)
        ).pack(pady=20)
        
        progress_bar = ttk.Progressbar(
            progress_window,
            mode='indeterminate',
            length=250
        )
        progress_bar.pack(pady=10)
        progress_bar.start()
        
        return progress_window
    
    def cancel_wizard(self):
        """
        Cancel wizard
        """
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel? All data will be lost."):
            self.window.destroy()