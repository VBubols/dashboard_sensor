import random
from dataclasses import dataclass


@dataclass
class Drift:
    value: float
    minimum: float
    maximum: float
    step: float
    precision: int = 2

    def next(self) -> float:
        self.value += random.uniform(-self.step, self.step)
        self.value = min(self.maximum, max(self.minimum, self.value))
        return round(self.value, self.precision)


class Dtl110:
    profile_id = "69f66330-747a-4705-b2a9-0b65b900bb0e"
    profile_name = "Khomp DTL 110 temperatura e umidade outdoor"

    def __init__(self, internal_temp: Drift, internal_hum: Drift,
                 external_temp: Drift, external_hum: Drift) -> None:
        self._internal_temp = internal_temp
        self._internal_hum = internal_hum
        self._external_temp = external_temp
        self._external_hum = external_hum
        self._battery = Drift(3.03, 3.0, 3.6, 0.002, precision=3)

    def build_object(self) -> dict:
        return {
            "Bat_status": 3,
            "Bateria": self._battery.next(),
            "Modo": "SHT31 Sensor",
            "TempC_SHT": self._internal_temp.next(),
            "Hum_SHT": self._internal_hum.next(),
            "Ext_TempC_SHT": self._external_temp.next(),
            "Ext_Hum_SHT": self._external_hum.next(),
        }


@dataclass
class Device:
    dev_eui: str
    name: str
    profile: Dtl110
    f_cnt: int = 0

    def read(self) -> dict:
        self.f_cnt += 1
        return self.profile.build_object()


def _temp(value: float, low: float, high: float) -> Drift:
    return Drift(value, low, high, 0.3, precision=2)


def _hum(value: float, low: float, high: float) -> Drift:
    return Drift(value, low, high, 1.0, precision=1)


def build_fleet() -> list[Device]:
    return [
        Device("0004a30b001a2b03", "camara-fria-laticinios",
               Dtl110(_temp(7.0, 4.0, 11.0), _hum(45.0, 35.0, 60.0),
                      _temp(4.0, 1.0, 8.0), _hum(82.0, 70.0, 95.0))),
        Device("0004a30b001a2b04", "camara-fria-hortifruti",
               Dtl110(_temp(9.0, 5.0, 14.0), _hum(55.0, 45.0, 70.0),
                      _temp(6.0, 2.0, 10.0), _hum(88.0, 75.0, 96.0))),
        Device("0004a30b001a2b01", "freezer-camara-01",
               Dtl110(_temp(2.0, -2.0, 6.0), _hum(40.0, 30.0, 55.0),
                      _temp(-18.0, -24.0, -14.0), _hum(70.0, 55.0, 85.0))),
        Device("0004a30b001a2b05", "sala-servidores",
               Dtl110(_temp(23.0, 19.0, 28.0), _hum(45.0, 35.0, 55.0),
                      _temp(21.0, 17.0, 26.0), _hum(48.0, 38.0, 60.0))),
        Device("0004a30b001a2b06", "doca-recebimento",
               Dtl110(_temp(26.0, 18.0, 33.0), _hum(60.0, 45.0, 78.0),
                      _temp(24.0, 16.0, 32.0), _hum(62.0, 45.0, 80.0))),
    ]
