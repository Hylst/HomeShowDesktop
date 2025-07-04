#!/usr/bin/env python3
"""
Dashboard for HomeShow Desktop
Main dashboard interface showing property statistics and quick actions

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Dict, Any, Optional, List
import webbrowser
import sys
from gui.components.property_manager_interface import PropertyManagerInterface

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.localization import translate

class Dashboard:
    """
    Dashboard interface for property overview and quick actions
    """
    
    def __init__(self, parent_frame, property_manager, main_window):
        """
        Initialize dashboard
        
        Args:
            parent_frame: Parent tkinter frame
            property_manager: PropertyManager instance
            main_window: Reference to main window
        """
        self.parent_frame = parent_frame
        self.property_manager = property_manager
        self.main_window = main_window
        
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """
        Create dashboard interface
        """
        # Main container with scrollable content
        self.canvas = tk.Canvas(self.parent_frame, bg='white')
        self.scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.canvas.yview)
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
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Create dashboard content
        self.create_header()
        self.create_statistics_section()
        self.create_quick_actions_section()
        self.create_recent_properties_section()
        self.create_tips_section()
    
    def _on_mousewheel(self, event):
        """
        Handle mouse wheel scrolling
        
        Args:
            event: Mouse wheel event
        """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_header(self):
        """
        Create dashboard header
        """
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Welcome message
        self.welcome_label = ttk.Label(
            header_frame,
            text=translate('dashboard_welcome'),
            font=('Segoe UI', 20, 'bold')
        )
        self.welcome_label.pack(anchor=tk.W)
        
        self.subtitle_label = ttk.Label(
            header_frame,
            text=translate('dashboard_subtitle'),
            font=('Segoe UI', 12),
            foreground='gray'
        )
        self.subtitle_label.pack(anchor=tk.W, pady=(5, 0))
    
    def create_statistics_section(self):
        """
        Create statistics cards section
        """
        self.stats_frame = ttk.LabelFrame(self.scrollable_frame, text=translate('dashboard_stats'), padding=15)
        self.stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Statistics container
        self.stats_container = ttk.Frame(self.stats_frame)
        self.stats_container.pack(fill=tk.X)
        
        # Create placeholder cards
        self.create_stat_cards()
    
    def create_stat_cards(self):
        """
        Create statistics cards
        """
        # Clear existing cards
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        
        # Get statistics
        stats = self.property_manager.get_property_statistics()
        
        # Define card data
        cards_data = [
            {
                'title': 'Total Properties',
                'value': str(stats['total_properties']),
                'color': '#4CAF50',
                'icon': '🏠'
            },
            {
                'title': 'Total Value',
                'value': f"€{stats['total_value']:,.0f}" if stats['total_value'] > 0 else 'N/A',
                'color': '#2196F3',
                'icon': '💰'
            },
            {
                'title': 'Average Price',
                'value': f"€{stats['average_price']:,.0f}" if stats['average_price'] > 0 else 'N/A',
                'color': '#FF9800',
                'icon': '📊'
            },
            {
                'title': 'Media Files',
                'value': str(stats['total_media_files']),
                'color': '#9C27B0',
                'icon': '📷'
            }
        ]
        
        # Create cards in a grid
        for i, card_data in enumerate(cards_data):
            self.create_stat_card(self.stats_container, card_data, i)
    
    def create_stat_card(self, parent, card_data: Dict[str, str], index: int):
        """
        Create individual statistics card
        
        Args:
            parent: Parent widget
            card_data: Card data dictionary
            index: Card index for positioning
        """
        # Card frame
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.grid(row=0, column=index, padx=10, pady=5, sticky='ew')
        
        # Configure grid weight
        parent.grid_columnconfigure(index, weight=1)
        
        # Card content
        content_frame = ttk.Frame(card_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icon and value
        header_frame = ttk.Frame(content_frame)
        header_frame.pack(fill=tk.X)
        
        icon_label = ttk.Label(
            header_frame,
            text=card_data['icon'],
            font=('Segoe UI', 24)
        )
        icon_label.pack(side=tk.LEFT)
        
        value_label = ttk.Label(
            header_frame,
            text=card_data['value'],
            font=('Segoe UI', 18, 'bold')
        )
        value_label.pack(side=tk.RIGHT)
        
        # Title
        title_label = ttk.Label(
            content_frame,
            text=card_data['title'],
            font=('Segoe UI', 10),
            foreground='gray'
        )
        title_label.pack(anchor=tk.W, pady=(10, 0))
    
    def create_quick_actions_section(self):
        """
        Create quick actions section
        """
        self.actions_frame = ttk.LabelFrame(self.scrollable_frame, text=translate('dashboard_quick_actions'), padding=15)
        self.actions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Actions container
        actions_container = ttk.Frame(self.actions_frame)
        actions_container.pack(fill=tk.X)
        
        # Action buttons
        actions = [
            {
                'text': translate('dashboard_new_property'),
                'command': self.main_window.new_property,
                'style': 'Primary.TButton'
            },
            {
                'text': 'Manage Properties',
                'command': self.open_property_manager,
                'style': 'Secondary.TButton'
            },
            {
                'text': translate('dashboard_generate_website'),
                'command': self.main_window.generate_website,
                'style': 'Secondary.TButton'
            },
            {
                'text': translate('dashboard_ai_staging'),
                'command': self.main_window.ai_staging,
                'style': 'Secondary.TButton'
            },
            {
                'text': translate('dashboard_import_property'),
                'command': self.main_window.import_property,
                'style': 'Secondary.TButton'
            }
        ]
        
        for i, action in enumerate(actions):
            btn = ttk.Button(
                actions_container,
                text=action['text'],
                command=action['command'],
                style=action['style'],
                width=20
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            actions_container.grid_columnconfigure(i, weight=1)
    
    def open_property_manager(self):
        """
        Open the property manager interface
        """
        property_manager_window = tk.Toplevel(self.main_window.root)
        property_manager_window.title("Property Manager")
        property_manager_window.geometry("900x600")
        property_manager_window.minsize(800, 500)
        
        # Create property manager interface
        PropertyManagerInterface(property_manager_window, self.property_manager, self.main_window)
    
    def create_recent_properties_section(self):
        """
        Create recent properties section
        """
        recent_frame = ttk.LabelFrame(self.scrollable_frame, text="Recent Properties", padding=15)
        recent_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Recent properties container
        self.recent_container = ttk.Frame(recent_frame)
        self.recent_container.pack(fill=tk.BOTH, expand=True)
        
        # Load recent properties
        self.load_recent_properties()
    
    def load_recent_properties(self):
        """
        Load and display recent properties
        """
        # Clear existing content
        for widget in self.recent_container.winfo_children():
            widget.destroy()
        
        # Get recent properties (last 5)
        properties = self.property_manager.get_all_property_summaries()[:5]
        
        if not properties:
            # No properties message
            no_props_label = ttk.Label(
                self.recent_container,
                text="No properties yet. Create your first property to get started!",
                font=('Segoe UI', 12),
                foreground='gray'
            )
            no_props_label.pack(pady=20)
            
            create_btn = ttk.Button(
                self.recent_container,
                text="Create First Property",
                command=self.main_window.new_property,
                style='Primary.TButton'
            )
            create_btn.pack()
        else:
            # Properties list
            for i, prop in enumerate(properties):
                self.create_property_card(self.recent_container, prop, i)
    
    def create_property_card(self, parent, property_data: Dict[str, Any], index: int):
        """
        Create property card for recent properties
        
        Args:
            parent: Parent widget
            property_data: Property data
            index: Card index
        """
        # Card frame
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.pack(fill=tk.X, pady=5)
        
        # Card content
        content_frame = ttk.Frame(card_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Left side - Property info
        info_frame = ttk.Frame(content_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Property title
        title_label = ttk.Label(
            info_frame,
            text=property_data['title'],
            font=('Segoe UI', 12, 'bold')
        )
        title_label.pack(anchor=tk.W)
        
        # Property details
        details = []
        if property_data.get('property_type'):
            details.append(property_data['property_type'])
        if property_data.get('city'):
            details.append(property_data['city'])
        if property_data.get('price'):
            details.append(f"€{property_data['price']:,.0f}")
        
        if details:
            details_text = " • ".join(details)
            details_label = ttk.Label(
                info_frame,
                text=details_text,
                font=('Segoe UI', 10),
                foreground='gray'
            )
            details_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Property stats
        stats_text = f"{property_data.get('rooms', 0)} rooms"
        if property_data.get('surface_area'):
            stats_text += f" • {property_data['surface_area']} m²"
        if property_data.get('image_count', 0) > 0:
            stats_text += f" • {property_data['image_count']} photos"
        
        stats_label = ttk.Label(
            info_frame,
            text=stats_text,
            font=('Segoe UI', 9),
            foreground='gray'
        )
        stats_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Right side - Actions
        actions_frame = ttk.Frame(content_frame)
        actions_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Status badge
        status_color = {
            'draft': '#FFC107',
            'published': '#4CAF50',
            'archived': '#9E9E9E'
        }.get(property_data.get('status', 'draft'), '#FFC107')
        
        status_label = ttk.Label(
            actions_frame,
            text=property_data.get('status', 'draft').upper(),
            font=('Segoe UI', 8, 'bold'),
            foreground='white',
            background=status_color
        )
        status_label.pack(pady=(0, 5))
        
        # Action buttons
        edit_btn = ttk.Button(
            actions_frame,
            text="Edit",
            command=lambda p_id=property_data['id']: self.edit_property(p_id),
            width=8
        )
        edit_btn.pack(pady=2)
        
        generate_btn = ttk.Button(
            actions_frame,
            text="Generate",
            command=lambda p_id=property_data['id']: self.generate_website(p_id),
            width=8
        )
        generate_btn.pack(pady=2)
    
    def create_tips_section(self):
        """
        Create tips and help section
        """
        tips_frame = ttk.LabelFrame(self.scrollable_frame, text="Tips & Resources", padding=15)
        tips_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Tips container
        tips_container = ttk.Frame(tips_frame)
        tips_container.pack(fill=tk.X)
        
        # Tips list
        tips = [
            {
                'icon': '💡',
                'title': 'Getting Started',
                'text': 'Create your first property and add high-quality photos for best results.',
                'action': ('Learn More', self.show_getting_started)
            },
            {
                'icon': '📸',
                'title': 'Photo Tips',
                'text': 'Use natural lighting and wide-angle shots to showcase spaces effectively.',
                'action': ('Photo Guide', self.show_photo_guide)
            },
            {
                'icon': '🎨',
                'title': 'AI Staging',
                'text': 'Transform empty rooms with AI-powered virtual staging for better appeal.',
                'action': ('Try AI Staging', self.main_window.ai_staging)
            }
        ]
        
        for i, tip in enumerate(tips):
            self.create_tip_card(tips_container, tip, i)
    
    def create_tip_card(self, parent, tip_data: Dict[str, Any], index: int):
        """
        Create tip card
        
        Args:
            parent: Parent widget
            tip_data: Tip data
            index: Card index
        """
        # Card frame
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.grid(row=index//2, column=index%2, padx=5, pady=5, sticky='ew')
        
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Card content
        content_frame = ttk.Frame(card_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Header with icon and title
        header_frame = ttk.Frame(content_frame)
        header_frame.pack(fill=tk.X)
        
        icon_label = ttk.Label(
            header_frame,
            text=tip_data['icon'],
            font=('Segoe UI', 16)
        )
        icon_label.pack(side=tk.LEFT)
        
        title_label = ttk.Label(
            header_frame,
            text=tip_data['title'],
            font=('Segoe UI', 11, 'bold')
        )
        title_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Tip text
        text_label = ttk.Label(
            content_frame,
            text=tip_data['text'],
            font=('Segoe UI', 9),
            foreground='gray',
            wraplength=250
        )
        text_label.pack(anchor=tk.W, pady=(5, 10))
        
        # Action button
        if tip_data.get('action'):
            action_text, action_command = tip_data['action']
            action_btn = ttk.Button(
                content_frame,
                text=action_text,
                command=action_command,
                style='Secondary.TButton'
            )
            action_btn.pack(anchor=tk.W)
    
    def refresh(self):
        """
        Refresh dashboard data
        """
        self.create_stat_cards()
        self.load_recent_properties()
    
    def refresh_language(self):
        """
        Refresh dashboard with new language.
        """
        # Update welcome text
        if hasattr(self, 'welcome_label'):
            self.welcome_label.config(text=translate('dashboard_welcome'))
        
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.config(text=translate('dashboard_subtitle'))
        
        # Update section titles
        if hasattr(self, 'stats_frame'):
            self.stats_frame.config(text=translate('dashboard_stats'))
        
        if hasattr(self, 'actions_frame'):
            self.actions_frame.config(text=translate('dashboard_quick_actions'))
        
        if hasattr(self, 'recent_frame'):
            self.recent_frame.config(text=translate('dashboard_recent_properties'))
        
        if hasattr(self, 'tips_frame'):
            self.tips_frame.config(text=translate('dashboard_tips'))
        
        # Update button texts
        if hasattr(self, 'create_btn'):
            self.create_btn.config(text=translate('dashboard_create_property'))
        
        if hasattr(self, 'import_btn'):
            self.import_btn.config(text=translate('dashboard_import_data'))
        
        if hasattr(self, 'generate_btn'):
            self.generate_btn.config(text=translate('dashboard_generate_website'))
        
        # Refresh statistics with new labels
        self.create_stat_cards()
        
        # Refresh recent properties
        self.load_recent_properties()
    
    # Action handlers
    def edit_property(self, property_id: int):
        """
        Edit property
        
        Args:
            property_id: Property ID
        """
        messagebox.showinfo("Edit Property", f"Edit property {property_id} - Coming soon...")
    
    def generate_website(self, property_id: int):
        """
        Generate website for property
        
        Args:
            property_id: Property ID
        """
        messagebox.showinfo("Generate Website", f"Generate website for property {property_id} - Coming soon...")
    
    def show_getting_started(self):
        """
        Show getting started guide
        """
        help_text = """
