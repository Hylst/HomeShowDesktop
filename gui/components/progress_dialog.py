#!/usr/bin/env python3
"""
Progress Dialog Component for HomeShow Desktop
Custom dialog for showing progress of long-running operations

Author: AI Assistant
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Optional, Callable, Any

class ProgressDialog:
    """
    Progress dialog for long-running operations
    """
    
    def __init__(self, parent, title: str = "Progress", 
                 message: str = "Processing...",
                 cancelable: bool = True,
                 modal: bool = True):
        """
        Initialize progress dialog
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Initial message
            cancelable: Whether operation can be canceled
            modal: Whether dialog is modal
        """
        self.parent = parent
        self.title = title
        self.message = message
        self.cancelable = cancelable
        self.modal = modal
        
        self.dialog = None
        self.progress_var = None
        self.message_var = None
        self.cancel_callback = None
        self.is_canceled = False
        self.is_completed = False
        
        self.create_dialog()
    
    def create_dialog(self):
        """
        Create progress dialog window
        """
        # Create dialog window
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.center_dialog()
        
        # Make modal if requested
        if self.modal:
            self.dialog.transient(self.parent)
            self.dialog.grab_set()
        
        # Prevent closing with X button if not cancelable
        if not self.cancelable:
            self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        else:
            self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Create dialog content
        self.create_content()
        
        # Focus dialog
        self.dialog.focus_set()
    
    def center_dialog(self):
        """
        Center dialog on parent window
        """
        self.dialog.update_idletasks()
        
        # Get parent position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def create_content(self):
        """
        Create dialog content
        """
        # Main frame
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Message label
        self.message_var = tk.StringVar(value=self.message)
        message_label = ttk.Label(
            main_frame,
            textvariable=self.message_var,
            font=('Segoe UI', 10),
            wraplength=350
        )
        message_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=350,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Progress text
        self.progress_text_var = tk.StringVar(value="0%")
        progress_text_label = ttk.Label(
            main_frame,
            textvariable=self.progress_text_var,
            font=('Segoe UI', 9),
            foreground='gray'
        )
        progress_text_label.pack()
        
        # Buttons frame
        if self.cancelable:
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=(15, 0))
            
            self.cancel_button = ttk.Button(
                button_frame,
                text="Cancel",
                command=self.on_cancel
            )
            self.cancel_button.pack(side=tk.RIGHT)
    
    def set_progress(self, value: float, message: str = None):
        """
        Update progress value and message
        
        Args:
            value: Progress value (0-100)
            message: Optional message update
        """
        if self.dialog and self.dialog.winfo_exists():
            self.progress_var.set(value)
            self.progress_text_var.set(f"{value:.1f}%")
            
            if message:
                self.message_var.set(message)
            
            # Update dialog
            self.dialog.update_idletasks()
    
    def set_message(self, message: str):
        """
        Update progress message
        
        Args:
            message: New message
        """
        if self.dialog and self.dialog.winfo_exists():
            self.message_var.set(message)
            self.dialog.update_idletasks()
    
    def set_indeterminate(self, active: bool = True):
        """
        Set progress bar to indeterminate mode
        
        Args:
            active: Whether to activate indeterminate mode
        """
        if self.dialog and self.dialog.winfo_exists():
            if active:
                self.progress_bar.config(mode='indeterminate')
                self.progress_bar.start(10)
                self.progress_text_var.set("Processing...")
            else:
                self.progress_bar.stop()
                self.progress_bar.config(mode='determinate')
    
    def set_cancel_callback(self, callback: Callable):
        """
        Set callback for cancel operation
        
        Args:
            callback: Function to call when canceled
        """
        self.cancel_callback = callback
    
    def on_cancel(self):
        """
        Handle cancel button click
        """
        if not self.is_canceled and not self.is_completed:
            self.is_canceled = True
            
            # Disable cancel button
            if hasattr(self, 'cancel_button'):
                self.cancel_button.config(state=tk.DISABLED, text="Canceling...")
            
            # Update message
            self.set_message("Canceling operation...")
            
            # Call cancel callback
            if self.cancel_callback:
                threading.Thread(
                    target=self.cancel_callback,
                    daemon=True
                ).start()
    
    def complete(self, message: str = "Completed"):
        """
        Mark operation as completed
        
        Args:
            message: Completion message
        """
        if self.dialog and self.dialog.winfo_exists():
            self.is_completed = True
            self.set_progress(100, message)
            
            # Close dialog after short delay
            self.dialog.after(1000, self.close)
    
    def close(self):
        """
        Close progress dialog
        """
        if self.dialog and self.dialog.winfo_exists():
            if self.modal:
                self.dialog.grab_release()
            self.dialog.destroy()
            self.dialog = None
    
    def is_open(self) -> bool:
        """
        Check if dialog is open
        
        Returns:
            bool: True if dialog is open
        """
        return self.dialog is not None and self.dialog.winfo_exists()
    
    def was_canceled(self) -> bool:
        """
        Check if operation was canceled
        
        Returns:
            bool: True if canceled
        """
        return self.is_canceled

class ProgressManager:
    """
    Manager for handling multiple progress operations
    """
    
    def __init__(self, parent):
        """
        Initialize progress manager
        
        Args:
            parent: Parent window
        """
        self.parent = parent
        self.active_dialogs = {}
    
    def create_progress(self, operation_id: str, title: str = "Progress",
                       message: str = "Processing...",
                       cancelable: bool = True) -> ProgressDialog:
        """
        Create new progress dialog
        
        Args:
            operation_id: Unique operation identifier
            title: Dialog title
            message: Initial message
            cancelable: Whether operation can be canceled
        
        Returns:
            ProgressDialog: Created progress dialog
        """
        # Close existing dialog for this operation
        if operation_id in self.active_dialogs:
            self.close_progress(operation_id)
        
        # Create new dialog
        dialog = ProgressDialog(
            self.parent,
            title=title,
            message=message,
            cancelable=cancelable
        )
        
        self.active_dialogs[operation_id] = dialog
        return dialog
    
    def update_progress(self, operation_id: str, value: float, message: str = None):
        """
        Update progress for operation
        
        Args:
            operation_id: Operation identifier
            value: Progress value (0-100)
            message: Optional message update
        """
        if operation_id in self.active_dialogs:
            dialog = self.active_dialogs[operation_id]
            if dialog.is_open():
                dialog.set_progress(value, message)
    
    def complete_progress(self, operation_id: str, message: str = "Completed"):
        """
        Complete progress operation
        
        Args:
            operation_id: Operation identifier
            message: Completion message
        """
        if operation_id in self.active_dialogs:
            dialog = self.active_dialogs[operation_id]
            if dialog.is_open():
                dialog.complete(message)
            
            # Remove from active dialogs after delay
            self.parent.after(2000, lambda: self.active_dialogs.pop(operation_id, None))
    
    def close_progress(self, operation_id: str):
        """
        Close progress dialog
        
        Args:
            operation_id: Operation identifier
        """
        if operation_id in self.active_dialogs:
            dialog = self.active_dialogs[operation_id]
            dialog.close()
            del self.active_dialogs[operation_id]
    
    def close_all(self):
        """
        Close all active progress dialogs
        """
        for operation_id in list(self.active_dialogs.keys()):
            self.close_progress(operation_id)
    
    def get_progress(self, operation_id: str) -> Optional[ProgressDialog]:
        """
        Get progress dialog for operation
        
        Args:
            operation_id: Operation identifier
        
        Returns:
            ProgressDialog or None
        """
        return self.active_dialogs.get(operation_id)

def show_progress_dialog(parent, title: str = "Progress",
                        message: str = "Processing...",
                        cancelable: bool = True) -> ProgressDialog:
    """
    Convenience function to show progress dialog
    
    Args:
        parent: Parent window
        title: Dialog title
        message: Initial message
        cancelable: Whether operation can be canceled
    
    Returns:
        ProgressDialog: Created progress dialog
    """
    return ProgressDialog(
        parent,
        title=title,
        message=message,
        cancelable=cancelable
    )

def run_with_progress(parent, operation: Callable, 
                     title: str = "Progress",
                     message: str = "Processing...",
                     cancelable: bool = True,
                     on_complete: Optional[Callable] = None,
                     on_error: Optional[Callable] = None) -> ProgressDialog:
    """
    Run operation with progress dialog
    
    Args:
        parent: Parent window
        operation: Function to execute
        title: Dialog title
        message: Initial message
        cancelable: Whether operation can be canceled
        on_complete: Callback when operation completes
        on_error: Callback when operation fails
    
    Returns:
        ProgressDialog: Progress dialog
    """
    dialog = ProgressDialog(
        parent,
        title=title,
        message=message,
        cancelable=cancelable
    )
    
    def run_operation():
        """
        Run operation in background thread
        """
        try:
            # Execute operation
            result = operation(dialog)
            
            # Complete if not canceled
            if not dialog.was_canceled():
                dialog.complete("Operation completed successfully")
                
                if on_complete:
                    parent.after(0, lambda: on_complete(result))
            
        except Exception as e:
            # Handle error
            if not dialog.was_canceled():
                error_msg = f"Operation failed: {str(e)}"
                dialog.set_message(error_msg)
                dialog.set_progress(0)
                
                if on_error:
                    parent.after(0, lambda: on_error(e))
                else:
                    parent.after(2000, dialog.close)
    
    # Start operation in background
    threading.Thread(target=run_operation, daemon=True).start()
    
    return dialog