# Vacation Rental Django Project

A Django web application for managing vacation rental properties with location-based search, AJAX autocomplete, image uploads, and admin panel features.

## 🌟 Features

- **Property Listing** with pagination (5 properties per page)
- **Location-based Search** with AJAX autocomplete (shows 5 suggestions)
- **Image Upload & Management** - Upload images directly or use external URLs
- **Image Gallery** with slider for each property (left/right navigation + keyboard support)
- **Admin Panel** with inline image management and preview
- **RESTful API** with Django REST Framework
- **Media Storage** configured for file uploads
- **Simple, Clean Frontend** - No frameworks, vanilla JavaScript

## 📋 Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## 🚀 Installation & Setup

### 1. Clone or Extract the Project

```bash
cd vacation_rental
```

### 2. Create and Activate Virtual Environment

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

This will install:
- Django (>=5.0)
- Django REST Framework
- django-cors-headers
- Pillow (for image processing)

### 4. Run Migrations

```bash
# Create migrations
python manage.py makemigrations rentals

# Apply migrations to database
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### 6. Import CSV Data (Optional)

```bash
# If you have the vacation_rental_data.csv file
python manage.py import_csv path/to/vacation_rental_data.csv

# Example:
python manage.py import_csv ../vacation_rental_data.csv
```

### 7. Run Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/properties/

## 📁 Project Structure

```
vacation_rental/
├── config/                     # Project settings
│   ├── settings.py            # Main settings (MEDIA_ROOT, REST_FRAMEWORK)
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py
├── rentals/                    # Main app
│   ├── management/
│   │   └── commands/
│   │       └── import_csv.py  # CSV import management command
│   ├── templates/
│   │   └── rentals/
│   │       ├── base.html      # Base template
│   │       ├── home.html      # Homepage with search/autocomplete
│   │       └── property_detail.html  # Property detail with gallery
│   ├── models.py              # Location, Property, PropertyImage models
│   ├── views.py               # Views and API endpoints
│   ├── serializers.py         # DRF serializers
│   ├── admin.py               # Admin with inline image management
│   └── urls.py                # App URL configuration
├── media/                      # User uploaded images (auto-created)
│   └── property_images/       # Property images storage
├── staticfiles/                # Static files (auto-created)
├── venv/                       # Virtual environment
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
└── README.md                   # This file
```

## 🗄️ Database Models

### Location Model
```python
- location_id (Primary Key, CharField)
- location_name (CharField)
- location_city (CharField)
- location_state (CharField)
- location_country (CharField)
- location_zip (CharField)
- location_latitude (DecimalField)
- location_longitude (DecimalField)
- location_description (TextField)
```

### Property Model
```python
- property_id (Primary Key, CharField)
- property_name (CharField)
- property_type (CharField - choices)
- bedrooms (IntegerField)
- bathrooms (DecimalField)
- max_guests (IntegerField)
- price_per_night (DecimalField)
- property_description (TextField)
- location (ForeignKey to Location)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

**Property Types:** Villa, Condo, Chalet, Cabin, Loft, Penthouse, House, Townhouse, Suite

**Relationship:** One Location can have many Properties

### PropertyImage Model
```python
- image_id (CharField, Unique)
- property (ForeignKey to Property)
- image_file (ImageField) - For uploaded images
- image_url (URLField) - For external image URLs
- image_caption (CharField)
- image_order (IntegerField)
```

**Relationship:** One Property can have many PropertyImages

**Image Storage:** 
- Uploaded images: `media/property_images/`
- Priority: If both `image_file` and `image_url` exist, uploaded file is used

## 🔌 API Endpoints

### Properties API

**List all properties (paginated)**
```
GET /api/properties/
GET /api/properties/?page=2
```

**Search by location**
```
GET /api/properties/?location=miami
GET /api/properties/?location=florida
```

**Get single property**
```
GET /api/properties/<property_id>/
```

### Autocomplete API

**Location autocomplete (max 5 suggestions)**
```
GET /api/location-autocomplete/?q=miami
```

**Response Example:**
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

**Searches:** City name, State name, Location name

## 🎨 Admin Panel Features

### Access Admin Panel
```
URL: http://127.0.0.1:8000/admin/
Login: Use the superuser credentials you created
```

### Property Management
- ✅ **Inline Image Management** - Add/edit images directly on property page
- ✅ **Image Upload** - Upload images from your computer
- ✅ **External URLs** - Or use external image URLs
- ✅ **Image Preview** - See thumbnails and full previews
- ✅ **Image Ordering** - Set display order for gallery
- ✅ **Auto Image ID** - Automatically generates unique IDs
- ✅ **Image Count** - Shows number of images per property
- ✅ **Bulk Operations** - Edit multiple properties at once
- ✅ **Search & Filter** - Find properties quickly

### Adding Images to Properties

**Option 1: Upload Image File**
1. Edit a property in admin
2. Scroll to "Property images" section
3. Click "Choose File" under "Image file"
4. Select image from your computer
5. Set image caption and order
6. Save

**Option 2: Use External URL**
1. Edit a property in admin
2. Scroll to "Property images" section
3. Enter URL in "Image url" field
4. Set image caption and order
5. Save

**Priority:** If both file and URL are provided, uploaded file takes priority.

### Image Features in Admin
- **Thumbnail Preview** - Small preview in property list
- **Large Preview** - Full preview in edit form
- **Image Source Label** - Shows "Uploaded File" or "External URL"
- **Inline Editing** - Edit images without leaving property page
- **Tabular Display** - Clean, organized layout

## 🖼️ Frontend Features