Getting Started with HomeShow Desktop

1. Create Your First Property
   • Click "New Property" to start the wizard
   • Fill in basic information (title, type, price)
   • Add high-quality photos and media

2. Organize Your Content
   • Add detailed descriptions
   • Include floor plans if available
   • Set property features and amenities

3. Generate Your Website
   • Choose from professional templates
   • Customize colors and layout
   • Generate and preview your site

4. Publish and Share
   • Export your website files
   • Upload to your hosting provider
   • Share with clients and prospects

Tips for Success:
• Use high-resolution images (1920x1080 or higher)
• Include virtual tours or 360° photos when possible
• Write compelling property descriptions
• Keep information accurate and up-to-date
        """
        
        messagebox.showinfo("Getting Started Guide", help_text)
    
    def show_photo_guide(self):
        """
        Show photo guide
        """
        help_text = """
Property Photography Best Practices

📸 Camera Settings:
• Use wide-angle lens (14-24mm)
• Shoot in RAW format for better editing
• Use tripod for stability
• HDR for high contrast scenes

💡 Lighting Tips:
• Natural light is best - shoot during golden hour
• Turn on all lights in the room
• Avoid harsh shadows
• Use flash sparingly

🏠 Composition:
• Shoot from corners to show room size
• Include ceiling in shots when possible
• Keep vertical lines straight
• Declutter and stage rooms

📱 Mobile Photography:
• Clean your lens before shooting
• Use grid lines for composition
• Take multiple shots of each room
• Edit for brightness and contrast

✨ Post-Processing:
• Adjust exposure and highlights
• Enhance colors naturally
• Straighten horizons
• Remove distracting elements
        """
        
        messagebox.showinfo("Photography Guide", help_text)