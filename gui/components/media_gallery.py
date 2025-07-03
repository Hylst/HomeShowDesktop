#!/usr/bin/env python3
"""
Media Gallery Component for HomeShow Desktop
Custom widget for managing and displaying property media files

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from PIL import Image, ImageTk
import threading
import shutil

class MediaGallery:
    """
    Media gallery widget for managing property images and videos
    """
    
    def __init__(self, parent, media_files: List[Dict[str, Any]] = None,
                 on_media_change: Optional[Callable] = None,
                 on_media_select: Optional[Callable] = None,
                 editable: bool = True):
        """
        Initialize media gallery
        
        Args:
            parent: Parent widget
            media_files: List of media file dictionaries
            on_media_change: Callback when media list changes
            on_media_select: Callback when media item is selected
            editable: Whether gallery is editable
        """
        self.parent = parent
        self.media_files = media_files or []
        self.on_media_change = on_media_change
        self.on_media_select = on_media_select
        self.editable = editable
        
        self.selected_index = -1
        self.thumbnails = {}
        
        self.create_gallery()
        self.load_media()
    
    def create_gallery(self):
        """
        Create media gallery interface
        """
        # Main container
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        if self.editable:
            self.create_toolbar()
        
        # Media grid
        self.create_media_grid()
        
        # Status bar
        self.create_status_bar()
    
    def create_toolbar(self):
        """
        Create toolbar with media management buttons
        """
        toolbar_frame = ttk.Frame(self.main_frame)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add buttons
        add_frame = ttk.Frame(toolbar_frame)
        add_frame.pack(side=tk.LEFT)
        
        add_images_btn = ttk.Button(
            add_frame,
            text="📷 Add Images",
            command=self.add_images,
            style='Primary.TButton'
        )
        add_images_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        add_videos_btn = ttk.Button(
            add_frame,
            text="🎥 Add Videos",
            command=self.add_videos
        )
        add_videos_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Management buttons
        mgmt_frame = ttk.Frame(toolbar_frame)
        mgmt_frame.pack(side=tk.LEFT)
        
        self.remove_btn = ttk.Button(
            mgmt_frame,
            text="🗑️ Remove",
            command=self.remove_selected,
            state=tk.DISABLED
        )
        self.remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(
            mgmt_frame,
            text="🧹 Clear All",
            command=self.clear_all
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # View options
        view_frame = ttk.Frame(toolbar_frame)
        view_frame.pack(side=tk.RIGHT)
        
        ttk.Label(view_frame, text="View:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.view_var = tk.StringVar(value="grid")
        view_combo = ttk.Combobox(
            view_frame,
            textvariable=self.view_var,
            values=["grid", "list"],
            state="readonly",
            width=8
        )
        view_combo.pack(side=tk.LEFT)
        view_combo.bind("<<ComboboxSelected>>", self.on_view_change)
    
    def create_media_grid(self):
        """
        Create scrollable media grid
        """
        # Container with scrollbar
        grid_container = ttk.Frame(self.main_frame)
        grid_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas with scrollbar
        self.canvas = tk.Canvas(
            grid_container,
            bg='white',
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            grid_container,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        
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
        
        # Bind mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Media items container
        self.media_container = ttk.Frame(self.scrollable_frame)
        self.media_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_status_bar(self):
        """
        Create status bar
        """
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(
            status_frame,
            text="0 media files",
            font=('Segoe UI', 9),
            foreground='gray'
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Selection info
        self.selection_label = ttk.Label(
            status_frame,
            text="",
            font=('Segoe UI', 9),
            foreground='blue'
        )
        self.selection_label.pack(side=tk.RIGHT)
    
    def _on_mousewheel(self, event):
        """
        Handle mouse wheel scrolling
        
        Args:
            event: Mouse wheel event
        """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_media(self):
        """
        Load and display media files
        """
        # Clear existing items
        self.clear_display()
        
        if not self.media_files:
            self.show_empty_state()
            return
        
        # Create media items based on view mode
        view_mode = self.view_var.get() if hasattr(self, 'view_var') else 'grid'
        
        if view_mode == 'grid':
            self.create_grid_view()
        else:
            self.create_list_view()
        
        # Update status
        self.update_status()
        
        # Load thumbnails in background
        self.load_thumbnails()
    
    def create_grid_view(self):
        """
        Create grid view of media items
        """
        # Calculate grid dimensions
        items_per_row = 4
        
        for i, media in enumerate(self.media_files):
            row = i // items_per_row
            col = i % items_per_row
            
            self.create_media_item_grid(media, i, row, col)
    
    def create_list_view(self):
        """
        Create list view of media items
        """
        for i, media in enumerate(self.media_files):
            self.create_media_item_list(media, i)
    
    def create_media_item_grid(self, media: Dict[str, Any], index: int, row: int, col: int):
        """
        Create media item in grid view
        
        Args:
            media: Media file data
            index: Media index
            row: Grid row
            col: Grid column
        """
        # Item frame
        item_frame = ttk.Frame(
            self.media_container,
            style='MediaItem.TFrame',
            relief=tk.RAISED,
            borderwidth=1
        )
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # Configure grid weights
        self.media_container.grid_columnconfigure(col, weight=1)
        
        # Bind click events
        item_frame.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
        
        # Thumbnail
        thumb_frame = ttk.Frame(item_frame)
        thumb_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Placeholder thumbnail
        icon = "📷" if media.get('type') == 'image' else "🎥"
        thumb_label = ttk.Label(
            thumb_frame,
            text=icon,
            font=('Segoe UI', 24),
            width=8,
            height=4,
            anchor=tk.CENTER,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        thumb_label.pack(fill=tk.BOTH, expand=True)
        thumb_label.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
        
        # Store reference for thumbnail loading
        media['thumb_label'] = thumb_label
        media['item_frame'] = item_frame
        
        # File name
        name_label = ttk.Label(
            item_frame,
            text=Path(media.get('path', '')).name,
            font=('Segoe UI', 8),
            anchor=tk.CENTER,
            wraplength=120
        )
        name_label.pack(fill=tk.X, padx=5, pady=(0, 5))
        name_label.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
        
        # File size
        if media.get('size'):
            size_text = self.format_file_size(media['size'])
            size_label = ttk.Label(
                item_frame,
                text=size_text,
                font=('Segoe UI', 7),
                foreground='gray',
                anchor=tk.CENTER
            )
            size_label.pack(fill=tk.X, padx=5, pady=(0, 5))
            size_label.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
    
    def create_media_item_list(self, media: Dict[str, Any], index: int):
        """
        Create media item in list view
        
        Args:
            media: Media file data
            index: Media index
        """
        # Item frame
        item_frame = ttk.Frame(
            self.media_container,
            style='MediaItem.TFrame',
            relief=tk.RAISED,
            borderwidth=1
        )
        item_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Bind click events
        item_frame.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
        
        # Content frame
        content_frame = ttk.Frame(item_frame)
        content_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Left side - thumbnail
        thumb_frame = ttk.Frame(content_frame)
        thumb_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        icon = "📷" if media.get('type') == 'image' else "🎥"
        thumb_label = ttk.Label(
            thumb_frame,
            text=icon,
            font=('Segoe UI', 16),
            width=4,
            height=2,
            anchor=tk.CENTER,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        thumb_label.pack()
        thumb_label.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
        
        # Store reference
        media['thumb_label'] = thumb_label
        media['item_frame'] = item_frame
        
        # Right side - info
        info_frame = ttk.Frame(content_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # File name
        name_label = ttk.Label(
            info_frame,
            text=Path(media.get('path', '')).name,
            font=('Segoe UI', 10, 'bold')
        )
        name_label.pack(anchor=tk.W)
        name_label.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
        
        # File details
        details = []
        if media.get('type'):
            details.append(media['type'].title())
        if media.get('size'):
            details.append(self.format_file_size(media['size']))
        if media.get('dimensions'):
            details.append(f"{media['dimensions'][0]}×{media['dimensions'][1]}")
        
        if details:
            details_text = " • ".join(details)
            details_label = ttk.Label(
                info_frame,
                text=details_text,
                font=('Segoe UI', 9),
                foreground='gray'
            )
            details_label.pack(anchor=tk.W)
            details_label.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
        
        # File path
        path_label = ttk.Label(
            info_frame,
            text=str(media.get('path', '')),
            font=('Segoe UI', 8),
            foreground='gray'
        )
        path_label.pack(anchor=tk.W)
        path_label.bind("<Button-1>", lambda e, idx=index: self.select_media(idx))
    
    def load_thumbnails(self):
        """
        Load thumbnails for media items in background
        """
        for i, media in enumerate(self.media_files):
            if media.get('type') == 'image' and media.get('path'):
                threading.Thread(
                    target=self._load_thumbnail_thread,
                    args=(media, i),
                    daemon=True
                ).start()
    
    def _load_thumbnail_thread(self, media: Dict[str, Any], index: int):
        """
        Load thumbnail in background thread
        
        Args:
            media: Media file data
            index: Media index
        """
        try:
            image_path = media['path']
            if not Path(image_path).exists():
                return
            
            # Load and resize image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Determine thumbnail size based on view mode
                view_mode = self.view_var.get() if hasattr(self, 'view_var') else 'grid'
                if view_mode == 'grid':
                    size = (80, 80)
                else:
                    size = (40, 40)
                
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Update UI in main thread
                self.parent.after(
                    0,
                    lambda: self._set_thumbnail(media, photo)
                )
                
        except Exception as e:
            print(f"Error loading thumbnail for {media.get('path')}: {e}")
    
    def _set_thumbnail(self, media: Dict[str, Any], photo):
        """
        Set thumbnail image (called from main thread)
        
        Args:
            media: Media file data
            photo: PhotoImage object
        """
        if 'thumb_label' in media and media['thumb_label'].winfo_exists():
            media['thumb_label'].config(
                image=photo,
                text=""
            )
            # Store reference to prevent garbage collection
            media['thumbnail'] = photo
    
    def show_empty_state(self):
        """
        Show empty state when no media files
        """
        empty_frame = ttk.Frame(self.media_container)
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        # Empty icon
        icon_label = ttk.Label(
            empty_frame,
            text="📁",
            font=('Segoe UI', 48),
            foreground='#bdc3c7'
        )
        icon_label.pack()
        
        # Empty message
        message_label = ttk.Label(
            empty_frame,
            text="No media files",
            font=('Segoe UI', 16),
            foreground='#7f8c8d'
        )
        message_label.pack(pady=(10, 5))
        
        # Subtitle
        if self.editable:
            subtitle_label = ttk.Label(
                empty_frame,
                text="Click 'Add Images' or 'Add Videos' to get started",
                font=('Segoe UI', 12),
                foreground='#95a5a6'
            )
            subtitle_label.pack()
    
    def clear_display(self):
        """
        Clear media display
        """
        for widget in self.media_container.winfo_children():
            widget.destroy()
        
        # Clear thumbnail references
        for media in self.media_files:
            media.pop('thumb_label', None)
            media.pop('item_frame', None)
            media.pop('thumbnail', None)
    
    def add_images(self):
        """
        Add image files
        """
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        
        for file_path in files:
            if not any(media.get('path') == file_path for media in self.media_files):
                media_info = self.get_media_info(file_path, 'image')
                self.media_files.append(media_info)
        
        self.load_media()
        self.notify_change()
    
    def add_videos(self):
        """
        Add video files
        """
        files = filedialog.askopenfilenames(
            title="Select Videos",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.wmv *.flv *.webm *.mkv"),
                ("All files", "*.*")
            ]
        )
        
        for file_path in files:
            if not any(media.get('path') == file_path for media in self.media_files):
                media_info = self.get_media_info(file_path, 'video')
                self.media_files.append(media_info)
        
        self.load_media()
        self.notify_change()
    
    def get_media_info(self, file_path: str, media_type: str) -> Dict[str, Any]:
        """
        Get media file information
        
        Args:
            file_path: Path to media file
            media_type: Type of media (image/video)
        
        Returns:
            Dict containing media information
        """
        path_obj = Path(file_path)
        
        media_info = {
            'path': file_path,
            'name': path_obj.name,
            'type': media_type,
            'size': path_obj.stat().st_size if path_obj.exists() else 0
        }
        
        # Get image dimensions for images
        if media_type == 'image':
            try:
                with Image.open(file_path) as img:
                    media_info['dimensions'] = img.size
            except Exception:
                pass
        
        return media_info
    
    def remove_selected(self):
        """
        Remove selected media file
        """
        if self.selected_index >= 0 and self.selected_index < len(self.media_files):
            media = self.media_files[self.selected_index]
            
            if messagebox.askyesno(
                "Remove Media",
                f"Remove '{media.get('name', 'Unknown')}' from gallery?"
            ):
                del self.media_files[self.selected_index]
                self.selected_index = -1
                self.load_media()
                self.notify_change()
    
    def clear_all(self):
        """
        Clear all media files
        """
        if self.media_files and messagebox.askyesno(
            "Clear All Media",
            "Remove all media files from gallery?"
        ):
            self.media_files.clear()
            self.selected_index = -1
            self.load_media()
            self.notify_change()
    
    def select_media(self, index: int):
        """
        Select media item
        
        Args:
            index: Media index to select
        """
        # Deselect previous
        if self.selected_index >= 0 and self.selected_index < len(self.media_files):
            prev_media = self.media_files[self.selected_index]
            if 'item_frame' in prev_media and prev_media['item_frame'].winfo_exists():
                prev_media['item_frame'].config(style='MediaItem.TFrame')
        
        # Select new
        self.selected_index = index
        if 0 <= index < len(self.media_files):
            media = self.media_files[index]
            if 'item_frame' in media and media['item_frame'].winfo_exists():
                media['item_frame'].config(style='Selected.TFrame')
            
            # Update buttons
            if hasattr(self, 'remove_btn'):
                self.remove_btn.config(state=tk.NORMAL)
            
            # Update selection info
            self.update_selection_info(media)
            
            # Call selection callback
            if self.on_media_select:
                self.on_media_select(index, media)
        else:
            if hasattr(self, 'remove_btn'):
                self.remove_btn.config(state=tk.DISABLED)
            self.selection_label.config(text="")
    
    def update_status(self):
        """
        Update status bar
        """
        total = len(self.media_files)
        images = len([m for m in self.media_files if m.get('type') == 'image'])
        videos = len([m for m in self.media_files if m.get('type') == 'video'])
        
        status_text = f"{total} media files"
        if images > 0 or videos > 0:
            status_text += f" ({images} images, {videos} videos)"
        
        self.status_label.config(text=status_text)
    
    def update_selection_info(self, media: Dict[str, Any]):
        """
        Update selection information
        
        Args:
            media: Selected media data
        """
        info_parts = [media.get('name', 'Unknown')]
        
        if media.get('size'):
            info_parts.append(self.format_file_size(media['size']))
        
        if media.get('dimensions'):
            info_parts.append(f"{media['dimensions'][0]}×{media['dimensions'][1]}")
        
        self.selection_label.config(text=" • ".join(info_parts))
    
    def format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human readable format
        
        Args:
            size_bytes: Size in bytes
        
        Returns:
            str: Formatted size string
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def on_view_change(self, event=None):
        """
        Handle view mode change
        
        Args:
            event: Combobox selection event
        """
        self.load_media()
    
    def notify_change(self):
        """
        Notify about media list changes
        """
        if self.on_media_change:
            self.on_media_change(self.media_files)
    
    def set_media_files(self, media_files: List[Dict[str, Any]]):
        """
        Set media files list
        
        Args:
            media_files: List of media file dictionaries
        """
        self.media_files = media_files or []
        self.selected_index = -1
        self.load_media()
    
    def get_media_files(self) -> List[Dict[str, Any]]:
        """
        Get current media files list
        
        Returns:
            List of media file dictionaries
        """
        return self.media_files.copy()
    
    def get_selected_media(self) -> Optional[Dict[str, Any]]:
        """
        Get currently selected media
        
        Returns:
            Selected media data or None
        """
        if 0 <= self.selected_index < len(self.media_files):
            return self.media_files[self.selected_index]
        return None
    
    def get_widget(self) -> ttk.Frame:
        """
        Get main widget frame
        
        Returns:
            ttk.Frame: Main frame widget
        """
        return self.main_frame