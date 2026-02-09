from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet, basename='property')

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<str:property_id>/', views.property_detail, name='property_detail'),
    path('api/', include(router.urls)),
    # NEW: Property name autocomplete endpoint
    path('api/property-autocomplete/', views.property_autocomplete, name='property_autocomplete'),
]