#!/usr/bin/env python3
"""
Property Manager Interface Component
Advanced interface for managing existing properties with search, filter, and detailed view

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
import sys
from datetime import datetime

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.localization import translate
from gui.components.media_gallery import MediaGallery
from gui.property_wizard import PropertyWizard

class PropertyManagerInterface:
    """
    Advanced property management interface with search, filter, and detailed view
    """
    
    def __init__(self, parent_frame, property_manager, main_window):
        """
        Initialize property manager interface
        
        Args:
            parent_frame: Parent tkinter frame
            property_manager: PropertyManager instance
            main_window: Reference to main window
        """
        self.parent_frame = parent_frame
        self.property_manager = property_manager
        self.main_window = main_window
        
        # Current filters and search
        self.current_filters = {}
        self.search_query = ""
        self.sort_column = "updated_at"
        self.sort_direction = "desc"
        
        # Selected property
        self.selected_property_id = None
        self.selected_property_data = None
        
        # UI components
        self.properties_tree = None
        self.detail_frame = None
        self.search_var = None
        self.filter_vars = {}
        
        self.setup_interface()
    
    def setup_interface(self):
        """
        Create the property management interface
        """
        # Main container with paned window for resizable layout
        self.paned_window = ttk.PanedWindow(self.parent_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Property list with search and filters
        self.create_list_panel()
        
        # Right panel - Property details
        self.create_detail_panel()
        
        # Load initial data
        self.refresh_properties_list()
    
    def create_list_panel(self):
        """
        Create the left panel with property list, search, and filters
        """
        # Left panel frame
        left_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(left_panel, weight=2)
        
        # Header with title and new property button
        header_frame = ttk.Frame(left_panel)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="Property Management", 
                 font=('Segoe UI', 16, 'bold')).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="New Property", 
                  command=self.new_property, 
                  style='Primary.TButton').pack(side=tk.RIGHT)
        
        # Search and filter section
        self.create_search_filter_section(left_panel)
        
        # Properties list
        self.create_properties_list(left_panel)
        
        # Action buttons
        self.create_action_buttons(left_panel)
    
    def create_search_filter_section(self, parent):
        """
        Create search and filter controls
        
        Args:
            parent: Parent widget
        """
        # Search and filter frame
        search_frame = ttk.LabelFrame(parent, text="Search & Filter", padding=10)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search bar
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_row, text="Search:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        search_entry = ttk.Entry(search_row, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 10), fill=tk.X, expand=True)
        
        ttk.Button(search_row, text="Clear", 
                  command=self.clear_search).pack(side=tk.RIGHT)
        
        # Filters row 1
        filter_row1 = ttk.Frame(search_frame)
        filter_row1.pack(fill=tk.X, pady=(0, 5))
        
        # Property type filter
        ttk.Label(filter_row1, text="Type:").pack(side=tk.LEFT)
        self.filter_vars['property_type'] = tk.StringVar(value="All")
        type_combo = ttk.Combobox(filter_row1, textvariable=self.filter_vars['property_type'],
                                 values=["All", "House", "Apartment", "Villa", "Condo", "Land", "Commercial"],
                                 state="readonly", width=12)
        type_combo.pack(side=tk.LEFT, padx=(5, 15))
        type_combo.bind('<<ComboboxSelected>>', self.on_filter_changed)
        
        # Transaction type filter
        ttk.Label(filter_row1, text="Transaction:").pack(side=tk.LEFT)
        self.filter_vars['transaction_type'] = tk.StringVar(value="All")
        transaction_combo = ttk.Combobox(filter_row1, textvariable=self.filter_vars['transaction_type'],
                                        values=["All", "Sale", "Rent", "Both"],
                                        state="readonly", width=12)
        transaction_combo.pack(side=tk.LEFT, padx=(5, 0))
        transaction_combo.bind('<<ComboboxSelected>>', self.on_filter_changed)
        
        # Filters row 2
        filter_row2 = ttk.Frame(search_frame)
        filter_row2.pack(fill=tk.X, pady=(0, 5))
        
        # Price range
        ttk.Label(filter_row2, text="Price Range:").pack(side=tk.LEFT)
        self.filter_vars['min_price'] = tk.StringVar()
        min_price_entry = ttk.Entry(filter_row2, textvariable=self.filter_vars['min_price'], width=10)
        min_price_entry.pack(side=tk.LEFT, padx=(5, 2))
        
        ttk.Label(filter_row2, text="-").pack(side=tk.LEFT, padx=2)
        
        self.filter_vars['max_price'] = tk.StringVar()
        max_price_entry = ttk.Entry(filter_row2, textvariable=self.filter_vars['max_price'], width=10)
        max_price_entry.pack(side=tk.LEFT, padx=(2, 15))
        
        # City filter
        ttk.Label(filter_row2, text="City:").pack(side=tk.LEFT)
        self.filter_vars['city'] = tk.StringVar()
        city_entry = ttk.Entry(filter_row2, textvariable=self.filter_vars['city'], width=15)
        city_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Bind filter changes
        for var in [self.filter_vars['min_price'], self.filter_vars['max_price'], self.filter_vars['city']]:
            var.trace('w', self.on_filter_changed)
        
        # Filter buttons
        filter_buttons = ttk.Frame(search_frame)
        filter_buttons.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(filter_buttons, text="Apply Filters", 
                  command=self.apply_filters).pack(side=tk.LEFT)
        ttk.Button(filter_buttons, text="Clear Filters", 
                  command=self.clear_filters).pack(side=tk.LEFT, padx=(10, 0))
    
    def create_properties_list(self, parent):
        """
        Create the properties list with treeview
        
        Args:
            parent: Parent widget
        """
        # List frame
        list_frame = ttk.LabelFrame(parent, text="Properties", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for properties
        columns = ('ID', 'Title', 'Type', 'Transaction', 'Price', 'City', 'Bedrooms', 'Status', 'Updated')
        self.properties_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        column_widths = {'ID': 50, 'Title': 200, 'Type': 80, 'Transaction': 80, 
                        'Price': 100, 'City': 100, 'Bedrooms': 70, 'Status': 80, 'Updated': 100}
        
        for col in columns:
            self.properties_tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.properties_tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.properties_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.properties_tree.xview)
        self.properties_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.properties_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.properties_tree.bind('<<TreeviewSelect>>', self.on_property_selected)
        
        # Context menu
        self.create_context_menu()
    
    def create_action_buttons(self, parent):
        """
        Create action buttons below the list
        
        Args:
            parent: Parent widget
        """
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Primary actions
        ttk.Button(buttons_frame, text="Edit", 
                  command=self.edit_selected_property).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Duplicate", 
                  command=self.duplicate_selected_property).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Delete", 
                  command=self.delete_selected_property).pack(side=tk.LEFT, padx=(0, 15))
        
        # Secondary actions
        ttk.Button(buttons_frame, text="Generate Website", 
                  command=self.generate_website).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Export", 
                  command=self.export_selected_property).pack(side=tk.LEFT, padx=(0, 5))
        
        # Refresh button
        ttk.Button(buttons_frame, text="Refresh", 
                  command=self.refresh_properties_list).pack(side=tk.RIGHT)
    
    def create_detail_panel(self):
        """
        Create the right panel with property details
        """
        # Right panel frame
        right_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(right_panel, weight=1)
        
        # Detail frame with scrollbar
        self.detail_canvas = tk.Canvas(right_panel, bg='white')
        detail_scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=self.detail_canvas.yview)
        self.detail_frame = ttk.Frame(self.detail_canvas)
        
        self.detail_frame.bind(
            "<Configure>",
            lambda e: self.detail_canvas.configure(scrollregion=self.detail_canvas.bbox("all"))
        )
        
        self.detail_canvas.create_window((0, 0), window=self.detail_frame, anchor="nw")
        self.detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        
        # Pack detail panel
        self.detail_canvas.pack(side="left", fill="both", expand=True)
        detail_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.detail_canvas.bind("<MouseWheel>", self._on_detail_mousewheel)
        
        # Show initial message
        self.show_no_selection_message()
    
    def _on_detail_mousewheel(self, event):
        """
        Handle mouse wheel scrolling in detail panel
        
        Args:
            event: Mouse wheel event
        """
        self.detail_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def show_no_selection_message(self):
        """
        Show message when no property is selected
        """
        # Clear detail frame
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        
        # Show message
        message_frame = ttk.Frame(self.detail_frame)
        message_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=50)
        
        ttk.Label(message_frame, text="Select a property to view details", 
                 font=('Segoe UI', 14), 
                 foreground='gray').pack(expand=True)
    
    def create_context_menu(self):
        """
        Create context menu for properties list
        """
        self.context_menu = tk.Menu(self.parent_frame, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected_property)
        self.context_menu.add_command(label="Duplicate", command=self.duplicate_selected_property)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Generate Website", command=self.generate_website)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Export", command=self.export_selected_property)
        self.context_menu.add_command(label="Delete", command=self.delete_selected_property)
        
        # Bind right-click
        self.properties_tree.bind('<Button-3>', self.show_context_menu)
    
    def show_context_menu(self, event):
        """
        Show context menu
        
        Args:
            event: Right-click event
        """
        # Select item under cursor
        item = self.properties_tree.identify_row(event.y)
        if item:
            self.properties_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    # Event handlers
    def on_search_changed(self, *args):
        """
        Handle search text changes
        """
        # Debounce search - could be improved with actual debouncing
        self.search_query = self.search_var.get().strip()
        if len(self.search_query) >= 2 or self.search_query == "":
            self.apply_filters()
    
    def on_filter_changed(self, *args):
        """
        Handle filter changes
        """
        # Auto-apply filters when dropdown changes
        if hasattr(self, 'properties_tree'):
            self.apply_filters()
    
    def clear_search(self):
        """
        Clear search field
        """
        self.search_var.set("")
    
    def clear_filters(self):
        """
        Clear all filters
        """
        self.search_var.set("")
        self.filter_vars['property_type'].set("All")
        self.filter_vars['transaction_type'].set("All")
        self.filter_vars['min_price'].set("")
        self.filter_vars['max_price'].set("")
        self.filter_vars['city'].set("")
        self.apply_filters()
    
    def apply_filters(self):
        """
        Apply current filters and refresh the list
        """
        # Build filter dictionary
        filters = {}
        
        if self.search_query:
            filters['search'] = self.search_query
        
        if self.filter_vars['property_type'].get() != "All":
            filters['property_type'] = self.filter_vars['property_type'].get()
        
        if self.filter_vars['transaction_type'].get() != "All":
            filters['transaction_type'] = self.filter_vars['transaction_type'].get()
        
        if self.filter_vars['min_price'].get():
            try:
                filters['min_price'] = float(self.filter_vars['min_price'].get())
            except ValueError:
                pass
        
        if self.filter_vars['max_price'].get():
            try:
                filters['max_price'] = float(self.filter_vars['max_price'].get())
            except ValueError:
                pass
        
        if self.filter_vars['city'].get():
            filters['city'] = self.filter_vars['city'].get()
        
        self.current_filters = filters
        self.refresh_properties_list()
    
    def sort_by_column(self, column):
        """
        Sort properties by column
        
        Args:
            column: Column name to sort by
        """
        if self.sort_column == column:
            self.sort_direction = "asc" if self.sort_direction == "desc" else "desc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"
        
        self.refresh_properties_list()
    
    def on_property_selected(self, event):
        """
        Handle property selection
        
        Args:
            event: Selection event
        """
        selection = self.properties_tree.selection()
        if selection:
            item = selection[0]
            property_id = self.properties_tree.item(item)['values'][0]
            self.selected_property_id = property_id
            self.load_property_details(property_id)
        else:
            self.selected_property_id = None
            self.show_no_selection_message()
    
    def refresh_properties_list(self):
        """
        Refresh the properties list with current filters and sorting
        """
        # Clear existing items
        for item in self.properties_tree.get_children():
            self.properties_tree.delete(item)
        
        try:
            # Get filtered and sorted properties
            properties = self.property_manager.get_filtered_properties(
                filters=self.current_filters,
                sort_column=self.sort_column,
                sort_direction=self.sort_direction
            )
            
            # Populate tree
            for prop in properties:
                values = (
                    prop['id'],
                    prop['title'][:40] + '...' if len(prop['title']) > 40 else prop['title'],
                    prop['property_type'],
                    prop['transaction_type'],
                    f"€{prop['price']:,.0f}" if prop['price'] else 'N/A',
                    prop['city'] or 'N/A',
                    prop['bedrooms'] or 'N/A',
                    prop['status'],
                    prop['updated_at'][:10] if prop['updated_at'] else 'N/A'
                )
                self.properties_tree.insert('', tk.END, values=values)
            
            # Update status
            count = len(properties)
            status_text = f"Showing {count} properties"
            if self.current_filters:
                status_text += " (filtered)"
            
            if hasattr(self.main_window, 'set_status'):
                self.main_window.set_status(status_text)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load properties: {e}")
    
    def load_property_details(self, property_id: int):
        """
        Load and display property details
        
        Args:
            property_id: Property ID to load
        """
        try:
            # Get property data
            property_data = self.property_manager.get_property_by_id(property_id)
            if not property_data:
                self.show_no_selection_message()
                return
            
            self.selected_property_data = property_data
            
            # Clear detail frame
            for widget in self.detail_frame.winfo_children():
                widget.destroy()
            
            # Create detail view
            self.create_property_detail_view(property_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load property details: {e}")
    
    def create_property_detail_view(self, property_data: Dict[str, Any]):
        """
        Create detailed view of selected property
        
        Args:
            property_data: Property data dictionary
        """
        # Header
        header_frame = ttk.Frame(self.detail_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Property Details", 
                 font=('Segoe UI', 14, 'bold')).pack(anchor=tk.W)
        
        # Basic information
        self.create_basic_info_section(property_data)
        
        # Location information
        self.create_location_info_section(property_data)
        
        # Features
        self.create_features_section(property_data)
        
        # Media gallery
        self.create_media_section(property_data)
        
        # Action buttons
        self.create_detail_action_buttons(property_data)
    
    def create_basic_info_section(self, property_data: Dict[str, Any]):
        """
        Create basic information section
        
        Args:
            property_data: Property data dictionary
        """
        info_frame = ttk.LabelFrame(self.detail_frame, text="Basic Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create info rows
        info_items = [
            ("Title", property_data.get('title', 'N/A')),
            ("Type", property_data.get('property_type', 'N/A')),
            ("Transaction", property_data.get('transaction_type', 'N/A')),
            ("Price", f"€{property_data.get('price', 0):,.0f}" if property_data.get('price') else 'N/A'),
            ("Surface Area", f"{property_data.get('surface_area', 0)} m²" if property_data.get('surface_area') else 'N/A'),
            ("Bedrooms", str(property_data.get('bedrooms', 'N/A'))),
            ("Bathrooms", str(property_data.get('bathrooms', 'N/A'))),
            ("Status", property_data.get('status', 'N/A')),
        ]
        
        for i, (label, value) in enumerate(info_items):
            row_frame = ttk.Frame(info_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=f"{label}:", 
                     font=('Segoe UI', 9, 'bold'), width=12).pack(side=tk.LEFT)
            ttk.Label(row_frame, text=str(value)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Description
        if property_data.get('description'):
            desc_frame = ttk.Frame(info_frame)
            desc_frame.pack(fill=tk.X, pady=(10, 0))
            
            ttk.Label(desc_frame, text="Description:", 
                     font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W)
            
            desc_text = tk.Text(desc_frame, height=4, wrap=tk.WORD, 
                               font=('Segoe UI', 9), state=tk.DISABLED)
            desc_text.pack(fill=tk.X, pady=(5, 0))
            
            desc_text.config(state=tk.NORMAL)
            desc_text.insert(tk.END, property_data['description'])
            desc_text.config(state=tk.DISABLED)
    
    def create_location_info_section(self, property_data: Dict[str, Any]):
        """
        Create location information section
        
        Args:
            property_data: Property data dictionary
        """
        location_frame = ttk.LabelFrame(self.detail_frame, text="Location", padding=10)
        location_frame.pack(fill=tk.X, padx=10, pady=5)
        
        location_items = [
            ("Address", property_data.get('address', 'N/A')),
            ("City", property_data.get('city', 'N/A')),
            ("Postal Code", property_data.get('postal_code', 'N/A')),
            ("Country", property_data.get('country', 'N/A')),
        ]
        
        for label, value in location_items:
            row_frame = ttk.Frame(location_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=f"{label}:", 
                     font=('Segoe UI', 9, 'bold'), width=12).pack(side=tk.LEFT)
            ttk.Label(row_frame, text=str(value)).pack(side=tk.LEFT, padx=(10, 0))
    
    def create_features_section(self, property_data: Dict[str, Any]):
        """
        Create features section
        
        Args:
            property_data: Property data dictionary
        """
        features = property_data.get('features', [])
        additional_features = property_data.get('additional_features', [])
        all_features = features + additional_features
        
        if all_features:
            features_frame = ttk.LabelFrame(self.detail_frame, text="Features", padding=10)
            features_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Create features grid
            features_container = ttk.Frame(features_frame)
            features_container.pack(fill=tk.X)
            
            for i, feature in enumerate(all_features):
                row = i // 2
                col = i % 2
                
                feature_label = ttk.Label(features_container, text=f"• {feature}")
                feature_label.grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=2)
    
    def create_media_section(self, property_data: Dict[str, Any]):
        """
        Create media section
        
        Args:
            property_data: Property data dictionary
        """
        media_files = self.property_manager.get_property_media(property_data['id'])
        
        if media_files:
            media_frame = ttk.LabelFrame(self.detail_frame, text="Media", padding=10)
            media_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Create media gallery
            try:
                self.media_gallery = MediaGallery(
                    media_frame, 
                    media_files=media_files,
                    readonly=True,
                    max_height=200
                )
            except Exception as e:
                ttk.Label(media_frame, text=f"Error loading media: {e}").pack()
    
    def create_detail_action_buttons(self, property_data: Dict[str, Any]):
        """
        Create action buttons in detail view
        
        Args:
            property_data: Property data dictionary
        """
        actions_frame = ttk.Frame(self.detail_frame)
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(actions_frame, text="Edit Property", 
                  command=self.edit_selected_property,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="Duplicate", 
                  command=self.duplicate_selected_property).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="Generate Website", 
                  command=self.generate_website).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="Export", 
                  command=self.export_selected_property).pack(side=tk.LEFT)
    
    # Action methods
    def new_property(self):
        """
        Open property creation wizard
        """
        if hasattr(self.main_window, 'new_property'):
            self.main_window.new_property()
    
    def edit_selected_property(self):
        """
        Edit selected property
        """
        if not self.selected_property_id:
            messagebox.showwarning("No Selection", "Please select a property to edit.")
            return
        
        try:
            # Open property wizard in edit mode
            if hasattr(self.main_window, 'property_wizard') and self.main_window.property_wizard:
                if self.main_window.property_wizard.window.winfo_exists():
                    self.main_window.property_wizard.window.destroy()
            
            from core.media_handler import MediaHandler
            media_handler = MediaHandler()
            
            self.main_window.property_wizard = PropertyWizard(
                self.main_window.root, 
                self.property_manager, 
                media_handler,
                self.on_property_saved
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open property editor: {e}")
    
    def duplicate_selected_property(self):
        """
        Duplicate selected property
        """
        if not self.selected_property_id:
            messagebox.showwarning("No Selection", "Please select a property to duplicate.")
            return
        
        try:
            new_property_id = self.property_manager.duplicate_property(self.selected_property_id)
            if new_property_id:
                messagebox.showinfo("Success", f"Property duplicated successfully (New ID: {new_property_id})")
                self.refresh_properties_list()
                if hasattr(self.main_window, 'dashboard') and self.main_window.dashboard:
                    self.main_window.dashboard.refresh()
            else:
                messagebox.showerror("Error", "Failed to duplicate property.")
        except Exception as e:
            messagebox.showerror("Error", f"Error duplicating property: {e}")
    
    def delete_selected_property(self):
        """
        Delete selected property
        """
        if not self.selected_property_id or not self.selected_property_data:
            messagebox.showwarning("No Selection", "Please select a property to delete.")
            return
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete property '{self.selected_property_data['title']}'?\n\n"
            "This action cannot be undone and will remove all associated media files."
        )
        
        if result:
            try:
                success = self.property_manager.delete_property_with_media(self.selected_property_id)
                
                if success:
                    messagebox.showinfo("Success", "Property deleted successfully")
                    self.refresh_properties_list()
                    self.show_no_selection_message()
                    if hasattr(self.main_window, 'dashboard') and self.main_window.dashboard:
                        self.main_window.dashboard.refresh()
                else:
                    messagebox.showerror("Error", "Failed to delete property.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting property: {e}")
    
    def generate_website(self):
        """
        Generate website for selected property
        """
        if not self.selected_property_id:
            messagebox.showwarning("No Selection", "Please select a property to generate website.")
            return
        
        messagebox.showinfo("Generate Website", f"Generate website for property {self.selected_property_id} - Coming soon...")
    
    def export_selected_property(self):
        """
        Export selected property
        """
        if not self.selected_property_id:
            messagebox.showwarning("No Selection", "Please select a property to export.")
            return
        
        export_path = filedialog.askdirectory(
            title="Select Export Directory",
            initialdir=str(Path.home())
        )
        
        if export_path:
            try:
                success = self.property_manager.export_property_data(
                    self.selected_property_id, export_path
                )
                
                if success:
                    messagebox.showinfo("Success", "Property exported successfully.")
                else:
                    messagebox.showerror("Error", "Failed to export property.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting property: {e}")
    
    def on_property_saved(self, property_id: int):
        """
        Callback when property is saved
        
        Args:
            property_id: ID of saved property
        """
        self.refresh_properties_list()
        
        # Select the saved property
        for item in self.properties_tree.get_children():
            if self.properties_tree.item(item)['values'][0] == property_id:
                self.properties_tree.selection_set(item)
                self.properties_tree.focus(item)
                break
        
        if hasattr(self.main_window, 'dashboard') and self.main_window.dashboard:
            self.main_window.dashboard.refresh()