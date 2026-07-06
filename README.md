# Desafio Técnico: Ambiente e Dados

Vaga: Desenvolvedor(a) Full-Stack Júnior. Stack: Django / DRF + Next.js 15 / React Query.

O enunciado do desafio (missão, escopo, regras, entregáveis e critérios de avaliação) está em [DESAFIO.md](DESAFIO.md). Este README descreve o ambiente que você recebe e o formato dos dados.

Este repositório já entrega um ambiente funcionando: um broker MQTT recebendo dados de sensores IoT continuamente. Você não precisa mexer nele. Seu trabalho é consumir esses dados e dar sentido a eles.

## 1. Subindo o ambiente

Pré-requisitos: Docker e Docker Compose.

```bash
docker compose up
```

Isso sobe dois serviços:

- `broker`: um broker MQTT (Mosquitto), exposto na porta `1883`.
- `generator`: um simulador que publica continuamente uplinks de dispositivos LoRaWAN (estilo ChirpStack) no broker.

Para confirmar que os dados estão chegando, abra outro terminal e assine todos os dispositivos com wildcard:

```bash
docker compose exec broker mosquitto_sub -t 'application/#' -v
```

Você verá uma mensagem nova a cada poucos segundos, cada uma num subtópico diferente.

### Como o seu serviço se conecta ao broker

- De dentro do `docker compose` (é assim que esperamos a entrega): use o host `broker` na porta `1883`.
- Rodando direto na sua máquina durante o desenvolvimento: use `localhost` na porta `1883`.

## 2. O fluxo de dados

Cada dispositivo publica no seu próprio subtópico, seguindo a convenção do ChirpStack:

```
application/{applicationId}/device/{devEui}/event/up
```

Para receber todos os dispositivos de uma vez, assine com wildcard: `application/+/device/+/event/up` (ou, mais amplo, `application/#`).

Cada mensagem é um evento de uplink do ChirpStack v4, o mesmo JSON que o ChirpStack publica na integração MQTT: o envelope da rede LoRaWAN somado ao payload já decodificado do dispositivo. Exemplo (sensor Khomp DTL 110 de temperatura e umidade):

```json
{
  "deduplicationId": "9ce591b6-98b8-471f-ae22-837edf8c03d5",
  "time": "2026-06-09T20:56:32.299949+00:00",
  "deviceInfo": {
    "tenantId": "e09b6a3e-7d09-4d74-b2d3-7a177d49d3df",
    "tenantName": "SensorWeb",
    "applicationId": "17c82e96-be03-4f38-9d4a-9b1d2e6f3f10",
    "applicationName": "Developer",
    "deviceProfileId": "69f66330-747a-4705-b2a9-0b65b900bb0e",
    "deviceProfileName": "Khomp DTL 110 temperatura e umidade outdoor",
    "deviceName": "camara-fria-laticinios",
    "devEui": "0004a30b001a2b03",
    "deviceClassEnabled": "CLASS_A",
    "tags": {}
  },
  "devAddr": "002de538",
  "adr": true,
  "dr": 5,
  "fCnt": 934,
  "fPort": 2,
  "confirmed": false,
  "data": "y9UC0wEqCwGSAUg=",
  "object": {
    "Bat_status": 3,
    "Bateria": 3.029,
    "Modo": "SHT31 Sensor",
    "TempC_SHT": 7.23,
    "Hum_SHT": 29.8,
    "Ext_TempC_SHT": 4.02,
    "Ext_Hum_SHT": 32.8
  },
  "rxInfo": [
    {
      "gatewayId": "ac1f09fffe10a29b",
      "uplinkId": 52221,
      "nsTime": "2026-06-09T20:56:32.090899+00:00",
      "rssi": -87,
      "snr": 10.8,
      "channel": 2,
      "location": {},
      "context": "vfIzZw==",
      "crcStatus": "CRC_OK"
    }
  ],
  "txInfo": {
    "frequency": 915600000,
    "modulation": {
      "lora": { "bandwidth": 125000, "spreadingFactor": 7, "codeRate": "CR_4_5" }
    }
  },
  "regionConfigId": "au915_0"
}
```

O que cada parte da mensagem contém:

- `object`: as leituras já decodificadas do sensor. Neste perfil (Khomp DTL 110): `TempC_SHT` e `Hum_SHT` (sensor interno), `Ext_TempC_SHT` e `Ext_Hum_SHT` (sonda externa), `Bateria` (em volts), `Bat_status` e `Modo`. As chaves de `object` variam conforme o modelo do dispositivo.
- `data`: o mesmo payload em base64, ainda sem decodificar. Use o `object`.
- O restante do JSON é o envelope da rede LoRaWAN que o ChirpStack adiciona a cada mensagem (identificação, qualidade do sinal, contadores de frame e parâmetros de rádio). O dispositivo é identificado por `deviceInfo.devEui`, e `deviceProfileName` traz o modelo.

O tenant e a aplicação são fixos, então você não precisa lidar com multi-tenancy. Os dados são simulados, com nomes plausíveis (modelos Khomp), e não correspondem a um datasheet real.

## 3. Não altere a fonte de dados

Os serviços `broker` e `generator` e o arquivo `mosquitto.conf` são a fonte de dados do desafio. Não os altere. Adicione os seus serviços (back-end, dashboard e o banco de dados que escolher) ao `docker-compose.yml`, na mesma rede do `broker`. A organização sugerida do repositório está no [DESAFIO.md](DESAFIO.md).
