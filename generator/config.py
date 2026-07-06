import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    mqtt_host: str
    mqtt_port: int
    publish_interval_seconds: float

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            mqtt_host=os.getenv("MQTT_HOST", "localhost"),
            mqtt_port=int(os.getenv("MQTT_PORT", "1883")),
            publish_interval_seconds=float(os.getenv("PUBLISH_INTERVAL_SECONDS", "3")),
        )
