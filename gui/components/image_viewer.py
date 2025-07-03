#!/usr/bin/env python3
"""
Image Viewer Component for HomeShow Desktop
Custom widget for displaying and managing property images

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import List, Optional, Callable
from PIL import Image, ImageTk
import threading

class ImageViewer:
    """
    Custom image viewer widget with navigation and zoom capabilities
    """
    
    def __init__(self, parent, images: List[str] = None, on_image_change: Optional[Callable] = None):
        """
        Initialize image viewer
        
        Args:
            parent: Parent widget
            images: List of image file paths
            on_image_change: Callback when image changes
        """
        self.parent = parent
        self.images = images or []
        self.on_image_change = on_image_change
        
        self.current_index = 0
        self.zoom_level = 1.0
        self.original_image = None
        self.display_image = None
        
        self.create_viewer()
        
        if self.images:
            self.load_image(0)
    
    def create_viewer(self):
        """
        Create image viewer interface
        """
        # Main container
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.create_toolbar()
        
        # Image display area
        self.create_image_area()
        
        # Navigation
        self.create_navigation()
        
        # Thumbnail strip
        self.create_thumbnail_strip()
    
    def create_toolbar(self):
        """
        Create toolbar with zoom and action buttons
        """
        toolbar_frame = ttk.Frame(self.main_frame)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Zoom controls
        zoom_frame = ttk.Frame(toolbar_frame)
        zoom_frame.pack(side=tk.LEFT)
        
        ttk.Button(
            zoom_frame,
            text="🔍-",
            command=self.zoom_out,
            width=4
        ).pack(side=tk.LEFT, padx=2)
        
        self.zoom_label = ttk.Label(
            zoom_frame,
            text="100%",
            width=6,
            anchor=tk.CENTER
        )
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            zoom_frame,
            text="🔍+",
            command=self.zoom_in,
            width=4
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            zoom_frame,
            text="🔄",
            command=self.reset_zoom,
            width=4
        ).pack(side=tk.LEFT, padx=5)
        
        # Image info
        self.info_label = ttk.Label(
            toolbar_frame,
            text="No image",
            font=('Segoe UI', 9)
        )
        self.info_label.pack(side=tk.RIGHT)
    
    def create_image_area(self):
        """
        Create scrollable image display area
        """
        # Image frame with scrollbars
        image_frame = ttk.Frame(self.main_frame)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas with scrollbars
        self.canvas = tk.Canvas(
            image_frame,
            bg='white',
            highlightthickness=0
        )
        
        self.h_scrollbar = ttk.Scrollbar(
            image_frame,
            orient=tk.HORIZONTAL,
            command=self.canvas.xview
        )
        self.v_scrollbar = ttk.Scrollbar(
            image_frame,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        
        self.canvas.configure(
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set
        )
        
        # Pack scrollbars and canvas
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        
        # Image item on canvas
        self.image_item = None
    
    def create_navigation(self):
        """
        Create navigation controls
        """
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Previous button
        self.prev_btn = ttk.Button(
            nav_frame,
            text="← Previous",
            command=self.previous_image,
            state=tk.DISABLED
        )
        self.prev_btn.pack(side=tk.LEFT)
        
        # Image counter
        self.counter_label = ttk.Label(
            nav_frame,
            text="0 / 0",
            font=('Segoe UI', 10)
        )
        self.counter_label.pack(side=tk.LEFT, expand=True)
        
        # Next button
        self.next_btn = ttk.Button(
            nav_frame,
            text="Next →",
            command=self.next_image,
            state=tk.DISABLED
        )
        self.next_btn.pack(side=tk.RIGHT)
    
    def create_thumbnail_strip(self):
        """
        Create thumbnail strip at bottom
        """
        thumb_frame = ttk.Frame(self.main_frame)
        thumb_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Scrollable thumbnail container
        thumb_canvas = tk.Canvas(
            thumb_frame,
            height=80,
            bg='lightgray',
            highlightthickness=0
        )
        thumb_scrollbar = ttk.Scrollbar(
            thumb_frame,
            orient=tk.HORIZONTAL,
            command=thumb_canvas.xview
        )
        
        self.thumb_container = ttk.Frame(thumb_canvas)
        
        self.thumb_container.bind(
            "<Configure>",
            lambda e: thumb_canvas.configure(scrollregion=thumb_canvas.bbox("all"))
        )
        
        thumb_canvas.create_window((0, 0), window=self.thumb_container, anchor="nw")
        thumb_canvas.configure(xscrollcommand=thumb_scrollbar.set)
        
        thumb_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        thumb_canvas.pack(side=tk.TOP, fill=tk.X)
        
        self.thumb_canvas = thumb_canvas
        self.thumbnails = []
    
    def set_images(self, images: List[str]):
        """
        Set list of images to display
        
        Args:
            images: List of image file paths
        """
        self.images = images
        self.current_index = 0
        self.create_thumbnails()
        
        if self.images:
            self.load_image(0)
        else:
            self.clear_display()
        
        self.update_navigation()
    
    def create_thumbnails(self):
        """
        Create thumbnail images
        """
        # Clear existing thumbnails
        for widget in self.thumb_container.winfo_children():
            widget.destroy()
        
        self.thumbnails.clear()
        
        # Create thumbnails in separate thread
        if self.images:
            threading.Thread(
                target=self._create_thumbnails_thread,
                daemon=True
            ).start()
    
    def _create_thumbnails_thread(self):
        """
        Create thumbnails in background thread
        """
        for i, image_path in enumerate(self.images):
            try:
                # Load and resize image
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Calculate thumbnail size
                    img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update UI in main thread
                    self.parent.after(
                        0,
                        lambda p=photo, idx=i: self._add_thumbnail(p, idx)
                    )
                    
            except Exception as e:
                print(f"Error creating thumbnail for {image_path}: {e}")
    
    def _add_thumbnail(self, photo, index):
        """
        Add thumbnail to UI (called from main thread)
        
        Args:
            photo: PhotoImage object
            index: Image index
        """
        # Thumbnail button
        thumb_btn = tk.Button(
            self.thumb_container,
            image=photo,
            command=lambda idx=index: self.load_image(idx),
            relief=tk.RAISED,
            bd=2
        )
        thumb_btn.image = photo  # Keep reference
        thumb_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.thumbnails.append(thumb_btn)
        
        # Update scroll region
        self.thumb_container.update_idletasks()
        self.thumb_canvas.configure(scrollregion=self.thumb_canvas.bbox("all"))
    
    def load_image(self, index: int):
        """
        Load image at specified index
        
        Args:
            index: Image index
        """
        if 0 <= index < len(self.images):
            self.current_index = index
            
            # Load image in background thread
            threading.Thread(
                target=self._load_image_thread,
                args=(self.images[index],),
                daemon=True
            ).start()
            
            self.update_navigation()
            self.update_thumbnail_selection()
            
            # Call change callback
            if self.on_image_change:
                self.on_image_change(index, self.images[index])
    
    def _load_image_thread(self, image_path: str):
        """
        Load image in background thread
        
        Args:
            image_path: Path to image file
        """
        try:
            # Load original image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                self.original_image = img.copy()
            
            # Update UI in main thread
            self.parent.after(0, self._display_image)
            
        except Exception as e:
            self.parent.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    f"Failed to load image: {e}"
                )
            )
    
    def _display_image(self):
        """
        Display loaded image on canvas
        """
        if not self.original_image:
            return
        
        try:
            # Apply zoom
            width = int(self.original_image.width * self.zoom_level)
            height = int(self.original_image.height * self.zoom_level)
            
            resized_image = self.original_image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )
            
            # Convert to PhotoImage
            self.display_image = ImageTk.PhotoImage(resized_image)
            
            # Clear canvas and add image
            self.canvas.delete("all")
            self.image_item = self.canvas.create_image(
                0, 0,
                anchor=tk.NW,
                image=self.display_image
            )
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Update info
            self.update_image_info()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image: {e}")
    
    def update_image_info(self):
        """
        Update image information display
        """
        if self.original_image and self.current_index < len(self.images):
            filename = Path(self.images[self.current_index]).name
            size = f"{self.original_image.width}×{self.original_image.height}"
            zoom = f"{int(self.zoom_level * 100)}%"
            
            self.info_label.config(text=f"{filename} | {size} | {zoom}")
            self.zoom_label.config(text=zoom)
        else:
            self.info_label.config(text="No image")
            self.zoom_label.config(text="100%")
    
    def update_navigation(self):
        """
        Update navigation button states
        """
        total = len(self.images)
        current = self.current_index + 1 if self.images else 0
        
        self.counter_label.config(text=f"{current} / {total}")
        
        self.prev_btn.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_index < total - 1 else tk.DISABLED)
    
    def update_thumbnail_selection(self):
        """
        Update thumbnail selection highlight
        """
        for i, thumb in enumerate(self.thumbnails):
            if i == self.current_index:
                thumb.config(relief=tk.SUNKEN, bd=3)
            else:
                thumb.config(relief=tk.RAISED, bd=2)
    
    def previous_image(self):
        """
        Show previous image
        """
        if self.current_index > 0:
            self.load_image(self.current_index - 1)
    
    def next_image(self):
        """
        Show next image
        """
        if self.current_index < len(self.images) - 1:
            self.load_image(self.current_index + 1)
    
    def zoom_in(self):
        """
        Zoom in on image
        """
        self.zoom_level = min(self.zoom_level * 1.25, 5.0)
        self._display_image()
    
    def zoom_out(self):
        """
        Zoom out on image
        """
        self.zoom_level = max(self.zoom_level / 1.25, 0.1)
        self._display_image()
    
    def reset_zoom(self):
        """
        Reset zoom to 100%
        """
        self.zoom_level = 1.0
        self._display_image()
    
    def clear_display(self):
        """
        Clear image display
        """
        self.canvas.delete("all")
        self.original_image = None
        self.display_image = None
        self.update_image_info()
    
    # Mouse event handlers
    def on_canvas_click(self, event):
        """
        Handle canvas click for panning
        
        Args:
            event: Mouse event
        """
        self.canvas.scan_mark(event.x, event.y)
    
    def on_canvas_drag(self, event):
        """
        Handle canvas drag for panning
        
        Args:
            event: Mouse event
        """
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    
    def on_mouse_wheel(self, event):
        """
        Handle mouse wheel for zooming
        
        Args:
            event: Mouse wheel event
        """
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def get_current_image(self) -> Optional[str]:
        """
        Get current image path
        
        Returns:
            str: Current image path or None
        """
        if 0 <= self.current_index < len(self.images):
            return self.images[self.current_index]
        return None
    
    def get_widget(self) -> ttk.Frame:
        """
        Get main widget frame
        
        Returns:
            ttk.Frame: Main frame widget
        """
        return self.main_frame