from django.db import models

from .models_manager import SoftDeleteModel


class EquipmentType(models.Model):
    type_name = models.TextField()
    serial_num_mask = models.TextField()


class Equipment(SoftDeleteModel):
    type_id = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    serial_num = models.TextField()
    note = models.TextField()
