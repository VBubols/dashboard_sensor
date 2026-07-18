import os
import time

from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt


class MqttSubscriber:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._topic = "application/+/device/+/event/up"
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def connect(self, retries: int = 30, delay: float = 2.0) -> None:
        for attempt in range(1, retries + 1):
            try:
                self._client.connect(self._host, self._port)
                break
            except OSError:
                if attempt == retries:
                    raise
                time.sleep(delay)

    def subscribe(self) -> None:
        def on_connect(client, userdata, flags, reason_code, properties):
            print("Connected to MQTT Broker!")
            client.subscribe(self._topic)

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self._client.on_connect = on_connect
        self._client.on_message = on_message

    def run(self) -> None:
        self.subscribe()
        self.connect()
        self._client.loop_forever()


class Command(BaseCommand):
    def handle(self, **options):
        host = os.getenv("MQTT_HOST", "localhost")
        port = int(os.getenv("MQTT_PORT", "1883"))
        subscriber = MqttSubscriber(host, port)
        subscriber.run()