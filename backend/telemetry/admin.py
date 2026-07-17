from django.contrib import admin
from .models import Device, Sensor, Reading

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "dev_eui", "profile_name")

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("device", "metric_key", "metric_type")

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ("sensor", "value", "timestamp")