from django.contrib import admin
from .models import Location, Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image_id', 'image_url', 'image_caption', 'image_order')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'location_name', 'location_city', 'location_state', 'location_country')
    search_fields = ('location_name', 'location_city', 'location_state')
    list_filter = ('location_country', 'location_state')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'property_name', 'property_type', 'bedrooms', 'bathrooms', 'price_per_night', 'location')
    search_fields = ('property_name', 'property_description', 'location__location_name')
    list_filter = ('property_type', 'bedrooms', 'location__location_city')
    inlines = [PropertyImageInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'property', 'image_caption', 'image_order')
    list_filter = ('property',)
    search_fields = ('image_id', 'image_caption', 'property__property_name')
