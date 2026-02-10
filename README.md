# Vacation Rental Django Project

A Django web application for managing vacation rental properties with location-based search, autocomplete, and admin panel features.

## Features

- Property listing with pagination (5 properties per page)
- Location-based search with AJAX autocomplete (shows 5 suggestions)
- Admin panel with inline image management
- Image gallery slider for each property
- RESTful API with Django REST Framework
- Media root configuration for file uploads
- Simple, clean frontend design

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Installation

1. **Extract/Clone the Project:**
   ```bash
   cd vacation_rental
   ```

2. **Activate Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies (if not already installed):**
   ```bash
   pip install django djangorestframework django-cors-headers pillow
   ```

## Running the Project

1. **Create Migrations (first time only):**
   ```bash
   python manage.py makemigrations
   ```

2. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   Enter username, email, and password when prompted.

4. **Import CSV Data:**
   ```bash
   python manage.py import_csv path/to/vacation_rental_data.csv
   ```
   Example:
   ```bash
   python manage.py import_csv ../vacation_rental_data.csv
   ```

5. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**
   - Homepage: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/properties/

## Project Structure

```
vacation_rental/
├── config/                     # Project settings
│   ├── settings.py            # Main settings (MEDIA_ROOT configured)
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
├── media/                      # User uploaded files (MEDIA_ROOT)
├── staticfiles/                # Static files
├── venv/                       # Virtual environment
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
└── README.md                   # This file
```

## Models

### Location
- `location_id` (Primary Key)
- `location_name`
- `location_city`
- `location_state`
- `location_country`
- `location_zip`
- `location_latitude`
- `location_longitude`
- `location_description`

### Property
- `property_id` (Primary Key)
- `property_name`
- `property_type` (Villa, Condo, Chalet, etc.)
- `bedrooms`
- `bathrooms`
- `max_guests`
- `price_per_night`
- `property_description`
- `location` (Foreign Key to Location)
- `created_at`
- `updated_at`

**Relationship:** One Location can have many Properties

### PropertyImage
- `image_id` (Unique)
- `property` (Foreign Key to Property)
- `image_url`
- `image_caption`
- `image_order`

**Relationship:** One Property can have many PropertyImages

## API Endpoints

### Properties
- `GET /api/properties/` - List all properties (paginated, 5 per page)
- `GET /api/properties/?page=2` - Get specific page
- `GET /api/properties/?location=<query>` - Search properties by location
- `GET /api/properties/<property_id>/` - Get single property details

### Autocomplete
- `GET /api/location-autocomplete/?q=<query>` - Get location suggestions (max 5)
  - Searches: city, state, location name
  - Returns: location details with property count

**Example:**
```
GET /api/location-autocomplete/?q=miami

Response:
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

## Admin Features

### Admin Panel (`/admin/`)

**Property Management:**
- Inline image management (add/edit/delete images on property page)
- Add multiple images per property
- Set image order for gallery display
- Search by property name, location
- Filter by property type, bedrooms, city
- View created/updated timestamps

**Location Management:**
- View all locations
- Filter by country, state
- Search by name, city

**Image Management:**
- Standalone image management
- Filter by property
- Search by image ID or caption

### Inline Model Features
The admin uses Django's `TabularInline` for PropertyImages:
- Add images directly on the property edit page
- Set image order for gallery display
- Edit image URLs and captions inline
- Delete images without leaving the property page

## Frontend Features

### Homepage
- Display all properties in a grid layout
- Location-based search with autocomplete
- AJAX-powered autocomplete (5 suggestions)
- Pagination (5 properties per page)
- Click on property to view details

### Property Detail Page
- Image gallery with slider
- Left/Right arrow navigation
- Keyboard arrow key support
- Indicator dots for current image
- Property details (beds, baths, price, etc.)
- Location information
- Back to properties link

### Autocomplete Functionality
- Triggers after typing 2+ characters
- 300ms debounce to reduce API calls
- Shows location name with property count
- Click to auto-fill and search
- Closes when clicking outside

## Configuration

### MEDIA_ROOT (User Uploads)
```python
# config/settings.py
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
Files uploaded through admin will be stored in the `media/` directory.

### Pagination Settings
```python
# config/settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}
```

### CORS Configuration
```python
# config/settings.py
CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

## CSV Import Command

The project includes a custom management command to import property data from CSV.

**Usage:**
```bash
python manage.py import_csv <path_to_csv_file>
```

**CSV Format:**
The CSV should have the following columns:
- property_id, property_name, property_type, bedrooms, bathrooms, max_guests, price_per_night, property_description
- location_id, location_name, location_city, location_state, location_country, location_zip, location_latitude, location_longitude, location_description
- image_ids (comma-separated), image_urls (comma-separated), image_captions (comma-separated)

**What it does:**
1. Clears existing data (PropertyImage, Property, Location)
2. Creates Location records
3. Creates Property records linked to locations
4. Creates PropertyImage records for each property
5. Reports success/failure for each operation

## Image Credits

All images used in the sample data are from Unsplash (https://unsplash.com), a free stock photo platform.

**License:** Unsplash License (Free to use)
- No attribution required
- Free for commercial and non-commercial use
- Images are representative and may not match exact property descriptions

## Technology Stack

- **Backend:** Django 6.0+
- **API:** Django REST Framework
- **Database:** SQLite3 (development)
- **Frontend:** Vanilla JavaScript (no frameworks)
- **Styling:** Pure CSS (no frameworks)
- **Image Hosting:** External URLs (Unsplash)

## Development Notes

### Debug Mode
The project runs in DEBUG mode by default. For production:
```python
# config/settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

### Secret Key
Change the secret key in production:
```python
# config/settings.py
SECRET_KEY = 'your-production-secret-key'
```

### Database
For production, consider using PostgreSQL:
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

## Troubleshooting

### "no such table" error
```bash
python manage.py makemigrations rentals
python manage.py migrate
```

### Port already in use
```bash
python manage.py runserver 8001
```

### CSV import fails
- Check CSV file path
- Ensure CSV has correct column names
- Verify data format matches expected types

### Images not displaying
- Check image URLs are accessible
- Verify MEDIA_URL is configured
- Check browser console for errors

## License

This project is for educational/demonstration purposes.

## Support

For issues or questions, please check:
1. Django documentation: https://docs.djangoproject.com/
2. DRF documentation: https://www.django-rest-framework.org/
3. Project structure and code comments