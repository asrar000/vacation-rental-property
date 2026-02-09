from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property, Location
from .serializers import PropertySerializer, LocationSerializer

# UPDATED: 5 items per page (changed from 6)
class PropertyPagination(PageNumberPagination):
    page_size = 5  # CHANGED FROM 6 TO 5
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
        search = self.request.query_params.get('search', None)
        
        if search:
            # UPDATED: Search only by property name
            queryset = queryset.filter(
                Q(property_name__icontains=search)
            )
        
        return queryset

# NEW: Property name autocomplete API - Returns only 5 suggestions
@api_view(['GET'])
def property_autocomplete(request):
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return Response([])
    
    # Search only by property name and limit to 5 results
    properties = Property.objects.filter(
        property_name__icontains=query
    ).distinct()[:5]  # ONLY 5 SUGGESTIONS
    
    suggestions = []
    for prop in properties:
        suggestions.append({
            'id': prop.property_id,
            'name': prop.property_name,
            'type': prop.property_type,
            'location': f"{prop.location.location_city}, {prop.location.location_state}"
        })
    
    return Response(suggestions)

def home(request):
    return render(request, 'rentals/home.html')

def property_detail(request, property_id):
    from django.shortcuts import get_object_or_404
    property_obj = get_object_or_404(Property, property_id=property_id)
    return render(request, 'rentals/property_detail.html', {'property': property_obj})