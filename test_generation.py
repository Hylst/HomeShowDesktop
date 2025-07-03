#!/usr/bin/env python3
"""
Test script for HomeShow Desktop website generation
This script demonstrates the website generation functionality
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.database import DatabaseManager
from core.property_manager import PropertyManager
from generators.site_generator import SiteGenerator, WebsiteTemplate

def create_sample_property():
    """
    Create a sample property for testing website generation
    """
    # Initialize database and property manager
    db_manager = DatabaseManager()
    property_manager = PropertyManager(db_manager)
    
    # Sample property data
    property_data = {
        'title': 'Luxury Modern Villa',
        'description': 'A stunning modern villa with panoramic city views, featuring contemporary design, premium finishes, and state-of-the-art amenities. This exceptional property offers the perfect blend of luxury and comfort.',
        'price': 1250000,
        'property_type': 'Villa',
        'bedrooms': 4,
        'bathrooms': 3,
        'area': 3500,
        'address': '123 Hillside Drive, Beverly Hills, CA 90210',
        'city': 'Beverly Hills',
        'state': 'California',
        'zip_code': '90210',
        'country': 'United States',
        'latitude': 34.0736,
        'longitude': -118.4004,
        'year_built': 2020,
        'lot_size': 8000,
        'garage_spaces': 2,
        'features': 'Swimming Pool,Garden,Garage,Fireplace,Balcony,Modern Kitchen,Walk-in Closet,Home Theater',
        'amenities': 'Gym,Spa,Wine Cellar,Smart Home System,Security System',
        'neighborhood_info': 'Located in the prestigious Beverly Hills area, close to high-end shopping, fine dining, and entertainment venues.',
        'schools': 'Beverly Hills High School, Horace Mann Elementary',
        'transportation': 'Easy access to major highways and public transportation',
        'agent_name': 'Sarah Johnson',
        'agent_email': 'sarah.johnson@luxuryrealty.com',
        'agent_phone': '+1 (555) 123-4567',
        'agency_name': 'Luxury Realty Group',
        'seo_title': 'Luxury Modern Villa in Beverly Hills - $1,250,000',
        'seo_description': 'Discover this stunning 4-bedroom modern villa in Beverly Hills with panoramic views, premium finishes, and luxury amenities.',
        'seo_keywords': 'luxury villa, Beverly Hills real estate, modern home, premium property'
    }
    
    # Create the property
    property_id, media_dir = property_manager.create_property_with_media(property_data, [])
    print(f"Created sample property with ID: {property_id}")
    print(f"Media directory: {media_dir}")
    
    return property_id, property_data

def generate_sample_website(property_id, property_data):
    """
    Generate a sample website for the created property
    """
    # Set up paths
    templates_dir = project_root / "generators" / "templates"
    output_base_dir = project_root / "data" / "projects"
    
    # Initialize site generator
    site_generator = SiteGenerator(str(templates_dir), str(output_base_dir))
    
    # Generate the website
    try:
        website_path = site_generator.generate_website(
            property_data=property_data,
            template_id="modern",
            output_name=f"property_{property_id}_website",
            options={
                'contact_form': True,
                'image_gallery': True,
                'mortgage_calculator': True,
                'map_integration': True,
                'social_sharing': True
            }
        )
        
        if website_path:
            print(f"\n✅ Website generated successfully!")
            print(f"📁 Output directory: {website_path}")
            print(f"🌐 Open index.html in your browser to view the website")
            
            # List generated files
            output_path = Path(website_path)
            if output_path.exists():
                files = list(output_path.rglob('*'))
                print(f"📊 Generated files: {len([f for f in files if f.is_file()])} files")
                print("\n📄 Generated files:")
                for file_path in files:
                    if file_path.is_file():
                        rel_path = file_path.relative_to(output_path)
                        print(f"   - {rel_path}")
                    
            return str(Path(website_path) / "index.html")
        else:
            print(f"❌ Website generation failed")
            return None
            
    except Exception as e:
        print(f"❌ Error during website generation: {str(e)}")
        return None

def main():
    """
    Main test function
    """
    print("🏠 HomeShow Desktop - Website Generation Test")
    print("=" * 50)
    
    try:
        # Create sample property
        print("\n1. Creating sample property...")
        property_id, property_data = create_sample_property()
        
        # Generate website
        print("\n2. Generating website...")
        website_path = generate_sample_website(property_id, property_data)
        
        if website_path:
            print(f"\n🎉 Test completed successfully!")
            print(f"\n📖 Instructions:")
            print(f"   1. Navigate to: {website_path}")
            print(f"   2. Open the file in your web browser")
            print(f"   3. Explore the generated real estate website")
            print(f"\n💡 The website includes:")
            print(f"   - Responsive design for all devices")
            print(f"   - Interactive image gallery")
            print(f"   - Mortgage calculator")
            print(f"   - Contact form")
            print(f"   - SEO optimization")
            print(f"   - Modern styling and animations")
        else:
            print("\n❌ Test failed - website generation unsuccessful")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()