#!/usr/bin/env python3
"""
Media Handler for HomeShow Desktop
Handles image processing, optimization, and media file management

Author: AI Assistant
Version: 1.0.0
"""

import os
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

try:
    from PIL import Image, ImageOps, ExifTags
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Image processing will be limited.")

class MediaHandler:
    """
    Handles media file processing and optimization
    """
    
    # Supported image formats
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    
    # Supported video formats
    SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'}
    
    # Image size presets
    IMAGE_SIZES = {
        'thumbnail': (300, 200),
        'medium': (800, 600),
        'large': (1200, 900),
        'original': None  # Keep original size
    }
    
    def __init__(self):
        """
        Initialize media handler
        """
        self.quality = 85  # JPEG quality
        self.optimize = True  # Enable optimization
    
    def is_image(self, file_path: str) -> bool:
        """
        Check if file is a supported image format
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is an image, False otherwise
        """
        extension = Path(file_path).suffix.lower()
        return extension in self.SUPPORTED_IMAGE_FORMATS
    
    def is_video(self, file_path: str) -> bool:
        """
        Check if file is a supported video format
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is a video, False otherwise
        """
        extension = Path(file_path).suffix.lower()
        return extension in self.SUPPORTED_VIDEO_FORMATS
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about a media file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file information
        """
        if not os.path.exists(file_path):
            return {}
        
        file_path = Path(file_path)
        stat = file_path.stat()
        
        info = {
            'filename': file_path.name,
            'extension': file_path.suffix.lower(),
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'modified': stat.st_mtime,
            'is_image': self.is_image(str(file_path)),
            'is_video': self.is_video(str(file_path))
        }
        
        # Get MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        info['mime_type'] = mime_type
        
        # Get image-specific information
        if info['is_image'] and PIL_AVAILABLE:
            try:
                with Image.open(file_path) as img:
                    info['width'] = img.width
                    info['height'] = img.height
                    info['format'] = img.format
                    info['mode'] = img.mode
                    
                    # Get EXIF data if available
                    exif_data = self._get_exif_data(img)
                    if exif_data:
                        info['exif'] = exif_data
            except Exception as e:
                print(f"Error reading image info for {file_path}: {e}")
        
        return info
    
    def _get_exif_data(self, image: 'Image.Image') -> Dict[str, Any]:
        """
        Extract EXIF data from image
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary containing EXIF data
        """
        if not PIL_AVAILABLE:
            return {}
        
        exif_data = {}
        
        try:
            exif = image._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    exif_data[tag] = value
        except Exception:
            pass
        
        return exif_data
    
    def process_image(self, image_path: str, output_dir: str) -> Dict[str, str]:
        """
        Process an image by creating multiple sizes and optimizing
        
        Args:
            image_path: Path to the original image
            output_dir: Directory to save processed images
            
        Returns:
            Dictionary mapping size names to file paths
        """
        if not PIL_AVAILABLE:
            print("Pillow not available. Skipping image processing.")
            return {'original': image_path}
        
        if not self.is_image(image_path):
            return {'original': image_path}
        
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            original_path = Path(image_path)
            base_name = original_path.stem
            
            processed_files = {}
            
            with Image.open(image_path) as img:
                # Fix orientation based on EXIF data
                img = ImageOps.exif_transpose(img)
                
                # Convert to RGB if necessary (for JPEG output)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Process each size
                for size_name, dimensions in self.IMAGE_SIZES.items():
                    if dimensions is None:  # Original size
                        output_path = output_dir / f"{base_name}_original.jpg"
                        img.save(
                            output_path,
                            'JPEG',
                            quality=self.quality,
                            optimize=self.optimize
                        )
                    else:
                        # Resize image
                        resized_img = img.copy()
                        resized_img.thumbnail(dimensions, Image.Resampling.LANCZOS)
                        
                        output_path = output_dir / f"{base_name}_{size_name}.jpg"
                        resized_img.save(
                            output_path,
                            'JPEG',
                            quality=self.quality,
                            optimize=self.optimize
                        )
                    
                    # Store relative path from project root
                    project_root = Path(__file__).parent.parent
                    relative_path = output_path.relative_to(project_root)
                    processed_files[size_name] = str(relative_path)
            
            return processed_files
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return {'original': image_path}
    
    def create_thumbnail(self, image_path: str, output_path: str, 
                        size: Tuple[int, int] = (300, 200)) -> bool:
        """
        Create a thumbnail from an image
        
        Args:
            image_path: Path to the original image
            output_path: Path for the thumbnail
            size: Thumbnail size (width, height)
            
        Returns:
            True if successful, False otherwise
        """
        if not PIL_AVAILABLE or not self.is_image(image_path):
            return False
        
        try:
            with Image.open(image_path) as img:
                # Fix orientation
                img = ImageOps.exif_transpose(img)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                output_dir = Path(output_path).parent
                output_dir.mkdir(parents=True, exist_ok=True)
                
                img.save(
                    output_path,
                    'JPEG',
                    quality=self.quality,
                    optimize=self.optimize
                )
                
                return True
                
        except Exception as e:
            print(f"Error creating thumbnail for {image_path}: {e}")
            return False
    
    def optimize_image(self, image_path: str, output_path: str = None, 
                      max_width: int = 1920, max_height: int = 1080) -> bool:
        """
        Optimize an image by reducing size and file size
        
        Args:
            image_path: Path to the original image
            output_path: Path for optimized image (optional)
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            True if successful, False otherwise
        """
        if not PIL_AVAILABLE or not self.is_image(image_path):
            return False
        
        if output_path is None:
            output_path = image_path
        
        try:
            with Image.open(image_path) as img:
                # Fix orientation
                img = ImageOps.exif_transpose(img)
                
                # Resize if too large
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Save optimized image
                output_dir = Path(output_path).parent
                output_dir.mkdir(parents=True, exist_ok=True)
                
                img.save(
                    output_path,
                    'JPEG',
                    quality=self.quality,
                    optimize=self.optimize
                )
                
                return True
                
        except Exception as e:
            print(f"Error optimizing image {image_path}: {e}")
            return False
    
    def get_image_dimensions(self, image_path: str) -> Optional[Tuple[int, int]]:
        """
        Get image dimensions without loading the full image
        
        Args:
            image_path: Path to the image
            
        Returns:
            Tuple of (width, height) or None if error
        """
        if not PIL_AVAILABLE or not self.is_image(image_path):
            return None
        
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception:
            return None
    
    def validate_media_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a media file and return validation results
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing validation results
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        
        # Check if file exists
        if not os.path.exists(file_path):
            result['errors'].append('File does not exist')
            return result
        
        # Get file info
        file_info = self.get_file_info(file_path)
        result['file_info'] = file_info
        
        # Check file size (max 50MB)
        max_size_mb = 50
        if file_info.get('size_mb', 0) > max_size_mb:
            result['errors'].append(f'File size ({file_info["size_mb"]}MB) exceeds maximum ({max_size_mb}MB)')
        
        # Check if supported format
        if not (file_info.get('is_image') or file_info.get('is_video')):
            result['errors'].append('Unsupported file format')
        
        # Image-specific validation
        if file_info.get('is_image'):
            width = file_info.get('width', 0)
            height = file_info.get('height', 0)
            
            # Check minimum dimensions
            min_width, min_height = 100, 100
            if width < min_width or height < min_height:
                result['errors'].append(f'Image dimensions ({width}x{height}) too small (minimum {min_width}x{min_height})')
            
            # Check maximum dimensions
            max_width, max_height = 8000, 8000
            if width > max_width or height > max_height:
                result['warnings'].append(f'Image dimensions ({width}x{height}) very large (recommended max {max_width}x{max_height})')
        
        # Set valid flag
        result['valid'] = len(result['errors']) == 0
        
        return result
    
    def batch_process_images(self, image_paths: List[str], output_dir: str) -> Dict[str, Dict[str, str]]:
        """
        Process multiple images in batch
        
        Args:
            image_paths: List of image file paths
            output_dir: Directory to save processed images
            
        Returns:
            Dictionary mapping original paths to processed file dictionaries
        """
        results = {}
        
        for image_path in image_paths:
            if self.is_image(image_path):
                try:
                    processed_files = self.process_image(image_path, output_dir)
                    results[image_path] = processed_files
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
                    results[image_path] = {'original': image_path}
            else:
                print(f"Skipping non-image file: {image_path}")
        
        return results
    
    def cleanup_processed_images(self, processed_files: Dict[str, str]):
        """
        Clean up processed image files
        
        Args:
            processed_files: Dictionary of processed file paths
        """
        project_root = Path(__file__).parent.parent
        
        for size_name, relative_path in processed_files.items():
            try:
                file_path = project_root / relative_path
                if file_path.exists():
                    file_path.unlink()
            except Exception as e:
                print(f"Error removing processed file {relative_path}: {e}")
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get list of supported file formats
        
        Returns:
            Dictionary with 'images' and 'videos' keys containing format lists
        """
        return {
            'images': list(self.SUPPORTED_IMAGE_FORMATS),
            'videos': list(self.SUPPORTED_VIDEO_FORMATS)
        }