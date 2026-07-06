import time

import paho.mqtt.client as mqtt


class MqttPublisher:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
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
        self._client.loop_start()

    def publish(self, topic: str, payload: str) -> None:
        self._client.publish(topic, payload, qos=0)
