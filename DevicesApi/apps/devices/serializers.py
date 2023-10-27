from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import DeviceType, Device
from .validators import SerialNumValidator


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        validators = [
            SerialNumValidator(),
            UniqueTogetherValidator(
                queryset=Device.objects.all(),
                fields=['type_id', 'serial_num'],
                message="Серийный номер для этого типа устойств не уникален"
            )
        ]
        fields = ["id", "type_id", "serial_num", "note"]
