#!/usr/bin/env python3
"""
Site Generator for HomeShow Desktop
Generates complete real estate websites from property data

Author: AI Assistant
Version: 1.0.0
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json
import base64
from jinja2 import Environment, FileSystemLoader, Template
from PIL import Image
import threading

@dataclass
class WebsiteTemplate:
    """
    Website template configuration
    """
    id: str
    name: str
    description: str
    preview_image: str
    template_dir: str
    style: str  # modern, luxury, minimal, bold
    features: List[str]
    responsive: bool = True
    seo_optimized: bool = True

class SiteGenerator:
    """
    Main site generator class for creating real estate websites
    """
    
    def __init__(self, templates_dir: str, output_dir: str):
        """
        Initialize site generator
        
        Args:
            templates_dir: Directory containing website templates
            output_dir: Base directory for generated websites
        """
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.templates = {}
        self.jinja_env = None
        
        # Ensure directories exist
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load available templates
        self.load_templates()
        
        # Initialize Jinja2 environment
        self.setup_jinja_environment()
    
    def load_templates(self):
        """
        Load available website templates
        """
        # Default templates
        default_templates = [
            WebsiteTemplate(
                id="modern",
                name="Modern",
                description="Clean, contemporary design with smooth animations",
                preview_image="modern_preview.jpg",
                template_dir="modern",
                style="modern",
                features=["Responsive", "Image Gallery", "Contact Form", "SEO Optimized"]
            ),
            WebsiteTemplate(
                id="luxury",
                name="Luxury",
                description="Elegant design for high-end properties",
                preview_image="luxury_preview.jpg",
                template_dir="luxury",
                style="luxury",
                features=["Responsive", "Video Background", "Virtual Tour", "Premium Styling"]
            ),
            WebsiteTemplate(
                id="minimal",
                name="Minimal",
                description="Simple, clean design focusing on content",
                preview_image="minimal_preview.jpg",
                template_dir="minimal",
                style="minimal",
                features=["Responsive", "Fast Loading", "Clean Layout", "Mobile First"]
            ),
            WebsiteTemplate(
                id="bold",
                name="Bold",
                description="Eye-catching design with vibrant colors",
                preview_image="bold_preview.jpg",
                template_dir="bold",
                style="bold",
                features=["Responsive", "Animated Elements", "Bold Typography", "Interactive"]
            )
        ]
        
        for template in default_templates:
            self.templates[template.id] = template
        
        # Load custom templates from directory
        self.load_custom_templates()
    
    def load_custom_templates(self):
        """
        Load custom templates from templates directory
        """
        if not self.templates_dir.exists():
            return
        
        for template_dir in self.templates_dir.iterdir():
            if template_dir.is_dir():
                config_file = template_dir / "template.json"
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        
                        template = WebsiteTemplate(
                            id=config.get('id', template_dir.name),
                            name=config.get('name', template_dir.name.title()),
                            description=config.get('description', ''),
                            preview_image=config.get('preview_image', ''),
                            template_dir=str(template_dir),
                            style=config.get('style', 'custom'),
                            features=config.get('features', []),
                            responsive=config.get('responsive', True),
                            seo_optimized=config.get('seo_optimized', True)
                        )
                        
                        self.templates[template.id] = template
                        
                    except Exception as e:
                        print(f"Error loading template {template_dir.name}: {e}")
    
    def setup_jinja_environment(self):
        """
        Setup Jinja2 template environment
        """
        # Create template loader
        loader = FileSystemLoader(str(self.templates_dir))
        
        # Create environment with custom filters
        self.jinja_env = Environment(
            loader=loader,
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.jinja_env.filters['format_price'] = self.format_price
        self.jinja_env.filters['format_area'] = self.format_area
        self.jinja_env.filters['format_date'] = self.format_date
        self.jinja_env.filters['slugify'] = self.slugify
        self.jinja_env.filters['image_url'] = self.image_url
        self.jinja_env.filters['json_encode'] = json.dumps
    
    def generate_website(self, property_data: Dict[str, Any], 
                        template_id: str,
                        output_name: str,
                        options: Dict[str, Any] = None,
                        progress_callback: Optional[Callable] = None) -> str:
        """
        Generate complete website for property
        
        Args:
            property_data: Property information
            template_id: Template to use
            output_name: Name for output directory
            options: Generation options
            progress_callback: Progress update callback
        
        Returns:
            str: Path to generated website
        """
        if template_id not in self.templates:
            raise ValueError(f"Template '{template_id}' not found")
        
        template = self.templates[template_id]
        options = options or {}
        
        # Create output directory
        site_output_dir = self.output_dir / output_name
        if site_output_dir.exists():
            shutil.rmtree(site_output_dir)
        site_output_dir.mkdir(parents=True)
        
        try:
            # Update progress
            if progress_callback:
                progress_callback(10, "Preparing template data...")
            
            # Prepare template data
            template_data = self.prepare_template_data(property_data, options)
            
            # Update progress
            if progress_callback:
                progress_callback(20, "Processing media files...")
            
            # Process and copy media files
            self.process_media_files(property_data, site_output_dir, progress_callback)
            
            # Update progress
            if progress_callback:
                progress_callback(40, "Generating HTML pages...")
            
            # Generate HTML pages
            self.generate_html_pages(template, template_data, site_output_dir, progress_callback)
            
            # Update progress
            if progress_callback:
                progress_callback(70, "Copying assets...")
            
            # Copy template assets
            self.copy_template_assets(template, site_output_dir)
            
            # Update progress
            if progress_callback:
                progress_callback(90, "Finalizing website...")
            
            # Generate additional files
            self.generate_additional_files(template_data, site_output_dir)
            
            # Update progress
            if progress_callback:
                progress_callback(100, "Website generated successfully!")
            
            return str(site_output_dir)
            
        except Exception as e:
            # Clean up on error
            if site_output_dir.exists():
                shutil.rmtree(site_output_dir)
            raise e
    
    def prepare_template_data(self, property_data: Dict[str, Any], 
                            options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare data for template rendering
        
        Args:
            property_data: Property information
            options: Generation options
        
        Returns:
            Dict containing template data
        """
        # Base template data
        template_data = {
            'property': property_data,
            'site': {
                'title': property_data.get('title', 'Property Listing'),
                'description': property_data.get('description', ''),
                'generated_date': datetime.now().isoformat(),
                'generator': 'HomeShow Desktop',
                'version': '1.0.0'
            },
            'options': options,
            'features': {
                'contact_form': options.get('contact_form', True),
                'image_gallery': options.get('image_gallery', True),
                'virtual_tour': options.get('virtual_tour', False),
                'mortgage_calculator': options.get('mortgage_calculator', True),
                'map_integration': options.get('map_integration', True),
                'social_sharing': options.get('social_sharing', True)
            }
        }
        
        # Add SEO data
        template_data['seo'] = self.generate_seo_data(property_data)
        
        # Add structured data
        template_data['structured_data'] = self.generate_structured_data(property_data)
        
        return template_data
    
    def process_media_files(self, property_data: Dict[str, Any], 
                           output_dir: Path,
                           progress_callback: Optional[Callable] = None):
        """
        Process and copy media files
        
        Args:
            property_data: Property data
            output_dir: Output directory
            progress_callback: Progress callback
        """
        media_dir = output_dir / 'media'
        media_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (media_dir / 'images').mkdir(exist_ok=True)
        (media_dir / 'thumbnails').mkdir(exist_ok=True)
        (media_dir / 'videos').mkdir(exist_ok=True)
        
        media_files = property_data.get('media', [])
        total_files = len(media_files)
        
        for i, media in enumerate(media_files):
            if progress_callback:
                progress = 20 + (20 * i / total_files) if total_files > 0 else 40
                progress_callback(progress, f"Processing {media.get('name', 'media file')}...")
            
            self.process_single_media_file(media, media_dir)
    
    def process_single_media_file(self, media: Dict[str, Any], media_dir: Path):
        """
        Process single media file
        
        Args:
            media: Media file data
            media_dir: Media directory
        """
        source_path = Path(media.get('path', ''))
        if not source_path.exists():
            return
        
        media_type = media.get('type', 'image')
        file_name = source_path.name
        
        if media_type == 'image':
            # Copy original image
            dest_path = media_dir / 'images' / file_name
            shutil.copy2(source_path, dest_path)
            
            # Create thumbnail
            self.create_thumbnail(source_path, media_dir / 'thumbnails' / file_name)
            
            # Create optimized versions
            self.create_optimized_images(source_path, media_dir / 'images')
            
        elif media_type == 'video':
            # Copy video file
            dest_path = media_dir / 'videos' / file_name
            shutil.copy2(source_path, dest_path)
    
    def create_thumbnail(self, source_path: Path, dest_path: Path, size: tuple = (300, 200)):
        """
        Create thumbnail image
        
        Args:
            source_path: Source image path
            dest_path: Destination path
            size: Thumbnail size
        """
        try:
            with Image.open(source_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                img.save(dest_path, 'JPEG', quality=85, optimize=True)
                
        except Exception as e:
            print(f"Error creating thumbnail for {source_path}: {e}")
    
    def create_optimized_images(self, source_path: Path, images_dir: Path):
        """
        Create optimized image versions
        
        Args:
            source_path: Source image path
            images_dir: Images directory
        """
        try:
            with Image.open(source_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                base_name = source_path.stem
                
                # Create different sizes
                sizes = {
                    'small': (800, 600),
                    'medium': (1200, 900),
                    'large': (1920, 1440)
                }
                
                for size_name, size in sizes.items():
                    # Only create if image is larger than target size
                    if img.width > size[0] or img.height > size[1]:
                        resized = img.copy()
                        resized.thumbnail(size, Image.Resampling.LANCZOS)
                        
                        output_path = images_dir / f"{base_name}_{size_name}.jpg"
                        resized.save(output_path, 'JPEG', quality=85, optimize=True)
                
        except Exception as e:
            print(f"Error creating optimized images for {source_path}: {e}")
    
    def generate_html_pages(self, template: WebsiteTemplate, 
                           template_data: Dict[str, Any],
                           output_dir: Path,
                           progress_callback: Optional[Callable] = None):
        """
        Generate HTML pages
        
        Args:
            template: Website template
            template_data: Template data
            output_dir: Output directory
            progress_callback: Progress callback
        """
        # Get template directory
        if template.template_dir.startswith('/'):
            template_dir = Path(template.template_dir)
        else:
            template_dir = self.templates_dir / template.template_dir
        
        # Create default template if not exists
        if not template_dir.exists():
            self.create_default_template(template_dir, template.style)
        
        # Generate main pages
        pages = {
            'index.html': 'index.html',
            'gallery.html': 'gallery.html',
            'contact.html': 'contact.html',
            'details.html': 'details.html'
        }
        
        for i, (output_file, template_file) in enumerate(pages.items()):
            if progress_callback:
                progress = 40 + (30 * i / len(pages))
                progress_callback(progress, f"Generating {output_file}...")
            
            self.generate_single_page(template_file, template_data, output_dir / output_file)
    
    def generate_single_page(self, template_file: str, 
                           template_data: Dict[str, Any],
                           output_path: Path):
        """
        Generate single HTML page
        
        Args:
            template_file: Template file name
            template_data: Template data
            output_path: Output file path
        """
        try:
            # Load template
            template = self.jinja_env.get_template(template_file)
            
            # Render template
            html_content = template.render(**template_data)
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
        except Exception as e:
            print(f"Error generating {template_file}: {e}")
            # Create basic fallback page
            self.create_fallback_page(output_path, template_data)
    
    def create_fallback_page(self, output_path: Path, template_data: Dict[str, Any]):
        """
        Create basic fallback HTML page
        
        Args:
            output_path: Output file path
            template_data: Template data
        """
        property_data = template_data.get('property', {})
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{property_data.get('title', 'Property Listing')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .property-info {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{property_data.get('title', 'Property Listing')}</h1>
        </div>
        <div class="property-info">
            <p>{property_data.get('description', 'No description available.')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def copy_template_assets(self, template: WebsiteTemplate, output_dir: Path):
        """
        Copy template assets (CSS, JS, images)
        
        Args:
            template: Website template
            output_dir: Output directory
        """
        # Get template directory
        if template.template_dir.startswith('/'):
            template_dir = Path(template.template_dir)
        else:
            template_dir = self.templates_dir / template.template_dir
        
        # Create default assets if template doesn't exist
        if not template_dir.exists():
            self.create_default_assets(output_dir, template.style)
            return
        
        # Copy assets directories
        asset_dirs = ['css', 'js', 'images', 'fonts']
        
        for asset_dir in asset_dirs:
            source_dir = template_dir / asset_dir
            if source_dir.exists():
                dest_dir = output_dir / asset_dir
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
    
    def create_default_template(self, template_dir: Path, style: str):
        """
        Create default template files
        
        Args:
            template_dir: Template directory
            style: Template style
        """
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Create basic index.html template
        index_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ property.title | default('Property Listing') }}</title>
    <meta name="description" content="{{ property.description | default('') }}">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <div class="container">
                <h1>{{ property.title | default('Property Listing') }}</h1>
            </div>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <div class="container">
                {% if property.media and property.media|length > 0 %}
                <img src="media/images/{{ property.media[0].name }}" alt="{{ property.title }}" class="hero-image">
                {% endif %}
                <div class="hero-content">
                    <h2>{{ property.title | default('Beautiful Property') }}</h2>
                    <p class="price">${{ property.price | format_price }}</p>
                    <p class="location">{{ property.location | default('') }}</p>
                </div>
            </div>
        </section>
        
        <section class="details">
            <div class="container">
                <h3>Property Details</h3>
                <p>{{ property.description | default('No description available.') }}</p>
                
                {% if property.features %}
                <div class="features">
                    <h4>Features</h4>
                    <ul>
                    {% for feature in property.features %}
                        <li>{{ feature }}</li>
                    {% endfor %}
                    </ul>
                </div>
                {% endif %}
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; {{ site.generated_date[:4] }} Generated by {{ site.generator }}</p>
        </div>
    </footer>
    
    <script src="js/script.js"></script>
</body>
</html>
        """
        
        with open(template_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(index_template)
        
        # Create other template files
        for page in ['gallery.html', 'contact.html', 'details.html']:
            with open(template_dir / page, 'w', encoding='utf-8') as f:
                f.write(index_template)  # Use same template for now
    
    def create_default_assets(self, output_dir: Path, style: str):
        """
        Create default CSS and JS assets
        
        Args:
            output_dir: Output directory
            style: Template style
        """
        # Create CSS directory and file
        css_dir = output_dir / 'css'
        css_dir.mkdir(exist_ok=True)
        
        css_content = self.get_default_css(style)
        with open(css_dir / 'style.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Create JS directory and file
        js_dir = output_dir / 'js'
        js_dir.mkdir(exist_ok=True)
        
        js_content = self.get_default_js()
        with open(js_dir / 'script.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
    
    def get_default_css(self, style: str) -> str:
        """
        Get default CSS content based on style
        
        Args:
            style: Template style
        
        Returns:
            str: CSS content
        """
        base_css = """
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    background: #fff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

nav {
    padding: 1rem 0;
}

nav h1 {
    color: #2c3e50;
}

/* Hero section */
.hero {
    padding: 2rem 0;
    background: #f8f9fa;
}

.hero-image {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.hero-content h2 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #2c3e50;
}

.price {
    font-size: 2rem;
    font-weight: bold;
    color: #e74c3c;
    margin-bottom: 0.5rem;
}

.location {
    font-size: 1.2rem;
    color: #7f8c8d;
}

/* Details section */
.details {
    padding: 3rem 0;
}

.details h3 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.features {
    margin-top: 2rem;
}

.features h4 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #34495e;
}

.features ul {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 0.5rem;
}

.features li {
    padding: 0.5rem;
    background: #ecf0f1;
    border-radius: 4px;
}

/* Footer */
footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-content h2 {
        font-size: 2rem;
    }
    
    .price {
        font-size: 1.5rem;
    }
    
    .features ul {
        grid-template-columns: 1fr;
    }
}
        """
        
        # Add style-specific modifications
        if style == 'luxury':
            base_css += """
/* Luxury style modifications */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #2c3e50;
}

