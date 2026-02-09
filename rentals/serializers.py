from rest_framework import serializers
from .models import Location, Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image_id', 'image_url', 'image_caption', 'image_order']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    location_name = serializers.CharField(source='location.location_name', read_only=True)
    location_city = serializers.CharField(source='location.location_city', read_only=True)

    class Meta:
        model = Property
        fields = ['property_id', 'property_name', 'property_type', 'bedrooms', 
                  'bathrooms', 'max_guests', 'price_per_night', 'property_description',
                  'location', 'location_name', 'location_city', 'images', 'created_at']
