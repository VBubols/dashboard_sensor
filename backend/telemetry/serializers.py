from rest_framework import serializers
from .models import Device, Sensor, Reading

class DeviceSerializer(serializers.ModelSerializer):
    current_state = serializers.SerializerMethodField()
    
    class Meta:
        model = Device
        fields = ["id", "dev_eui", "name", "profile_name", "current_state"]

    def get_current_state(self, device):
        sensors = device.sensors.all()
        result = []

        for sensor in sensors:
            latest = sensor.readings.first()
            if latest:
                result.append({
                    "metric_key": sensor.metric_key,
                    "metric_type": sensor.metric_type,
                    "label": sensor.label,
                    "unit": sensor.unit,
                    "value": latest.value,
                    "timestamp": latest.timestamp
                })
        return result

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "metric_key", "metric_type"]

class ReadingSerializer(serializers.ModelSerializer):
    metric_key = serializers.CharField(source="sensor.metric_key")
    metric_type = serializers.CharField(source="sensor.metric_type")
    label = serializers.CharField(source="sensor.label")
    unit = serializers.CharField(source="sensor.unit")

    class Meta:
        model = Reading
        fields = ["id", "metric_key", "metric_type", "label", "unit", "value", "timestamp"]