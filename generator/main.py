import json
import time

from config import Settings
from devices import build_fleet
from publisher import MqttPublisher
from uplink import build_uplink, uplink_topic


def main() -> None:
    settings = Settings.from_env()
    fleet = build_fleet()

    publisher = MqttPublisher(settings.mqtt_host, settings.mqtt_port)
    publisher.connect()

    print(
        f"Publishing simulated ChirpStack uplinks every {settings.publish_interval_seconds}s",
        flush=True,
    )

    index = 0
    while True:
        device = fleet[index % len(fleet)]
        topic = uplink_topic(device)
        publisher.publish(topic, json.dumps(build_uplink(device, device.read())))
        print(f"-> {topic}  fCnt={device.f_cnt}", flush=True)
        index += 1
        time.sleep(settings.publish_interval_seconds)


if __name__ == "__main__":
    main()
