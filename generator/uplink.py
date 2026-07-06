import base64
import random
import uuid
from datetime import datetime, timezone

from devices import Device

TENANT_ID = "e09b6a3e-7d09-4d74-b2d3-7a177d49d3df"
TENANT_NAME = "SensorWeb"
APPLICATION_ID = "17c82e96-be03-4f38-9d4a-9b1d2e6f3f10"
APPLICATION_NAME = "Developer"
GATEWAY_ID = "ac1f09fffe10a29b"
REGION_CONFIG_ID = "au915_0"
AU915_FREQUENCIES = [915200000, 915400000, 915600000, 915800000, 916000000]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _random_hex(num_bytes: int) -> str:
    return bytes(random.getrandbits(8) for _ in range(num_bytes)).hex()


def _random_base64(num_bytes: int) -> str:
    return base64.b64encode(bytes(random.getrandbits(8) for _ in range(num_bytes))).decode()


def _device_info(device: Device) -> dict:
    return {
        "tenantId": TENANT_ID,
        "tenantName": TENANT_NAME,
        "applicationId": APPLICATION_ID,
        "applicationName": APPLICATION_NAME,
        "deviceProfileId": device.profile.profile_id,
        "deviceProfileName": device.profile.profile_name,
        "deviceName": device.name,
        "devEui": device.dev_eui,
        "deviceClassEnabled": "CLASS_A",
        "tags": {},
    }


def _rx_info() -> list[dict]:
    return [
        {
            "gatewayId": GATEWAY_ID,
            "uplinkId": random.randint(1, 100000),
            "nsTime": _now(),
            "rssi": random.randint(-115, -60),
            "snr": round(random.uniform(-5.0, 11.0), 1),
            "channel": random.randint(0, 7),
            "location": {},
            "context": _random_base64(4),
            "crcStatus": "CRC_OK",
        }
    ]


def _tx_info() -> dict:
    return {
        "frequency": random.choice(AU915_FREQUENCIES),
        "modulation": {
            "lora": {
                "bandwidth": 125000,
                "spreadingFactor": random.choice([7, 8, 9, 10]),
                "codeRate": "CR_4_5",
            }
        },
    }


def build_uplink(device: Device, decoded: dict) -> dict:
    return {
        "deduplicationId": str(uuid.uuid4()),
        "time": _now(),
        "deviceInfo": _device_info(device),
        "devAddr": _random_hex(4),
        "adr": True,
        "dr": random.randint(0, 5),
        "fCnt": device.f_cnt,
        "fPort": 2,
        "confirmed": False,
        "data": _random_base64(random.randint(6, 11)),
        "object": decoded,
        "rxInfo": _rx_info(),
        "txInfo": _tx_info(),
        "regionConfigId": REGION_CONFIG_ID,
    }


def uplink_topic(device: Device) -> str:
    return f"application/{APPLICATION_ID}/device/{device.dev_eui}/event/up"
