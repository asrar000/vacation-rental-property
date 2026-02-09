from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet, basename='property')

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<str:property_id>/', views.property_detail, name='property_detail'),
    path('api/', include(router.urls)),
    # UPDATED: Location autocomplete endpoint (changed from property-autocomplete)
    path('api/location-autocomplete/', views.location_autocomplete, name='location_autocomplete'),
]