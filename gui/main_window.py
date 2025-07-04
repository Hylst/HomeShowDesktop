#!/usr/bin/env python3
"""
Main Window for HomeShow Desktop
Primary GUI interface with navigation and main functionality

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Import application modules
sys.path.append(str(Path(__file__).parent.parent))

from core.database import DatabaseManager
from core.property_manager import PropertyManager
from gui.dashboard import Dashboard
from gui.property_wizard import PropertyWizard
from gui.components.property_manager_interface import PropertyManagerInterface
from gui.preferences_dialog import PreferencesDialog
from gui.components.projects_interface import ProjectsInterface
from gui.components.templates_interface import TemplatesInterface
from core.localization import get_localization_manager, translate, set_language

class MainWindow:
    """
    Main application window with tabbed interface
    """
    
    def __init__(self):
        """
        Initialize main window
        """
        self.root = tk.Tk()
        
        # Initialize localization
        self.localization = get_localization_manager()
        
        self.setup_window()
        self.setup_styles()
        
        # Initialize core components
        self.db_manager = DatabaseManager()
        self.property_manager = PropertyManager(self.db_manager)
        
        # GUI components
        self.dashboard = None
        self.property_wizard = None
        
        # Setup interface
        self.create_menu()
        self.create_main_interface()
        
        # Initialize dashboard
        self.show_dashboard()
    
    def setup_window(self):
        """
        Configure main window properties
        """
        self.root.title("HomeShow Desktop - Real Estate Website Generator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Center window on screen
        self.center_window()
    
    def update_window_title(self):
        """
        Update the window title with localized text.
        """
        title = f"{translate('app_title')} - {translate('app_subtitle')}"
        self.root.title(title)
    
    def change_language(self, language_code):
        """
        Change the application language and refresh the interface.
        
        Args:
            language_code: Language code ('en' or 'fr')
        """
        set_language(language_code)
        self.refresh_interface()
    
    def refresh_interface(self):
        """
        Refresh the entire interface with new language.
        """
        # Update window title
        self.update_window_title()
        
        # Recreate menu
        self.create_menu()
        
        # Refresh notebook tabs
        self.refresh_tabs()
        
        # Refresh dashboard with new language
        if hasattr(self, 'dashboard') and self.dashboard:
            self.dashboard.refresh_language()
    
    def refresh_tabs(self):
        """
        Refresh notebook tab labels.
        """
        if hasattr(self, 'notebook'):
            # Update tab texts
            self.notebook.tab(0, text=translate('tab_dashboard'))
            self.notebook.tab(1, text=translate('tab_properties'))
            self.notebook.tab(2, text=translate('tab_projects'))
            self.notebook.tab(3, text=translate('tab_templates'))
        
        # Set window icon (if available)
        try:
            icon_path = Path(__file__).parent.parent / "resources" / "icons" / "app_icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """
        Center the window on the screen
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):
        """
        Configure ttk styles for modern appearance
        """
        style = ttk.Style()
        
        # Configure notebook (tabs) style
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Configure button styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Secondary.TButton', font=('Segoe UI', 9))
        
        # Configure frame styles
        style.configure('Card.TFrame', relief='solid', borderwidth=1)
        style.configure('Sidebar.TFrame', background='#e8e8e8')
    
    def create_menu(self):
        """
        Create application menu bar
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translate('menu_file'), menu=file_menu)
        file_menu.add_command(label=translate('menu_new'), command=self.new_property, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label=translate('menu_import'), command=self.import_property)
        file_menu.add_command(label=translate('menu_export'), command=self.export_property)
        file_menu.add_separator()
        file_menu.add_command(label=translate('menu_exit'), command=self.on_closing, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translate('menu_edit'), menu=edit_menu)
        edit_menu.add_command(label=translate('menu_preferences'), command=self.show_preferences)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translate('menu_tools'), menu=tools_menu)
        tools_menu.add_command(label=translate('menu_generate_website'), command=self.generate_website)
        tools_menu.add_command(label=translate('menu_ai_staging'), command=self.ai_staging)
        tools_menu.add_separator()
        tools_menu.add_command(label=translate('menu_backup_database'), command=self.backup_database)
        
        # Language menu
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translate('menu_language'), menu=language_menu)
        language_menu.add_command(label=translate('menu_english'), command=lambda: self.change_language('en'))
        language_menu.add_command(label=translate('menu_french'), command=lambda: self.change_language('fr'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translate('menu_help'), menu=help_menu)
        help_menu.add_command(label=translate('menu_user_guide'), command=self.show_help)
        help_menu.add_command(label=translate('menu_about'), command=self.show_about)
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_property())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
    
    def create_main_interface(self):
        """
        Create the main interface with tabbed navigation
        """
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dashboard tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text=translate('tab_dashboard'))
        
        # Properties tab
        self.properties_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.properties_frame, text=translate('tab_properties'))
        
        # Projects tab
        self.projects_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.projects_frame, text=translate('tab_projects'))
        
        # Templates tab
        self.templates_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.templates_frame, text=translate('tab_templates'))
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_status_bar(self, parent):
        """
        Create status bar at bottom of window
        
        Args:
            parent: Parent widget
        """
        self.status_bar = ttk.Frame(parent)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Status label
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar (hidden by default)
        self.progress_bar = ttk.Progressbar(self.status_bar, mode='indeterminate')
        
        # Version info
        version_label = ttk.Label(self.status_bar, text="v1.0.0")
        version_label.pack(side=tk.RIGHT)
    
    def show_dashboard(self):
        """
        Initialize and show dashboard
        """
        if self.dashboard is None:
            self.dashboard = Dashboard(self.dashboard_frame, self.property_manager, self)
        self.dashboard.refresh()
    
    def show_properties(self):
        """
        Show properties management interface
        """
        # Clear existing content
        for widget in self.properties_frame.winfo_children():
            widget.destroy()
        
        # Create advanced properties interface
        self.property_manager_interface = PropertyManagerInterface(
            self.properties_frame, 
            self.property_manager, 
            self
        )
        
        # Add manage properties button
        manage_frame = ttk.Frame(self.properties_frame)
        manage_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(manage_frame, text=translate("manage_properties"),
                  command=self.open_property_wizard).pack(side=tk.LEFT)
    
    def refresh_properties_interface(self):
        """
        Refresh the properties interface if it exists
        """
        if hasattr(self, 'property_manager_interface'):
            self.property_manager_interface.refresh_properties_list()
    

    
    def new_property(self):
        """
        Open property creation wizard
        """
        if self.property_wizard is None or not self.property_wizard.window.winfo_exists():
            self.property_wizard = PropertyWizard(self.root, self.property_manager, self.on_property_saved)
        else:
            self.property_wizard.window.lift()
    
    def on_property_saved(self, property_id: int):
        """
        Callback when property is saved
        
        Args:
            property_id: ID of saved property
        """
        self.set_status(f"Property saved successfully (ID: {property_id})")
        
        # Refresh dashboard and properties interface
        if self.dashboard:
            self.dashboard.refresh()
        
        # Refresh properties interface if it exists
        self.refresh_properties_interface()
    
    def on_settings_changed(self, settings):
        """
        Callback when settings are changed in preferences dialog
        
        Args:
            settings: Updated settings dictionary
        """
        # Refresh interface to apply new settings
        self.refresh_interface()
        self.set_status("Settings updated successfully")
    
    def open_property_wizard(self):
        """
        Open the property creation wizard
        """
        try:
            from core.media_handler import MediaHandler
            media_handler = MediaHandler()
            wizard = PropertyWizard(
                self.root,
                self.property_manager,
                media_handler,
                on_complete=self.on_property_saved
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open property wizard: {e}")
    
    def on_tab_changed(self, event):
        """
        Handle tab change events
        
        Args:
            event: Tab change event
        """
        selected_index = self.notebook.index(self.notebook.select())
        
        if selected_index == 0:  # Dashboard
            self.show_dashboard()
        elif selected_index == 1:  # Properties
            self.show_properties()
        elif selected_index == 2:  # Projects
            self.show_projects()
        elif selected_index == 3:  # Templates
            self.show_templates()
    
    def show_projects(self):
        """
        Show projects interface
        """
        # Clear existing content
        for widget in self.projects_frame.winfo_children():
            widget.destroy()
        
        # Create projects interface
        self.projects_interface = ProjectsInterface(self.projects_frame)
    
    def show_templates(self):
        """
        Show templates interface
        """
        # Clear existing content
        for widget in self.templates_frame.winfo_children():
            widget.destroy()
        
        # Create templates interface
        self.templates_interface = TemplatesInterface(self.templates_frame)
    
    def set_status(self, message: str, show_progress: bool = False):
        """
        Update status bar message
        
        Args:
            message: Status message
            show_progress: Whether to show progress bar
        """
        self.status_label.config(text=message)
        
        if show_progress:
            self.progress_bar.pack(side=tk.LEFT, padx=(10, 0))
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
        
        self.root.update_idletasks()
    
    # Menu command implementations
    def import_property(self):
        """
        Import property from file
        """
        folder_path = filedialog.askdirectory(
            title="Select Property Export Folder",
            initialdir=str(Path.home())
        )
        
        if folder_path:
            self.set_status("Importing property...", True)
            
            try:
                property_id = self.property_manager.import_property_data(folder_path)
                
                if property_id:
                    self.set_status(f"Property imported successfully (ID: {property_id})")
                    self.refresh_properties_list()
                    if self.dashboard:
                        self.dashboard.refresh()
                else:
                    self.set_status("Failed to import property")
                    messagebox.showerror("Import Error", "Failed to import property data.")
                    
            except Exception as e:
                self.set_status("Import failed")
                messagebox.showerror("Import Error", f"Error importing property: {e}")
    
    def export_property(self):
        """
        Export selected property
        """
        messagebox.showinfo("Export", "Please select a property from the Properties tab to export.")
    
    def show_preferences(self):
        """
        Show preferences dialog
        """
        try:
            PreferencesDialog(self.root, on_settings_changed=self.on_settings_changed)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open preferences: {e}")
    
    def generate_website(self):
        """
        Generate website for selected property
        """
        messagebox.showinfo("Generate Website", "Website generation coming soon...")
    
    def ai_staging(self):
        """
        Open AI staging interface
        """
        messagebox.showinfo("AI Staging", "AI Virtual Staging interface coming soon...")
    
    def backup_database(self):
        """
        Backup database
        """
        backup_path = filedialog.asksaveasfilename(
            title="Save Database Backup",
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        
        if backup_path:
            try:
                import shutil
                db_path = Path(__file__).parent.parent / "data" / "database.db"
                shutil.copy2(db_path, backup_path)
                messagebox.showinfo("Backup", "Database backup created successfully.")
            except Exception as e:
                messagebox.showerror("Backup Error", f"Failed to create backup: {e}")
    
    def show_help(self):
        """
        Show help documentation
        """
        messagebox.showinfo("Help", "User guide coming soon...")
    
    def show_about(self):
        """
        Show about dialog
        """
        about_text = """
