from django.db import models

from models_manager import SoftDeleteModel


class DeviceType(models.Model):
    type_name = models.CharField()
    serial_num_mask = models.CharField()


class Device(SoftDeleteModel):
    type_id = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    serial_num = models.CharField()
    note = models.TextField()
