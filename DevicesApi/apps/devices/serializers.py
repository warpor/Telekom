from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import EquipmentType, Equipment
from .validators import SerialNumValidator


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        validators = [
            SerialNumValidator(),
            UniqueTogetherValidator(
                queryset=Equipment.objects.all(),
                fields=['type_id', 'serial_num'],
                message="Серийный номер для этого типа устойств не уникален"
            )
        ]
        fields = ["id", "type_id", "serial_num", "note"]
