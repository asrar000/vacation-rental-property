# Vacation Rental Django Project

A Django web application for managing vacation rental properties with search, autocomplete, and admin panel features.

## Features

- Property listing with pagination
- Location-based search with autocomplete (AJAX)
- Admin panel with inline image management
- Image gallery with slider for each property
- RESTful API with Django REST Framework
- Simple, clean frontend design

## Setup Instructions

This project was created using the automated setup script. All dependencies and configurations are already in place.

## Running the Project

1. **Activate Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Import CSV Data:**
   ```bash
   python manage.py import_csv path/to/vacation_rental_data.csv
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
├── config/                 # Project settings
├── rentals/                # Main app
│   ├── management/
│   │   └── commands/
│   │       └── import_csv.py
│   ├── templates/
│   │   └── rentals/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── admin.py
│   └── urls.py
├── media/                  # User uploaded files
├── staticfiles/            # Static files
├── db.sqlite3              # Database
└── manage.py
```

## Models

- **Location**: Stores location information
- **Property**: Stores property details with foreign key to Location
- **PropertyImage**: Stores multiple images for each property

## API Endpoints

- `GET /api/properties/` - List all properties (paginated)
- `GET /api/properties/?location=<query>` - Search properties by location
- `GET /api/autocomplete/?q=<query>` - Get location suggestions

## Admin Features

- Inline image management for properties
- Bulk operations
- Search and filter capabilities

## Image Credits

All images used in the sample data are from Unsplash (https://unsplash.com), a free stock photo platform.

