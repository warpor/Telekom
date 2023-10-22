from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import DeviceType, Device
from .serializers import DeviceTypeSerializer, DeviceSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'equipment': reverse('equipment', request=request, format=format),
        'equipment-type': reverse('equipment-type', request=request, format=format)
    })


class DeviceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
