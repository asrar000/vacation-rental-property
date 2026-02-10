from rest_framework import serializers
from .models import Location, Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    # UPDATED: Use SerializerMethodField to get the correct image URL
    display_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyImage
        fields = ['image_id', 'display_url', 'image_caption', 'image_order']
    
    def get_display_url(self, obj):
        """Return the image URL - either from uploaded file or external URL"""
        request = self.context.get('request')
        
        # If image_file exists (uploaded file)
        if obj.image_file:
            if request is not None:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        
        # Otherwise return external URL
        return obj.image_url or ''


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True, context={'request': None})
    location_name = serializers.CharField(source='location.location_name', read_only=True)
    location_city = serializers.CharField(source='location.location_city', read_only=True)

    class Meta:
        model = Property
        fields = ['property_id', 'property_name', 'property_type', 'bedrooms', 
                  'bathrooms', 'max_guests', 'price_per_night', 'property_description',
                  'location', 'location_name', 'location_city', 'images', 'created_at']