.hero {
    background: rgba(255, 255, 255, 0.95);
}

.price {
    color: #d4af37;
}
            """
        elif style == 'minimal':
            base_css += """
/* Minimal style modifications */
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background: #fafafa;
}

.hero {
    background: white;
}

header {
    border-bottom: 1px solid #eee;
    box-shadow: none;
}
            """
        elif style == 'bold':
            base_css += """
/* Bold style modifications */
body {
    background: #1a1a1a;
    color: white;
}

.hero {
    background: #ff6b6b;
    color: white;
}

header {
    background: #4ecdc4;
}

.price {
    color: #ffe66d;
}
            """
        
        return base_css
    
    def get_default_js(self) -> str:
        """
        Get default JavaScript content
        
        Returns:
            str: JavaScript content
        """
        return """
// HomeShow Desktop Generated Website
// Basic functionality

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Simple image gallery
    const galleryImages = document.querySelectorAll('.gallery img');
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            // Create modal overlay
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.9);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
                cursor: pointer;
            `;
            
            const modalImg = document.createElement('img');
            modalImg.src = this.src;
            modalImg.style.cssText = `
                max-width: 90%;
                max-height: 90%;
                object-fit: contain;
            `;
            
            modal.appendChild(modalImg);
            document.body.appendChild(modal);
            
            // Close modal on click
            modal.addEventListener('click', () => {
                document.body.removeChild(modal);
            });
        });
    });
    
    console.log('HomeShow Desktop website loaded successfully!');
});
        """
    
    def generate_additional_files(self, template_data: Dict[str, Any], output_dir: Path):
        """
        Generate additional files (sitemap, robots.txt, etc.)
        
        Args:
            template_data: Template data
            output_dir: Output directory
        """
        # Generate robots.txt
        robots_content = """User-agent: *
Allow: /

Sitemap: sitemap.xml
"""
        
        with open(output_dir / 'robots.txt', 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        # Generate sitemap.xml
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>index.html</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>gallery.html</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>contact.html</loc>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
    <url>
        <loc>details.html</loc>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
</urlset>
"""
        
        with open(output_dir / 'sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
    
    def generate_seo_data(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate SEO metadata
        
        Args:
            property_data: Property data
        
        Returns:
            Dict containing SEO data
        """
        title = property_data.get('title', 'Property Listing')
        description = property_data.get('description', '')[:160]  # Limit to 160 chars
        
        return {
            'title': title,
            'description': description,
            'keywords': f"real estate, property, {property_data.get('location', '')}, {property_data.get('type', '')}",
            'og_title': title,
            'og_description': description,
            'og_type': 'website',
            'twitter_card': 'summary_large_image'
        }
    
    def generate_structured_data(self, property_data: Dict[str, Any]) -> str:
        """
        Generate JSON-LD structured data
        
        Args:
            property_data: Property data
        
        Returns:
            str: JSON-LD structured data
        """
        structured_data = {
            "@context": "https://schema.org",
            "@type": "RealEstateListing",
            "name": property_data.get('title', ''),
            "description": property_data.get('description', ''),
            "url": "index.html"
        }
        
        if property_data.get('price'):
            structured_data["offers"] = {
                "@type": "Offer",
                "price": property_data['price'],
                "priceCurrency": "USD"
            }
        
        if property_data.get('location'):
            structured_data["address"] = {
                "@type": "PostalAddress",
                "addressLocality": property_data['location']
            }
        
        return json.dumps(structured_data, indent=2)
    
    # Template filters
    def format_price(self, price) -> str:
        """
        Format price for display
        
        Args:
            price: Price value
        
        Returns:
            str: Formatted price
        """
        if isinstance(price, (int, float)):
            return f"{price:,.0f}"
        return str(price)
    
    def format_area(self, area) -> str:
        """
        Format area for display
        
        Args:
            area: Area value
        
        Returns:
            str: Formatted area
        """
        if isinstance(area, (int, float)):
            return f"{area:,.0f} sq ft"
        return str(area)
    
    def format_date(self, date_str) -> str:
        """
        Format date for display
        
        Args:
            date_str: Date string
        
        Returns:
            str: Formatted date
        """
        try:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date_obj.strftime('%B %d, %Y')
        except:
            return str(date_str)
    
    def slugify(self, text) -> str:
        """
        Convert text to URL-friendly slug
        
        Args:
            text: Text to slugify
        
        Returns:
            str: Slugified text
        """
        import re
        text = str(text).lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    def image_url(self, filename) -> str:
        """
        Generate image URL
        
        Args:
            filename: Image filename
        
        Returns:
            str: Image URL
        """
        return f"media/images/{filename}"
    
    def get_available_templates(self) -> List[WebsiteTemplate]:
        """
        Get list of available templates
        
        Returns:
            List of WebsiteTemplate objects
        """
        return list(self.templates.values())
    
    def get_template(self, template_id: str) -> Optional[WebsiteTemplate]:
        """
        Get specific template by ID
        
        Args:
            template_id: Template identifier
        
        Returns:
            WebsiteTemplate or None
        """
        return self.templates.get(template_id)