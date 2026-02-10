# Vacation Rental Django Project

A Django web application for managing vacation rental properties with location-based search, AJAX autocomplete, image uploads, and a comprehensive admin panel.

## Features

- Property listing with pagination (5 properties per page)
- Location-based search with AJAX autocomplete (shows 5 suggestions)
- Image upload and management (upload files or use external URLs)
- Image gallery with slider for each property
- Admin panel with inline image management and preview
- RESTful API with Django REST Framework
- Media storage for uploaded files
- Simple, clean frontend with vanilla JavaScript

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Admin Panel](#admin-panel)
- [Frontend Features](#frontend-features)
- [Configuration](#configuration)
- [CSV Import](#csv-import)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [License](#license)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)

## Installation

### 1. Navigate to Project Directory

```bash
cd vacation_rental
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django (>=5.0, <7.0)
- Django REST Framework (>=3.14.0)
- django-cors-headers (>=4.0.0)
- Pillow (>=10.0.0)

### 4. Run Database Migrations

```bash
# Create migration files
python manage.py makemigrations rentals

# Apply migrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Import Sample Data (Optional)

```bash
python manage.py import_csv path/to/vacation_rental_data.csv
```

Example:
```bash
python manage.py import_csv ../vacation_rental_data.csv
```

### 7. Run Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

- Homepage: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/properties/

## Project Structure

```
vacation_rental/
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── db.sqlite3                  # SQLite database
├── config/                     # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI configuration
├── rentals/                    # Main application
│   ├── management/
│   │   └── commands/
│   │       └── import_csv.py  # CSV import command
│   ├── templates/
│   │   ├── admin/
│   │   │   └── base_site.html # Custom admin template
│   │   └── rentals/
│   │       ├── base.html      # Base template
│   │       ├── home.html      # Homepage
│   │       └── property_detail.html  # Property detail
│   ├── models.py              # Data models
│   ├── views.py               # Views and API logic
│   ├── serializers.py         # DRF serializers
│   ├── admin.py               # Admin configuration
│   └── urls.py                # App URLs
├── media/                      # Uploaded files (tracked in Git)
│   └── property_images/       # Property images
├── staticfiles/                # Collected static files
└── venv/                       # Virtual environment
```

## Database Models

### Location Model

Stores location information for properties.

**Fields:**
- `location_id` - Primary key (CharField, max 20)
- `location_name` - Location name (CharField, max 200)
- `location_city` - City name (CharField, max 100)
- `location_state` - State/province (CharField, max 100)
- `location_country` - Country (CharField, max 100)
- `location_zip` - Postal code (CharField, max 20)
- `location_latitude` - Latitude (DecimalField, 9 digits, 6 decimals)
- `location_longitude` - Longitude (DecimalField, 9 digits, 6 decimals)
- `location_description` - Location description (TextField)

**Relationships:**
- One location can have many properties

### Property Model

Stores property details.

**Fields:**
- `property_id` - Primary key (CharField, max 20)
- `property_name` - Property name (CharField, max 200)
- `property_type` - Type (CharField with choices: Villa, Condo, Chalet, Cabin, Loft, Penthouse, House, Townhouse, Suite)
- `bedrooms` - Number of bedrooms (IntegerField)
- `bathrooms` - Number of bathrooms (DecimalField, 3 digits, 1 decimal)
- `max_guests` - Maximum guests (IntegerField)
- `price_per_night` - Nightly rate (DecimalField, 10 digits, 2 decimals)
- `property_description` - Description (TextField)
- `location` - Foreign key to Location
- `created_at` - Created timestamp (DateTimeField, auto)
- `updated_at` - Updated timestamp (DateTimeField, auto)

**Relationships:**
- Many properties belong to one location
- One property can have many images

### PropertyImage Model

Stores images for properties.

**Fields:**
- `image_id` - Unique identifier (CharField, max 20, unique)
- `property` - Foreign key to Property
- `image_file` - Uploaded image (ImageField, upload_to='property_images/', optional)
- `image_url` - External image URL (URLField, max 500, optional)
- `image_caption` - Image caption (CharField, max 300, optional)
- `image_order` - Display order (IntegerField, default 0)

**Methods:**
- `get_image_url()` - Returns image URL (uploaded file if available, otherwise external URL)

**Relationships:**
- Many images belong to one property

**Image Priority:**
If both `image_file` and `image_url` are provided, the uploaded file takes priority.

## API Endpoints

### Properties API

**List all properties (paginated)**
```
GET /api/properties/
```

Response: Paginated list of properties (5 per page)

**Get specific page**
```
GET /api/properties/?page=2
```

**Search by location**
```
GET /api/properties/?location=miami
GET /api/properties/?location=florida
```

Searches: city name, state name, location name

**Get single property**
```
GET /api/properties/<property_id>/
```

### Location Autocomplete API

**Get location suggestions**
```
GET /api/location-autocomplete/?q=<query>
```

Parameters:
- `q` - Search query (minimum 2 characters)

Returns: Maximum 5 location suggestions

**Example Request:**
```
GET /api/location-autocomplete/?q=miami
```

**Example Response:**
```json
[
  {
    "id": "LOC001",
    "name": "Beachfront Paradise",
    "city": "Miami Beach",
    "state": "Florida",
    "display": "Miami Beach, Florida",
    "full_display": "Beachfront Paradise - Miami Beach, Florida",
    "property_count": 2
  }
]
```

## Admin Panel

### Access

URL: http://127.0.0.1:8000/admin/

Login with superuser credentials created during setup.

### Features

**Property Management:**
- Inline image management
- Add/edit/delete images directly on property page
- Image preview thumbnails
- Image upload or external URL support
- Set image display order
- Auto-generated image IDs
- View image count per property
- Search and filter properties

**Location Management:**
- Add/edit locations
- Filter by country, state
- Search by name, city

**Image Management:**
- Standalone image administration
- Filter by property
- View image source (uploaded vs external)
- Large image preview
- Search by image ID or caption

### Adding Images to Properties

**Method 1: Upload Image File**

1. Edit a property in admin panel
2. Scroll to "Property images" section
3. Click "Choose File" under "Image file"
4. Select image from computer
5. Fill in caption and order (optional)
6. Click "Save"

Images are stored in `media/property_images/`

**Method 2: Use External URL**

1. Edit a property in admin panel
2. Scroll to "Property images" section
3. Enter URL in "Image url" field
4. Fill in caption and order (optional)
5. Click "Save"

**Image Fields:**
- Image ID: Auto-generated if left blank
- Image file: Upload from computer
- Image url: External image URL
- Image caption: Description (optional)
- Image order: Display order in gallery (1, 2, 3...)

**Note:** If both image file and URL are provided, the uploaded file takes priority.

### Admin Navigation

**From Admin Panel:**
- Click "View Homepage" button (top-right) to return to homepage

**From Homepage:**
- Click "Admin Panel" button (top-right) to access admin
- Click "API" button (top-right) to view API

## Frontend Features

### Homepage

**URL:** http://127.0.0.1:8000/

**Features:**
- Property grid layout (responsive)
- Location search with autocomplete
- AJAX-powered suggestions
- Pagination (5 properties per page)
- Navigation buttons (API, Admin Panel)

**Search Functionality:**
- Type 2+ characters to trigger autocomplete
- Shows 5 location suggestions
- Displays location name with property count
- 300ms debounce to reduce API calls
- Click suggestion to search
- Press Enter to search current text

### Property Detail Page

**URL:** http://127.0.0.1:8000/property/<property_id>/

**Features:**
- Image gallery slider
- Left/Right arrow navigation
- Keyboard arrow key support (← →)
- Indicator dots for current image
- Auto-loops through images
- Property details (type, beds, baths, guests, price)
- Full description
- Location information
- Back to properties link

### Navigation

**Header Links:**
- Homepage logo - Returns to homepage
- API button (blue) - Opens DRF browsable API
- Admin Panel button (green) - Opens Django admin

## Configuration

### Media Files

**Settings** (`config/settings.py`):
```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Storage:** Uploaded images saved to `media/property_images/`

**Access:** Images served at `/media/property_images/<filename>`

**Note:** Media files are tracked in Git for this project.

### Pagination

**Settings** (`config/settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}
```

**Frontend:** Also displays 5 properties per page

### CORS (Development)

**Settings** (`config/settings.py`):
```python
CORS_ALLOW_ALL_ORIGINS = True
```

**Production:** Configure specific allowed origins

### Debug Mode

**Current** (Development):
```python
DEBUG = True
ALLOWED_HOSTS = ['*']
```

**Production:**
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

## CSV Import

### Usage

```bash
python manage.py import_csv <path_to_csv>
```

### CSV Format

Required columns:
- `property_id`, `property_name`, `property_type`, `bedrooms`, `bathrooms`, `max_guests`, `price_per_night`, `property_description`
- `location_id`, `location_name`, `location_city`, `location_state`, `location_country`, `location_zip`, `location_latitude`, `location_longitude`, `location_description`
- `image_ids` (comma-separated)
- `image_urls` (comma-separated)
- `image_captions` (comma-separated)

### Import Process

1. Clears existing data (PropertyImage, Property, Location)
2. Creates Location records
3. Creates Property records
4. Creates PropertyImage records
5. Reports success/errors

### Example CSV Row

```csv
PROP001,Ocean View Villa,Villa,4,3,8,450,"Luxury villa",LOC001,Beachfront Paradise,Miami Beach,Florida,USA,33139,25.7907,-80.1300,"Prime beachfront","IMG001,IMG002","https://url1.jpg,https://url2.jpg","Caption 1,Caption 2"
```

## Troubleshooting

### No Such Table Error

```bash
python manage.py makemigrations rentals
python manage.py migrate
```

### Pillow Not Installed

```bash
pip install Pillow
```

### Port Already in Use

```bash
python manage.py runserver 8001
```

### Images Not Displaying

**Check file upload:**
```bash
ls media/property_images/
```

**Check Django shell:**
```python
python manage.py shell
>>> from rentals.models import PropertyImage
>>> img = PropertyImage.objects.first()
>>> img.image_file.url
'/media/property_images/image.jpg'
```

**Verify media serving:**
Check `config/urls.py` includes:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### CSV Import Fails

- Verify CSV file path
- Check column names match expected format
- Ensure data types are correct
- Check for missing required fields

### Admin Panel Issues

- Clear browser cache
- Check superuser credentials
- Verify migrations are applied
- Check browser console for errors

## Deployment

### Pre-Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure CORS properly
- [ ] Set up static file serving (`collectstatic`)
- [ ] Configure media file serving (S3/CDN recommended)
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure backups
- [ ] Run security checks (`python manage.py check --deploy`)

### Database for Production

**Recommended:** PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### Static Files for Production

```bash
# Install whitenoise for static file serving
pip install whitenoise

# Collect static files
python manage.py collectstatic
```

### Media Files for Production

**Recommended:** Use cloud storage (AWS S3, Google Cloud Storage, Azure)

Install django-storages:
```bash
pip install django-storages boto3
```

Configure in settings:
```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
```

## Technology Stack

- **Backend:** Django 5.0+
- **API:** Django REST Framework 3.14+
- **Database:** SQLite3 (development), PostgreSQL (production recommended)
- **Image Processing:** Pillow 10.0+
- **CORS:** django-cors-headers 4.0+
- **Frontend:** Vanilla JavaScript (no frameworks)
- **Styling:** Pure CSS (no frameworks)
- **Image Storage:** Local filesystem (development), S3/CDN (production recommended)

## Image Credits

Sample images in the CSV are from Unsplash (https://unsplash.com).

**License:** Unsplash License
- Free for commercial and non-commercial use
- No attribution required
- Cannot be sold as-is

**Note:** Images are representative and may not exactly match descriptions.

## Version Control

### Git Configuration

Media files are tracked in this repository for demonstration purposes.

**To commit changes:**
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

**Note:** For production applications, store media files externally (S3, CDN) and add `media/` to `.gitignore`.

## License

This project is for educational and demonstration purposes.

## Support

For issues:
- Check Django documentation: https://docs.djangoproject.com/
- Review DRF documentation: https://www.django-rest-framework.org/
- Consult Pillow documentation: https://pillow.readthedocs.io/

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Pillow (Python Imaging Library): https://pillow.readthedocs.io/
- Git Documentation: https://git-scm.com/doc

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Built with:** Django | REST Framework | Pillow | Vanilla JavaScript