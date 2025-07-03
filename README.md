# HomeShow Desktop

A powerful Python desktop application for generating complete real estate websites (HTML/CSS/JS) through a guided creation wizard.

## 🏠 Overview

HomeShow Desktop is a comprehensive solution for real estate professionals to create stunning, responsive websites for their properties. The application features an intuitive GUI built with Tkinter, local SQLite database storage, and generates modern, SEO-optimized websites using Jinja2 templates.

## ✨ Features

### Core Functionality
- **Modern GUI Interface**: Clean, intuitive interface with tabbed navigation
- **Property Management**: Complete CRUD operations for property data
- **Website Generation**: Generate responsive HTML/CSS/JS websites
- **Template System**: Multiple professional templates (Modern, Luxury, Minimal, Bold)
- **Media Management**: Image processing, optimization, and gallery creation
- **Local Storage**: SQLite database for offline data management

### Advanced Features
- **AI Virtual Staging**: Integration with Replicate API for property staging
- **Interactive Floor Plans**: Hotspot-enabled floor plan viewer
- **Mortgage Calculator**: Built-in loan calculation tools
- **SEO Optimization**: Automatic meta tags and structured data
- **Responsive Design**: Mobile-first, cross-device compatibility
- **Image Gallery**: Lightbox gallery with navigation
- **Contact Forms**: Integrated lead capture forms
- **Map Integration**: Location display with OpenStreetMap

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd HomeShowDesktop
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
HomeShowDesktop/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── changelog.md           # Version history
├── core/                  # Core business logic
│   ├── __init__.py
│   ├── database.py        # SQLite operations
│   ├── property_manager.py # Property management
│   ├── media_handler.py   # Image processing
│   └── ai_staging.py      # AI virtual staging
├── gui/                   # User interface
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── dashboard.py       # Dashboard interface
│   ├── property_wizard.py # Property creation wizard
│   └── components/        # Reusable UI components
│       ├── __init__.py
│       ├── image_viewer.py
│       ├── property_card.py
│       ├── media_gallery.py
│       └── progress_dialog.py
├── generators/            # Website generation
│   ├── __init__.py
│   ├── site_generator.py  # Main generator
│   └── templates/         # HTML templates
│       └── modern/        # Modern template
│           ├── template.json
│           ├── index.html
│           ├── css/
│           │   └── style.css
│           └── js/
│               └── script.js
├── data/                  # Application data
│   ├── database.db        # SQLite database
│   └── projects/          # Generated websites
└── resources/             # Static resources
    ├── icons/
    └── templates/
```

## 🎯 Usage

### Creating a Property

1. **Launch the Application**: Run `python main.py`
2. **Open Property Wizard**: Click "New Property" from the dashboard
3. **Follow the Guided Steps**:
   - **Basic Information**: Enter property details (title, price, type, etc.)
   - **Media Upload**: Add photos, videos, and floor plans
   - **Property Features**: Specify bedrooms, bathrooms, amenities
   - **Location**: Set address and neighborhood information
   - **Advanced Options**: Configure SEO settings and special features
   - **Review**: Confirm all information before saving

### Generating a Website

1. **Select Property**: Choose from your property list
2. **Choose Template**: Select from available design templates
3. **Configure Options**: Set generation preferences
4. **Generate**: Click "Generate Website" to create HTML/CSS/JS files
5. **Preview**: View the generated website in your browser
6. **Deploy**: Upload the generated files to your web server

### Managing Properties

- **View All Properties**: Browse your property database
- **Edit Properties**: Update information and media
- **Duplicate Properties**: Create copies for similar listings
- **Export/Import**: Backup and restore property data
- **Search & Filter**: Find properties quickly

## 🎨 Templates

### Modern Template
- Clean, contemporary design
- Responsive layout
- Image slider hero section
- Interactive gallery
- Mortgage calculator
- Contact form integration
- SEO optimized

### Future Templates
- **Luxury**: Premium design for high-end properties
- **Minimal**: Clean, minimalist approach
- **Bold**: Eye-catching, vibrant design

## 🔧 Configuration

### AI Virtual Staging

To use AI virtual staging features:

1. Sign up for a Replicate API account
2. Get your API token
3. Configure in the application settings
4. Select staging styles and process images

### Database Settings

The application uses SQLite for local storage:
- Database file: `data/database.db`
- Automatic backup creation
- Export/import functionality

## 🚀 Building Executable

To create a standalone executable:

```bash
# Install PyInstaller (included in requirements.txt)
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name="HomeShow Desktop" main.py

# The executable will be in the dist/ folder
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Write modular, reusable code
- Update changelog.md for all changes
- Test thoroughly before committing

## 🐛 Troubleshooting

### Common Issues

**Application won't start**:
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Check for missing system libraries

**Database errors**:
- Ensure write permissions in the data/ directory
- Check if database file is corrupted
- Try deleting database.db to reset (will lose data)

**Image processing issues**:
- Verify Pillow installation
- Check image file formats (JPEG, PNG, GIF supported)
- Ensure sufficient disk space

**Website generation fails**:
- Check template files are present
- Verify output directory permissions
- Ensure all required property data is provided

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Tkinter**: Python's standard GUI toolkit
- **CustomTkinter**: Modern UI components
- **Jinja2**: Powerful templating engine
- **Pillow**: Image processing library
- **SQLite**: Lightweight database engine
- **Replicate**: AI model hosting platform

## 📞 Support

For support, feature requests, or bug reports:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting section

## 🔄 Version History

See [changelog.md](changelog.md) for detailed version history and updates.

---

**HomeShow Desktop** - Empowering real estate professionals with modern website generation tools.