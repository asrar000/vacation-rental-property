import csv
from django.core.management.base import BaseCommand
from rentals.models import Location, Property, PropertyImage

class Command(BaseCommand):
    help = 'Import vacation rental data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        PropertyImage.objects.all().delete()
        Property.objects.all().delete()
        Location.objects.all().delete()
        
        locations = {}
        properties = {}
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Create or get location
                location_id = row['location_id']
                if location_id not in locations:
                    location = Location.objects.create(
                        location_id=location_id,
                        location_name=row['location_name'],
                        location_city=row['location_city'],
                        location_state=row['location_state'],
                        location_country=row['location_country'],
                        location_zip=row['location_zip'],
                        location_latitude=row['location_latitude'],
                        location_longitude=row['location_longitude'],
                        location_description=row['location_description']
                    )
                    locations[location_id] = location
                    self.stdout.write(self.style.SUCCESS(f'Created location: {location.location_name}'))
                
                # Create or get property
                property_id = row['property_id']
                if property_id not in properties:
                    property_obj = Property.objects.create(
                        property_id=property_id,
                        property_name=row['property_name'],
                        property_type=row['property_type'],
                        bedrooms=int(row['bedrooms']),
                        bathrooms=float(row['bathrooms']),
                        max_guests=int(row['max_guests']),
                        price_per_night=float(row['price_per_night']),
                        property_description=row['property_description'],
                        location=locations[location_id]
                    )
                    properties[property_id] = property_obj
                    self.stdout.write(self.style.SUCCESS(f'Created property: {property_obj.property_name}'))
                    
                    # Create images for this property
                    image_ids = row['image_ids'].split(',')
                    image_urls = row['image_urls'].split(',')
                    image_captions = row['image_captions'].split(',')
                    
                    for i, (img_id, img_url, img_caption) in enumerate(zip(image_ids, image_urls, image_captions)):
                        PropertyImage.objects.create(
                            image_id=img_id.strip(),
                            property=property_obj,
                            image_url=img_url.strip(),
                            image_caption=img_caption.strip(),
                            image_order=i + 1
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'  Created {len(image_ids)} images for {property_obj.property_name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nImport completed!'))
        self.stdout.write(self.style.SUCCESS(f'Total Locations: {Location.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total Properties: {Property.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total Images: {PropertyImage.objects.count()}'))
