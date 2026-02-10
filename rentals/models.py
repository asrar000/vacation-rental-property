from django.db import models

class Location(models.Model):
    location_id = models.CharField(max_length=20, unique=True, primary_key=True)
    location_name = models.CharField(max_length=200)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_country = models.CharField(max_length=100)
    location_zip = models.CharField(max_length=20)
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_description = models.TextField()

    def __str__(self):
        return f"{self.location_name} - {self.location_city}, {self.location_state}"

    class Meta:
        ordering = ['location_name']


class Property(models.Model):
    PROPERTY_TYPES = [
        ('Villa', 'Villa'),
        ('Condo', 'Condo'),
        ('Chalet', 'Chalet'),
        ('Cabin', 'Cabin'),
        ('Loft', 'Loft'),
        ('Penthouse', 'Penthouse'),
        ('House', 'House'),
        ('Townhouse', 'Townhouse'),
        ('Suite', 'Suite'),
    ]

    property_id = models.CharField(max_length=20, unique=True, primary_key=True)
    property_name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    max_guests = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    property_description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property_name} - {self.property_type}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'


class PropertyImage(models.Model):
    image_id = models.CharField(max_length=20, unique=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    
    # UPDATED: Added ImageField for file uploads
    image_file = models.ImageField(upload_to='property_images/', blank=True, null=True, 
                                    help_text="Upload an image file")
    
    # Keep URL field for external images
    image_url = models.URLField(max_length=500, blank=True, null=True,
                                 help_text="Or provide an external image URL")
    
    image_caption = models.CharField(max_length=300, blank=True)
    image_order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.image_id} - {self.property.property_name}"

    class Meta:
        ordering = ['image_order', 'image_id']
    
    # UPDATED: Method to get the image URL (uploaded or external)
    def get_image_url(self):
        """Returns the image URL - either from uploaded file or external URL"""
        if self.image_file:
            return self.image_file.url
        return self.image_url or ''
    
    def save(self, *args, **kwargs):
        """Auto-generate image_id if not provided"""
        if not self.image_id:
            # Generate a unique image_id
            import uuid
            self.image_id = f"IMG{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)