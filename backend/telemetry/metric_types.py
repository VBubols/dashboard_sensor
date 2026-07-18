METRIC_TYPE_MAP = {
    "TempC_SHT": "temperature",
    "Ext_TempC_SHT": "temperature",
    "Hum_SHT": "humidity",
    "Ext_Hum_SHT": "humidity",
    "Bateria": "battery",
    "Bat_status": "battery_status",
    "Modo": "mode",
}

def resolve_metric_type(metric_key: str) -> str:
    return METRIC_TYPE_MAP.get(metric_key, "unknown")