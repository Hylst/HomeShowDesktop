#!/usr/bin/env python3
"""
Projects Interface for HomeShow Desktop
Manages real estate projects and campaigns

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from core.localization import translate


class ProjectsInterface:
    """
    Interface for managing real estate projects
    """
    
    def __init__(self, parent):
        """
        Initialize projects interface
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.create_interface()
    
    def create_interface(self):
        """
        Create the projects interface
        """
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text=translate("projects_title"), 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text=translate("projects_new"),
                  command=self.new_project).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text=translate("projects_import"),
                  command=self.import_project).pack(side=tk.LEFT)
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Projects list
        self.create_projects_list(content_frame)
        
        # Project details
        self.create_project_details(content_frame)
    
    def create_projects_list(self, parent):
        """
        Create projects list view
        
        Args:
            parent: Parent widget
        """
        # Left panel for projects list
        list_frame = ttk.LabelFrame(parent, text=translate("projects_list"), padding=10)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text=translate("projects_search")).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Projects treeview
        columns = ('name', 'status', 'properties', 'created')
        self.projects_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.projects_tree.heading('name', text=translate("projects_name"))
        self.projects_tree.heading('status', text=translate("projects_status"))
        self.projects_tree.heading('properties', text=translate("projects_properties_count"))
        self.projects_tree.heading('created', text=translate("projects_created"))
        
        self.projects_tree.column('name', width=200)
        self.projects_tree.column('status', width=100)
        self.projects_tree.column('properties', width=80)
        self.projects_tree.column('created', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.projects_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.projects_tree.xview)
        
        self.projects_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind events
        self.projects_tree.bind('<<TreeviewSelect>>', self.on_project_select)
        self.projects_tree.bind('<Double-1>', self.on_project_double_click)
        
        # Context menu
        self.create_context_menu()
        
        # Load sample data
        self.load_sample_projects()
    
    def create_project_details(self, parent):
        """
        Create project details panel
        
        Args:
            parent: Parent widget
        """
        # Right panel for project details
        details_frame = ttk.LabelFrame(parent, text=translate("projects_details"), padding=10)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Project info
        info_frame = ttk.Frame(details_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Project name
        ttk.Label(info_frame, text=translate("projects_name") + ":", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.project_name_label = ttk.Label(info_frame, text="-")
        self.project_name_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Project description
        ttk.Label(info_frame, text=translate("projects_description") + ":", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.project_desc_label = ttk.Label(info_frame, text="-", wraplength=300)
        self.project_desc_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Project status
        ttk.Label(info_frame, text=translate("projects_status") + ":", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.project_status_label = ttk.Label(info_frame, text="-")
        self.project_status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Properties count
        ttk.Label(info_frame, text=translate("projects_properties_count") + ":", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.project_props_label = ttk.Label(info_frame, text="-")
        self.project_props_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Action buttons
        action_frame = ttk.Frame(details_frame)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text=translate("projects_edit"),
                  command=self.edit_project).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_frame, text=translate("projects_delete"),
                  command=self.delete_project).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_frame, text=translate("projects_export"),
                  command=self.export_project).pack(side=tk.LEFT)
    
    def create_context_menu(self):
        """
        Create context menu for projects list
        """
        self.context_menu = tk.Menu(self.parent, tearoff=0)
        self.context_menu.add_command(label=translate("projects_edit"), command=self.edit_project)
        self.context_menu.add_command(label=translate("projects_duplicate"), command=self.duplicate_project)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=translate("projects_export"), command=self.export_project)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=translate("projects_delete"), command=self.delete_project)
        
        # Bind right-click
        self.projects_tree.bind('<Button-3>', self.show_context_menu)
    
    def load_sample_projects(self):
        """
        Load sample projects data
        """
        sample_projects = [
            ("Luxury Downtown Condos", "Active", "12", "2024-01-15"),
            ("Suburban Family Homes", "Planning", "8", "2024-02-01"),
            ("Waterfront Villas", "Completed", "5", "2023-12-10"),
            ("Commercial Plaza", "On Hold", "3", "2024-01-20"),
            ("Student Housing Complex", "Active", "15", "2024-02-05")
        ]
        
        for project in sample_projects:
            self.projects_tree.insert('', tk.END, values=project)
    
    def on_search(self, event=None):
        """
        Handle search functionality
        
        Args:
            event: Event object
        """
        search_term = self.search_var.get().lower()
        
        # Clear current items
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        # Reload filtered data (in a real app, this would query the database)
        sample_projects = [
            ("Luxury Downtown Condos", "Active", "12", "2024-01-15"),
            ("Suburban Family Homes", "Planning", "8", "2024-02-01"),
            ("Waterfront Villas", "Completed", "5", "2023-12-10"),
            ("Commercial Plaza", "On Hold", "3", "2024-01-20"),
            ("Student Housing Complex", "Active", "15", "2024-02-05")
        ]
        
        for project in sample_projects:
            if not search_term or search_term in project[0].lower():
                self.projects_tree.insert('', tk.END, values=project)
    
    def on_project_select(self, event=None):
        """
        Handle project selection
        
        Args:
            event: Event object
        """
        selection = self.projects_tree.selection()
        if selection:
            item = self.projects_tree.item(selection[0])
            values = item['values']
            
            # Update details panel
            self.project_name_label.config(text=values[0])
            self.project_desc_label.config(text=f"A {values[0].lower()} project with {values[2]} properties.")
            self.project_status_label.config(text=values[1])
            self.project_props_label.config(text=values[2])
    
    def on_project_double_click(self, event=None):
        """
        Handle project double-click
        
        Args:
            event: Event object
        """
        self.edit_project()
    
    def show_context_menu(self, event):
        """
        Show context menu
        
        Args:
            event: Event object
        """
        # Select item under cursor
        item = self.projects_tree.identify_row(event.y)
        if item:
            self.projects_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def new_project(self):
        """
        Create new project
        """
        messagebox.showinfo(translate("projects_new"), translate("projects_new_coming_soon"))
    
    def import_project(self):
        """
        Import project
        """
        messagebox.showinfo(translate("projects_import"), translate("projects_import_coming_soon"))
    
    def edit_project(self):
        """
        Edit selected project
        """
        selection = self.projects_tree.selection()
        if not selection:
            messagebox.showwarning(translate("projects_warning"), translate("projects_select_first"))
            return
        
        messagebox.showinfo(translate("projects_edit"), translate("projects_edit_coming_soon"))
    
    def duplicate_project(self):
        """
        Duplicate selected project
        """
        selection = self.projects_tree.selection()
        if not selection:
            messagebox.showwarning(translate("projects_warning"), translate("projects_select_first"))
            return
        
        messagebox.showinfo(translate("projects_duplicate"), translate("projects_duplicate_coming_soon"))
    
    def delete_project(self):
        """
        Delete selected project
        """
        selection = self.projects_tree.selection()
        if not selection:
            messagebox.showwarning(translate("projects_warning"), translate("projects_select_first"))
            return
        
        result = messagebox.askyesno(translate("projects_delete_confirm"), 
                                   translate("projects_delete_warning"))
        if result:
            self.projects_tree.delete(selection[0])
            # Clear details panel
            self.project_name_label.config(text="-")
            self.project_desc_label.config(text="-")
            self.project_status_label.config(text="-")
            self.project_props_label.config(text="-")
    
    def export_project(self):
        """
        Export selected project
        """
        selection = self.projects_tree.selection()
        if not selection:
            messagebox.showwarning(translate("projects_warning"), translate("projects_select_first"))
            return
        
        messagebox.showinfo(translate("projects_export"), translate("projects_export_coming_soon"))