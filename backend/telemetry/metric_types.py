METRIC_LABELS = {
    "TempC_SHT":     {"metric_type": "temperature",    "label": "Temperatura Interna",  "unit": "°C"},
    "Ext_TempC_SHT": {"metric_type": "temperature",    "label": "Temperatura Externa",  "unit": "°C"},
    "Hum_SHT":       {"metric_type": "humidity",       "label": "Umidade Interna",      "unit": "%"},
    "Ext_Hum_SHT":   {"metric_type": "humidity",       "label": "Umidade Externa",      "unit": "%"},
    "Bateria":       {"metric_type": "battery",        "label": "Voltagem da Bateria",  "unit": "V"},
    "Bat_status":    {"metric_type": "battery_status", "label": "Status da bateria",    "unit": ""},
    "Modo":          {"metric_type": "mode",           "label": "Modo",                 "unit": ""},
}

def resolve_metric_meta(metric_key: str) -> str:
    return METRIC_LABELS.get(
        metric_key,
        {"metric_type": "unknown", "label": metric_key, "unit": ""},
    )