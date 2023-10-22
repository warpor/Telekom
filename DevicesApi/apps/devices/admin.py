from django.contrib import admin

from .models import DeviceType, Device

# Register your models here.
admin.site.register(DeviceType)
admin.site.register(Device)
