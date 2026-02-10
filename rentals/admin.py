from django.contrib import admin
from django.utils.html import format_html
from .models import Location, Property, PropertyImage

# UPDATED: PropertyImage inline with image preview
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image_preview', 'image_id', 'image_file', 'image_url', 'image_caption', 'image_order')
    readonly_fields = ('image_preview',)
    ordering = ['image_order']
    
    # UPDATED: Display image preview in admin
    def image_preview(self, obj):
        """Display thumbnail preview of the image"""
        if obj.image_file:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', 
                             obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', 
                             obj.image_url)
        return "No image"
    
    image_preview.short_description = 'Preview'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'location_name', 'location_city', 'location_state', 'location_country')
    search_fields = ('location_name', 'location_city', 'location_state')
    list_filter = ('location_country', 'location_state')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'property_name', 'property_type', 'bedrooms', 'bathrooms', 
                    'price_per_night', 'location', 'image_count')
    search_fields = ('property_name', 'property_description', 'location__location_name')
    list_filter = ('property_type', 'bedrooms', 'location__location_city')
    inlines = [PropertyImageInline]  # Inline model relation
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('property_id', 'property_name', 'property_type')
        }),
        ('Details', {
            'fields': ('bedrooms', 'bathrooms', 'max_guests', 'price_per_night', 'property_description')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # UPDATED: Show image count in property list
    def image_count(self, obj):
        count = obj.images.count()
        return f"{count} image{'s' if count != 1 else ''}"
    
    image_count.short_description = 'Images'


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'property', 'image_thumbnail', 'image_caption', 'image_order', 'image_source')
    list_filter = ('property',)
    search_fields = ('image_id', 'image_caption', 'property__property_name')
    ordering = ['property', 'image_order']
    
    fields = ('image_id', 'property', 'image_file', 'image_url', 'image_caption', 
              'image_order', 'image_preview')
    readonly_fields = ('image_preview',)
    
    # UPDATED: Display thumbnail in list view
    def image_thumbnail(self, obj):
        """Display small thumbnail in admin list"""
        if obj.image_file:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 75px;" />', 
                             obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 75px;" />', 
                             obj.image_url)
        return "No image"
    
    image_thumbnail.short_description = 'Thumbnail'
    
    # UPDATED: Display larger preview in detail view
    def image_preview(self, obj):
        """Display larger preview in the detail/edit form"""
        if obj.image_file:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 400px;" />', 
                             obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 400px;" />', 
                             obj.image_url)
        return "No image uploaded or URL provided"
    
    image_preview.short_description = 'Image Preview'
    
    # UPDATED: Show whether image is uploaded or from URL
    def image_source(self, obj):
        """Display the source of the image"""
        if obj.image_file:
            return "Uploaded File"
        elif obj.image_url:
            return "External URL"
        return "No Image"
    
    image_source.short_description = 'Source'