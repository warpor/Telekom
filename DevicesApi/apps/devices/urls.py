from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import DeviceViewSet, DeviceTypeViewSet, api_root

router = DefaultRouter()
router.register(r'equipment', DeviceViewSet, basename="equipment")
router.register(r'equipment-type', DeviceTypeViewSet, basename="equipment-type")

urlpatterns = [
    path('', include(router.urls)),
]
