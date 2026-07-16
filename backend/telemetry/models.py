from django.db import models

class Device(models.Model):
    dev_eui = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)
    profile_id = models.CharField(max_length=64)
    profile_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Sensor(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="sensors")
    metric_key = models.CharField(max_length=64)
    metric_type = models.CharField(max_length=32)

    class Meta:
        unique_together = ("device", "metric_key")

    def __str__(self):
        return f"{self.device.name} / {self.metric_key}"
    
class Reading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="readings")
    timestamp = models.DateTimeField()
    value = models.FloatField()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sensor} = {self.value} @ {self.timestamp}"