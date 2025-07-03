#!/usr/bin/env python3
"""
Preferences Dialog for HomeShow Desktop
Provides user settings and configuration options

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import json
from typing import Dict, Any
from core.localization import translate, get_language, set_language


class PreferencesDialog:
    """
    Preferences dialog for application settings
    """
    
    def __init__(self, parent, on_settings_changed=None):
        """
        Initialize preferences dialog
        
        Args:
            parent: Parent window
            on_settings_changed: Callback when settings change
        """
        self.parent = parent
        self.on_settings_changed = on_settings_changed
        self.settings = self.load_settings()
        self.create_dialog()
    
    def load_settings(self) -> Dict[str, Any]:
        """
        Load application settings
        
        Returns:
            Dictionary of settings
        """
        settings_file = Path(__file__).parent.parent / "data" / "settings.json"
        
        default_settings = {
            "language": "en",
            "theme": "default",
            "auto_backup": True,
            "backup_interval": 24,  # hours
            "max_backups": 10,
            "default_currency": "EUR",
            "image_quality": "high",
            "auto_resize_images": True,
            "max_image_size": 1920,
            "website_template": "modern",
            "export_format": "json",
            "show_tips": True,
            "check_updates": True,
            "data_directory": str(Path(__file__).parent.parent / "data"),
            "backup_directory": str(Path(__file__).parent.parent / "backups")
        }
        
        try:
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded_settings)
            return default_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return default_settings
    
    def save_settings(self):
        """
        Save application settings
        """
        try:
            settings_file = Path(__file__).parent.parent / "data" / "settings.json"
            settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            if self.on_settings_changed:
                self.on_settings_changed(self.settings)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def create_dialog(self):
        """
        Create preferences dialog window
        """
        self.window = tk.Toplevel(self.parent)
        self.window.title(translate("preferences_title"))
        self.window.geometry("600x500")
        self.window.resizable(True, True)
        
        # Center window
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Main container
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create tabs
        self.create_general_tab()
        self.create_media_tab()
        self.create_backup_tab()
        self.create_website_tab()
        
        # Buttons
        self.create_buttons(main_frame)
    
    def create_general_tab(self):
        """
        Create general settings tab
        """
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=translate("preferences_general"))
        
        # Language settings
        lang_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_language"), padding=10)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(lang_frame, text=translate("preferences_select_language")).pack(anchor=tk.W)
        
        self.language_var = tk.StringVar(value=self.settings.get("language", get_language()))
        language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var, 
                                     values=["en", "fr"], 
                                     state="readonly", width=20)
        language_combo.pack(anchor=tk.W, pady=(5, 0))
        
        # Currency settings
        currency_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_currency"), padding=10)
        currency_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(currency_frame, text=translate("preferences_default_currency")).pack(anchor=tk.W)
        
        self.currency_var = tk.StringVar(value=self.settings.get("default_currency", "EUR"))
        currency_combo = ttk.Combobox(currency_frame, textvariable=self.currency_var,
                                     values=["EUR", "USD", "GBP", "CAD", "AUD", "CHF", "JPY"],
                                     state="readonly", width=10)
        currency_combo.pack(anchor=tk.W, pady=(5, 0))
        
        # Other general settings
        other_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_other"), padding=10)
        other_frame.pack(fill=tk.X)
        
        self.show_tips_var = tk.BooleanVar(value=self.settings.get("show_tips", True))
        ttk.Checkbutton(other_frame, text=translate("preferences_show_tips"),
                       variable=self.show_tips_var).pack(anchor=tk.W, pady=2)
        
        self.check_updates_var = tk.BooleanVar(value=self.settings.get("check_updates", True))
        ttk.Checkbutton(other_frame, text=translate("preferences_check_updates"),
                       variable=self.check_updates_var).pack(anchor=tk.W, pady=2)
    
    def create_media_tab(self):
        """
        Create media settings tab
        """
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=translate("preferences_media"))
        
        # Image quality settings
        quality_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_image_quality"), padding=10)
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(quality_frame, text=translate("preferences_quality_level")).pack(anchor=tk.W)
        
        self.image_quality_var = tk.StringVar(value=self.settings.get("image_quality", "high"))
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.image_quality_var,
                                    values=["low", "medium", "high", "original"],
                                    state="readonly", width=15)
        quality_combo.pack(anchor=tk.W, pady=(5, 0))
        
        # Auto resize settings
        resize_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_auto_resize"), padding=10)
        resize_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.auto_resize_var = tk.BooleanVar(value=self.settings.get("auto_resize_images", True))
        ttk.Checkbutton(resize_frame, text=translate("preferences_enable_auto_resize"),
                       variable=self.auto_resize_var).pack(anchor=tk.W, pady=2)
        
        size_frame = ttk.Frame(resize_frame)
        size_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(size_frame, text=translate("preferences_max_size")).pack(side=tk.LEFT)
        
        self.max_size_var = tk.StringVar(value=str(self.settings.get("max_image_size", 1920)))
        size_entry = ttk.Entry(size_frame, textvariable=self.max_size_var, width=10)
        size_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        ttk.Label(size_frame, text="px").pack(side=tk.LEFT)
    
    def create_backup_tab(self):
        """
        Create backup settings tab
        """
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=translate("preferences_backup"))
        
        # Auto backup settings
        auto_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_auto_backup"), padding=10)
        auto_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.auto_backup_var = tk.BooleanVar(value=self.settings.get("auto_backup", True))
        ttk.Checkbutton(auto_frame, text=translate("preferences_enable_auto_backup"),
                       variable=self.auto_backup_var).pack(anchor=tk.W, pady=2)
        
        interval_frame = ttk.Frame(auto_frame)
        interval_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(interval_frame, text=translate("preferences_backup_interval")).pack(side=tk.LEFT)
        
        self.backup_interval_var = tk.StringVar(value=str(self.settings.get("backup_interval", 24)))
        interval_entry = ttk.Entry(interval_frame, textvariable=self.backup_interval_var, width=10)
        interval_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        ttk.Label(interval_frame, text=translate("preferences_hours")).pack(side=tk.LEFT)
        
        # Max backups
        max_frame = ttk.Frame(auto_frame)
        max_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(max_frame, text=translate("preferences_max_backups")).pack(side=tk.LEFT)
        
        self.max_backups_var = tk.StringVar(value=str(self.settings.get("max_backups", 10)))
        max_entry = ttk.Entry(max_frame, textvariable=self.max_backups_var, width=10)
        max_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Backup directory
        dir_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_backup_directory"), padding=10)
        dir_frame.pack(fill=tk.X)
        
        self.backup_dir_var = tk.StringVar(value=self.settings.get("backup_directory", ""))
        
        dir_entry_frame = ttk.Frame(dir_frame)
        dir_entry_frame.pack(fill=tk.X)
        
        dir_entry = ttk.Entry(dir_entry_frame, textvariable=self.backup_dir_var)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(dir_entry_frame, text=translate("preferences_browse"),
                  command=self.browse_backup_directory).pack(side=tk.RIGHT)
    
    def create_website_tab(self):
        """
        Create website settings tab
        """
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=translate("preferences_website"))
        
        # Default template
        template_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_default_template"), padding=10)
        template_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(template_frame, text=translate("preferences_select_template")).pack(anchor=tk.W)
        
        self.template_var = tk.StringVar(value=self.settings.get("website_template", "modern"))
        template_combo = ttk.Combobox(template_frame, textvariable=self.template_var,
                                     values=["modern", "classic", "minimal", "luxury"],
                                     state="readonly", width=20)
        template_combo.pack(anchor=tk.W, pady=(5, 0))
        
        # Export format
        export_frame = ttk.LabelFrame(tab_frame, text=translate("preferences_export_format"), padding=10)
        export_frame.pack(fill=tk.X)
        
        ttk.Label(export_frame, text=translate("preferences_default_export")).pack(anchor=tk.W)
        
        self.export_format_var = tk.StringVar(value=self.settings.get("export_format", "json"))
        export_combo = ttk.Combobox(export_frame, textvariable=self.export_format_var,
                                   values=["json", "xml", "csv"],
                                   state="readonly", width=15)
        export_combo.pack(anchor=tk.W, pady=(5, 0))
    
    def create_buttons(self, parent):
        """
        Create dialog buttons
        
        Args:
            parent: Parent widget
        """
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        # Cancel button
        ttk.Button(button_frame, text=translate("preferences_cancel"),
                  command=self.cancel).pack(side=tk.LEFT)
        
        # Reset button
        ttk.Button(button_frame, text=translate("preferences_reset"),
                  command=self.reset_to_defaults).pack(side=tk.LEFT, padx=(10, 0))
        
        # Apply and OK buttons
        ttk.Button(button_frame, text=translate("preferences_apply"),
                  command=self.apply_settings).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(button_frame, text=translate("preferences_ok"),
                  command=self.ok, style='Primary.TButton').pack(side=tk.RIGHT)
    
    def browse_backup_directory(self):
        """
        Browse for backup directory
        """
        directory = filedialog.askdirectory(
            title=translate("preferences_select_backup_dir"),
            initialdir=self.backup_dir_var.get() or str(Path.home())
        )
        
        if directory:
            self.backup_dir_var.set(directory)
    
    def apply_settings(self):
        """
        Apply current settings
        """
        try:
            # Update settings dictionary
            self.settings.update({
                "language": self.language_var.get(),
                "default_currency": self.currency_var.get(),
                "show_tips": self.show_tips_var.get(),
                "check_updates": self.check_updates_var.get(),
                "image_quality": self.image_quality_var.get(),
                "auto_resize_images": self.auto_resize_var.get(),
                "max_image_size": int(self.max_size_var.get()),
                "auto_backup": self.auto_backup_var.get(),
                "backup_interval": int(self.backup_interval_var.get()),
                "max_backups": int(self.max_backups_var.get()),
                "backup_directory": self.backup_dir_var.get(),
                "website_template": self.template_var.get(),
                "export_format": self.export_format_var.get()
            })
            
            # Save settings
            self.save_settings()
            
            # Apply language change if needed
            if self.language_var.get() != get_current_language():
                set_language(self.language_var.get())
                messagebox.showinfo(
                    translate("preferences_language_changed"),
                    translate("preferences_restart_required")
                )
            
            messagebox.showinfo(
                translate("preferences_applied"),
                translate("preferences_settings_saved")
            )
            
        except ValueError as e:
            messagebox.showerror(
                translate("preferences_error"),
                translate("preferences_invalid_values")
            )
        except Exception as e:
            messagebox.showerror(
                translate("preferences_error"),
                f"Failed to apply settings: {e}"
            )
    
    def reset_to_defaults(self):
        """
        Reset all settings to defaults
        """
        result = messagebox.askyesno(
            translate("preferences_reset_confirm"),
            translate("preferences_reset_warning")
        )
        
        if result:
            # Reset to default values
            self.language_var.set("en")
            self.currency_var.set("EUR")
            self.show_tips_var.set(True)
            self.check_updates_var.set(True)
            self.image_quality_var.set("high")
            self.auto_resize_var.set(True)
            self.max_size_var.set("1920")
            self.auto_backup_var.set(True)
            self.backup_interval_var.set("24")
            self.max_backups_var.set("10")
            self.backup_dir_var.set(str(Path(__file__).parent.parent / "backups"))
            self.template_var.set("modern")
            self.export_format_var.set("json")
    
    def ok(self):
        """
        Apply settings and close dialog
        """
        self.apply_settings()
        self.window.destroy()
    
    def cancel(self):
        """
        Close dialog without saving
        """
        self.window.destroy()