### Homepage (`/`)
- **Property Grid** - Responsive grid layout
- **Location Search** - Search bar with autocomplete
- **AJAX Autocomplete** - Live suggestions as you type
  - Triggers after 2+ characters
  - Shows 5 suggestions max
  - 300ms debounce
  - Shows location with property count
- **Pagination** - 5 properties per page
- **Click to View** - Click any property card for details

### Property Detail Page (`/property/<id>/`)
- **Image Gallery Slider**
  - One image displayed at a time
  - Left/Right arrow buttons
  - Keyboard navigation (← →)
  - Indicator dots
  - Auto-loops through images
- **Property Information**
  - Type, bedrooms, bathrooms
  - Max guests, price per night
  - Full description
- **Location Details**
  - Location name, address
  - City, state, country, zip
  - Location description
- **Back Button** - Return to property list

### Search & Autocomplete
- **What you can search:** City names, State names, Location names
- **Examples:** "Miami", "Florida", "Beachfront Paradise"
- **How it works:**
  1. Type 2+ characters
  2. Wait 300ms (debounce)
  3. API returns 5 suggestions
  4. Click suggestion to search
  5. Press Enter to search current text

## ⚙️ Configuration

### Media Files (Uploaded Images)

```python
# config/settings.py
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Storage Location:** `media/property_images/`

**Access:** Uploaded images are served at `/media/property_images/filename.jpg`

### Pagination

```python
# config/settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,  # 5 items per page
}
```

### CORS (Development)

```python
# config/settings.py
CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

**Production:** Set specific allowed origins

## 📊 CSV Import Command

### Usage

```bash
python manage.py import_csv <path_to_csv_file>
```

### CSV Format Required

The CSV must have these columns:
- `property_id`, `property_name`, `property_type`, `bedrooms`, `bathrooms`, `max_guests`, `price_per_night`, `property_description`
- `location_id`, `location_name`, `location_city`, `location_state`, `location_country`, `location_zip`, `location_latitude`, `location_longitude`, `location_description`
- `image_ids` (comma-separated), `image_urls` (comma-separated), `image_captions` (comma-separated)

### What It Does

1. ✅ Clears existing data (PropertyImage, Property, Location)
2. ✅ Creates Location records
3. ✅ Creates Property records with location links
4. ✅ Creates PropertyImage records for each property
5. ✅ Reports success/errors for each operation

### Example CSV Row

```csv
PROP001,Ocean View Villa,Villa,4,3,8,450,"Luxury villa...",LOC001,Beachfront Paradise,Miami Beach,Florida,USA,33139,25.7907,-80.1300,"Prime beachfront...","IMG001,IMG002,IMG003","https://...,https://...,https://...","Caption 1,Caption 2,Caption 3"
```

## 🛠️ Technology Stack

- **Backend Framework:** Django 5.0+
- **API Framework:** Django REST Framework
- **Database:** SQLite3 (development)
- **Image Processing:** Pillow
- **Frontend:** Vanilla JavaScript (no frameworks)
- **Styling:** Pure CSS (no frameworks)
- **Image Hosting:** Upload + External URLs supported

## 🔒 Security Notes

### Development vs Production

**Current Settings (Development):**
```python
DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'django-insecure-...'
CORS_ALLOW_ALL_ORIGINS = True
```

**Production Settings (Required):**
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']
```

### Database for Production

**Current:** SQLite3 (development only)

**Recommended for Production:** PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files for Production

```bash
# Collect static files
python manage.py collectstatic

# Serve with nginx or whitenoise
pip install whitenoise
```

## 🐛 Troubleshooting

### "no such table" error

```bash
python manage.py makemigrations rentals
python manage.py migrate
```

### Pillow not installed

```bash
pip install Pillow
```

### Port already in use

```bash
# Use different port
python manage.py runserver 8001
```

### CSV import fails

- ✅ Check CSV file path is correct
- ✅ Ensure CSV has correct column names
- ✅ Verify data types match model fields
- ✅ Check for empty required fields

### Images not displaying

- ✅ Check `MEDIA_URL` and `MEDIA_ROOT` in settings
- ✅ Verify image URLs are accessible
- ✅ Check browser console for errors
- ✅ Ensure uploaded images are in `media/property_images/`

### Admin panel not loading images

- ✅ Make sure Pillow is installed
- ✅ Check media files are being served in development
- ✅ Verify `urls.py` includes media URL patterns

## 📷 Image Credits

All sample images in the provided CSV are from [Unsplash](https://unsplash.com), a free stock photo platform.

**License:** Unsplash License
- ✅ Free to use for commercial and non-commercial purposes
- ✅ No attribution required (but appreciated)
- ✅ Cannot be sold as-is or in a wallpaper collection

**Note:** Images are representative stock photos and may not exactly match property descriptions.

## 📝 Development Workflow

### Adding New Properties

1. Go to admin panel
2. Click "Properties" → "Add Property"
3. Fill in property details
4. Add location
5. Add images (upload or URL)
6. Set image order
7. Save

### Updating Properties

1. Edit property in admin
2. Modify fields as needed
3. Add/remove/reorder images inline
4. Save changes

### Managing Locations

1. Add locations before properties
2. One location can have multiple properties
3. Edit location details in admin

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure CORS properly
- [ ] Set up static file serving
- [ ] Set up media file serving
- [ ] Enable HTTPS
- [ ] Configure backup strategy
- [ ] Set up monitoring/logging
- [ ] Test all functionality

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Pillow Documentation](https://pillow.readthedocs.io/)

## 📄 License

This project is for educational/demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to use and modify as needed.

## 📧 Support

For Django-specific issues:
- Check Django documentation
- Review error messages carefully
- Ensure all migrations are applied
- Verify dependencies are installed

---

**Built with Django • REST Framework • Pillow • Vanilla JavaScript**