HomeShow Desktop v1.0.0

Real Estate Website Generator

A powerful desktop application for creating
professional real estate websites with ease.

Features:
• Property management
• Website generation
• AI virtual staging
• Multiple templates
• Media optimization

Developed with Python and Tkinter
        """
        messagebox.showinfo("About HomeShow Desktop", about_text)
    
    # Properties list context menu handlers
    def show_properties_context_menu(self, event):
        """
        Show context menu for properties list
        
        Args:
            event: Right-click event
        """
        # Select item under cursor
        item = self.properties_tree.identify_row(event.y)
        if item:
            self.properties_tree.selection_set(item)
            self.properties_context_menu.post(event.x_root, event.y_root)
    
    def edit_selected_property(self):
        """
        Edit selected property
        """
        selection = self.properties_tree.selection()
        if selection:
            item = selection[0]
            property_id = self.properties_tree.item(item)['values'][0]
            # TODO: Open property editor
            messagebox.showinfo("Edit", f"Edit property {property_id} - Coming soon...")
    
    def duplicate_selected_property(self):
        """
        Duplicate selected property
        """
        selection = self.properties_tree.selection()
        if selection:
            item = selection[0]
            property_id = self.properties_tree.item(item)['values'][0]
            
            try:
                new_property_id = self.property_manager.duplicate_property(property_id)
                if new_property_id:
                    self.set_status(f"Property duplicated (New ID: {new_property_id})")
                    self.refresh_properties_list()
                    if self.dashboard:
                        self.dashboard.refresh()
                else:
                    messagebox.showerror("Error", "Failed to duplicate property.")
            except Exception as e:
                messagebox.showerror("Error", f"Error duplicating property: {e}")
    
    def generate_website_for_selected(self):
        """
        Generate website for selected property
        """
        selection = self.properties_tree.selection()
        if selection:
            item = selection[0]
            property_id = self.properties_tree.item(item)['values'][0]
            messagebox.showinfo("Generate", f"Generate website for property {property_id} - Coming soon...")
    
    def export_selected_property(self):
        """
        Export selected property
        """
        selection = self.properties_tree.selection()
        if selection:
            item = selection[0]
            property_id = self.properties_tree.item(item)['values'][0]
            
            export_path = filedialog.askdirectory(
                title="Select Export Directory",
                initialdir=str(Path.home())
            )
            
            if export_path:
                self.set_status("Exporting property...", True)
                
                try:
                    success = self.property_manager.export_property_data(
                        property_id, export_path
                    )
                    
                    if success:
                        self.set_status("Property exported successfully")
                        messagebox.showinfo("Export", "Property exported successfully.")
                    else:
                        self.set_status("Export failed")
                        messagebox.showerror("Export Error", "Failed to export property.")
                        
                except Exception as e:
                    self.set_status("Export failed")
                    messagebox.showerror("Export Error", f"Error exporting property: {e}")
    
    def delete_selected_property(self):
        """
        Delete selected property
        """
        selection = self.properties_tree.selection()
        if selection:
            item = selection[0]
            property_id = self.properties_tree.item(item)['values'][0]
            property_title = self.properties_tree.item(item)['values'][1]
            
            # Confirm deletion
            result = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete property '{property_title}'?\n\n"
                "This action cannot be undone and will remove all associated media files."
            )
            
            if result:
                try:
                    success = self.property_manager.delete_property_with_media(property_id)
                    
                    if success:
                        self.set_status("Property deleted successfully")
                        self.refresh_properties_list()
                        if self.dashboard:
                            self.dashboard.refresh()
                    else:
                        messagebox.showerror("Error", "Failed to delete property.")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting property: {e}")
    
    def on_closing(self):
        """
        Handle application closing
        """
        # Close database connection
        if hasattr(self, 'db_manager'):
            self.db_manager.close()
        
        # Destroy window
        self.root.destroy()
    
    def run(self):
        """
        Start the application main loop
        """
        self.root.mainloop()