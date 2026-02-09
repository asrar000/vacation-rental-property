from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property, Location
from .serializers import PropertySerializer, LocationSerializer

class PropertyPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all().prefetch_related('images', 'location')
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['property_name', 'property_description', 'location__location_name', 'location__location_city']

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.query_params.get('location', None)
        
        if location:
            # UPDATED: Search by location (city, state, or location name)
            queryset = queryset.filter(
                Q(location__location_city__icontains=location) |
                Q(location__location_state__icontains=location) |
                Q(location__location_name__icontains=location)
            )
        
        return queryset

# UPDATED: Location autocomplete API based on property locations - Returns only 5 suggestions
@api_view(['GET'])
def location_autocomplete(request):
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return Response([])
    
    # Get unique locations that have properties, matching the search query
    locations = Location.objects.filter(
        Q(location_city__icontains=query) |
        Q(location_state__icontains=query) |
        Q(location_name__icontains=query)
    ).distinct()[:5]  # ONLY 5 SUGGESTIONS
    
    suggestions = []
    for loc in locations:
        # Count how many properties are in this location
        property_count = loc.properties.count()
        suggestions.append({
            'id': loc.location_id,
            'name': loc.location_name,
            'city': loc.location_city,
            'state': loc.location_state,
            'display': f"{loc.location_city}, {loc.location_state}",
            'full_display': f"{loc.location_name} - {loc.location_city}, {loc.location_state}",
            'property_count': property_count
        })
    
    return Response(suggestions)

def home(request):
    return render(request, 'rentals/home.html')

def property_detail(request, property_id):
    from django.shortcuts import get_object_or_404
    property_obj = get_object_or_404(Property, property_id=property_id)
    return render(request, 'rentals/property_detail.html', {'property': property_obj})