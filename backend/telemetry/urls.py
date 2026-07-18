from django.urls import path
from .views import DeviceListView, DeviceReadingsView

urlpatterns = [
    path("devices/", DeviceListView.as_view(), name="device-list"),
    path("devices/<int:device_id>/readings", DeviceReadingsView.as_view(), name="device-readings")
]