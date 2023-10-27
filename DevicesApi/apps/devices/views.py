from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import DeviceType, Device
from .serializers import DeviceTypeSerializer, DeviceSerializer
from .service import multiple_objects_add


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'equipment': reverse('equipment', request=request, format=format),
        'equipment-type': reverse('equipment-type', request=request, format=format)
    })


class DeviceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter]
    filterset_fields = ['id', "type_id", "serial_num", "note"]
    search_fields = ['note', 'serial_num']

    def destroy(self, request, *args, **kwargs):
        """
        Производит мягкое удаление объекта
        """

        try:
            self.get_object().soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request, *args, **kwargs):
        """
        Если в запросе массив - пытается добавить массив объектов.
        Если в запросе один объект - пытается добавить один объект.
        """

        is_many = isinstance(request.data, list)
        if not is_many:
            return super(DeviceViewSet, self).create(request, *args, **kwargs)
        else:
            return multiple_objects_add(self, request)
