from rest_framework.generics import ListAPIView
from .models import Device, Reading
from .serializers import DeviceSerializer, ReadingSerializer

class DeviceListView(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceReadingsView(ListAPIView):
    serializer_class = ReadingSerializer

    def get_queryset(self):
        device_id = self.kwargs["device_id"]
        return Reading.objects.filter(sensor__device_id=device_id)