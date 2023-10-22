from django.db import models

from .models_manager import SoftDeleteModel


class DeviceType(models.Model):
    type_name = models.TextField()
    serial_num_mask = models.TextField()


class Device(SoftDeleteModel):
    type_id = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    serial_num = models.TextField()
    note = models.TextField()
