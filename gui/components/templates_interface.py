#!/usr/bin/env python3
"""
Templates Interface for HomeShow Desktop
Manages website templates and property listing templates

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from core.localization import translate


class TemplatesInterface:
    """
    Interface for managing website and property templates
    """
    
    def __init__(self, parent):
        """
        Initialize templates interface
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.create_interface()
    
    def create_interface(self):
        """
        Create the templates interface
        """
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text=translate("templates_title"), 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text=translate("templates_new"),
                  command=self.new_template).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text=translate("templates_import"),
                  command=self.import_template).pack(side=tk.LEFT)
        
        # Template categories
        self.create_template_categories(main_frame)
    
    def create_template_categories(self, parent):
        """
        Create template categories with tabs
        
        Args:
            parent: Parent widget
        """
        # Notebook for different template types
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Website templates tab
        self.create_website_templates_tab()
        
        # Property listing templates tab
        self.create_property_templates_tab()
        
        # Email templates tab
        self.create_email_templates_tab()
    
    def create_website_templates_tab(self):
        """
        Create website templates tab
        """
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=translate("templates_website"))
        
        # Templates grid
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sample website templates
        website_templates = [
            {
                "name": "Modern Luxury",
                "description": "Clean, modern design perfect for luxury properties",
                "preview": "🏢",
                "features": ["Responsive", "Image Gallery", "Contact Forms"]
            },
            {
                "name": "Classic Elegance",
                "description": "Traditional design with elegant typography",
                "preview": "🏛️",
                "features": ["Professional", "Print-friendly", "SEO Optimized"]
            },
            {
                "name": "Minimalist",
                "description": "Simple, clean design focusing on content",
                "preview": "⬜",
                "features": ["Fast Loading", "Mobile First", "Accessibility"]
            },
            {
                "name": "Real Estate Pro",
                "description": "Professional template for real estate agencies",
                "preview": "🏘️",
                "features": ["Multi-listing", "Search Filters", "Agent Profiles"]
            }
        ]
        
        self.create_template_grid(scrollable_frame, website_templates, "website")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_property_templates_tab(self):
        """
        Create property listing templates tab
        """
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=translate("templates_property"))
        
        # Templates grid
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sample property templates
        property_templates = [
            {
                "name": "Residential Standard",
                "description": "Standard template for residential properties",
                "preview": "🏠",
                "features": ["Room Details", "Amenities", "Neighborhood Info"]
            },
            {
                "name": "Commercial Listing",
                "description": "Template designed for commercial properties",
                "preview": "🏢",
                "features": ["Floor Plans", "Zoning Info", "Investment Details"]
            },
            {
                "name": "Luxury Showcase",
                "description": "Premium template for high-end properties",
                "preview": "💎",
                "features": ["Virtual Tour", "Video Gallery", "Concierge Info"]
            },
            {
                "name": "Rental Property",
                "description": "Template optimized for rental listings",
                "preview": "🔑",
                "features": ["Lease Terms", "Availability", "Application Form"]
            }
        ]
        
        self.create_template_grid(scrollable_frame, property_templates, "property")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_email_templates_tab(self):
        """
        Create email templates tab
        """
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=translate("templates_email"))
        
        # Templates list
        list_frame = ttk.Frame(tab_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Email templates treeview
        columns = ('name', 'subject', 'type', 'modified')
        self.email_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.email_tree.heading('name', text=translate("templates_name"))
        self.email_tree.heading('subject', text=translate("templates_subject"))
        self.email_tree.heading('type', text=translate("templates_type"))
        self.email_tree.heading('modified', text=translate("templates_modified"))
        
        self.email_tree.column('name', width=200)
        self.email_tree.column('subject', width=300)
        self.email_tree.column('type', width=150)
        self.email_tree.column('modified', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.email_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.email_tree.xview)
        
        self.email_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.email_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load sample email templates
        self.load_sample_email_templates()
        
        # Bind events
        self.email_tree.bind('<Double-1>', self.edit_email_template)
    
    def create_template_grid(self, parent, templates, template_type):
        """
        Create a grid of template cards
        
        Args:
            parent: Parent widget
            templates: List of template dictionaries
            template_type: Type of templates (website, property)
        """
        row = 0
        col = 0
        max_cols = 2
        
        for template in templates:
            # Template card frame
            card_frame = ttk.LabelFrame(parent, text=template["name"], padding=15)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            # Preview icon
            preview_label = ttk.Label(card_frame, text=template["preview"], 
                                    font=("Arial", 24))
            preview_label.pack(pady=(0, 10))
            
            # Description
            desc_label = ttk.Label(card_frame, text=template["description"], 
                                 wraplength=200, justify=tk.CENTER)
            desc_label.pack(pady=(0, 10))
            
            # Features
            features_frame = ttk.Frame(card_frame)
            features_frame.pack(pady=(0, 10))
            
            for feature in template["features"]:
                feature_label = ttk.Label(features_frame, text=f"• {feature}", 
                                        font=("Arial", 8))
                feature_label.pack(anchor=tk.W)
            
            # Action buttons
            button_frame = ttk.Frame(card_frame)
            button_frame.pack(fill=tk.X)
            
            ttk.Button(button_frame, text=translate("templates_preview"),
                      command=lambda t=template: self.preview_template(t, template_type)).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(button_frame, text=translate("templates_use"),
                      command=lambda t=template: self.use_template(t, template_type)).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(button_frame, text=translate("templates_edit"),
                      command=lambda t=template: self.edit_template(t, template_type)).pack(side=tk.LEFT)
            
            # Update grid position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(max_cols):
            parent.grid_columnconfigure(i, weight=1)
    
    def load_sample_email_templates(self):
        """
        Load sample email templates
        """
        sample_emails = [
            ("Welcome New Client", "Welcome to Our Real Estate Services", "Client Onboarding", "2024-01-15"),
            ("Property Inquiry Response", "Thank you for your interest in [Property]", "Inquiry Response", "2024-01-20"),
            ("Showing Confirmation", "Your property showing is confirmed", "Appointment", "2024-02-01"),
            ("Market Update", "Monthly Market Report - [Month]", "Newsletter", "2024-02-05"),
            ("Offer Submitted", "Your offer has been submitted", "Transaction", "2024-01-25"),
            ("Closing Reminder", "Upcoming closing - Important information", "Transaction", "2024-02-10")
        ]
        
        for email in sample_emails:
            self.email_tree.insert('', tk.END, values=email)
    
    def preview_template(self, template, template_type):
        """
        Preview a template
        
        Args:
            template: Template dictionary
            template_type: Type of template
        """
        messagebox.showinfo(
            translate("templates_preview"),
            f"Preview for {template['name']} ({template_type}) coming soon!"
        )
    
    def use_template(self, template, template_type):
        """
        Use a template
        
        Args:
            template: Template dictionary
            template_type: Type of template
        """
        messagebox.showinfo(
            translate("templates_use"),
            f"Using template {template['name']} ({template_type}) coming soon!"
        )
    
    def edit_template(self, template, template_type):
        """
        Edit a template
        
        Args:
            template: Template dictionary
            template_type: Type of template
        """
        messagebox.showinfo(
            translate("templates_edit"),
            f"Editing template {template['name']} ({template_type}) coming soon!"
        )
    
    def edit_email_template(self, event=None):
        """
        Edit selected email template
        
        Args:
            event: Event object
        """
        selection = self.email_tree.selection()
        if selection:
            item = self.email_tree.item(selection[0])
            template_name = item['values'][0]
            messagebox.showinfo(
                translate("templates_edit"),
                f"Editing email template '{template_name}' coming soon!"
            )
    
    def new_template(self):
        """
        Create new template
        """
        messagebox.showinfo(translate("templates_new"), translate("templates_new_coming_soon"))
    
    def import_template(self):
        """
        Import template
        """
        messagebox.showinfo(translate("templates_import"), translate("templates_import_coming_soon"))