from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import EquipmentType, Equipment
from .serializers import DeviceTypeSerializer, DeviceSerializer
from .service import multiple_objects_add


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'equipment': reverse('equipment', request=request, format=format),
        'equipment-type': reverse('equipment-type', request=request, format=format)
    })


class EquipmentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = DeviceTypeSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter]
    filterset_fields = ['id', "type_id", "serial_num", "note"]
    search_fields = ['note', 'serial_num']

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Производит мягкое удаление объекта

        Возвращаемое значение
        ---------------------
        Response: Получилось ли удалить объект, если нет, то вернуть,
         что объект не найден
        """

        try:
            self.get_object().soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Если в запросе массив - пытается добавить массив объектов.
        Если в запросе один объект - пытается добавить один объект.

        Параметры
        ---------
        request (Request): POST запрос, который может
        содержать как один JSON, так и массив JSON-ов

        Возвращаемое значение
        ---------------------
        Response: Получилось ли создать запись, если нет, то вернуть ошибки
        """

        is_many = isinstance(request.data, list)
        if not is_many:
            return super(EquipmentViewSet, self).create(request, *args, **kwargs)
        else:
            return multiple_objects_add(self, request)
