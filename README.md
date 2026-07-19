# Dashboard de Sensores IoT (MQTT + Django + Next.js)

Solução do desafio técnico: ingestão, persistência e visualização de dados IoT recebidos via MQTT.

O projeto consome uplinks de dispositivos LoRaWAN (formato ChirpStack v4) publicados num broker
MQTT, persiste as leituras num banco PostgreSQL, expõe os dados via uma API em Django REST
Framework e os visualiza num dashboard em Next.js 15 com React Query.

## Stack

- **Back-end**: Django + Django REST Framework
- **Consumidor MQTT**: management command do Django (paho-mqtt)
- **Banco**: PostgreSQL
- **Front-end**: Next.js 15 + React Query
- **Infra local**: Docker Compose
- **Fonte de dados** (já fornecida): broker Mosquitto + gerador de uplinks simulados

## Como rodar

Pré-requisitos: **Docker** e **Docker Compose**.

Na raiz do projeto:

```bash
docker compose up --build
```

Isso sobe todos os serviços:

- `broker` — broker MQTT (Mosquitto)
- `generator` — simulador que publica uplinks continuamente
- `db` — PostgreSQL
- `backend` — API Django (roda as migrations e sobe o servidor)
- `mqtt_consumer` — consumidor que assina o broker e persiste as leituras
- `frontend` — dashboard Next.js

Depois que tudo subir, acesse:

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000/api/devices/
- **Admin do Django**: http://localhost:8000/admin/ (requer superusuário, veja abaixo)

A primeira subida demora um pouco (baixa imagens e instala dependências). Os dados começam a
aparecer no dashboard alguns segundos depois, conforme o gerador publica e o consumidor persiste.

### Criar um superusuário (opcional, para o admin)

Com os containers rodando, em outro terminal:

```bash
docker compose exec backend python manage.py createsuperuser
```

## Endpoints da API

- `GET /api/devices/` — lista os dispositivos com o estado atual (última leitura de cada sensor)
  embutido no campo `current_state`.
- `GET /api/devices/{id}/readings/` — histórico de leituras de um dispositivo.

## Estrutura do repositório

```
.
├── docker-compose.yml     # orquestra todos os serviços
├── mosquitto/             # config do broker (fonte de dados, não alterada)
├── generator/             # simulador de uplinks (fonte de dados, não alterada)
├── backend/               # Django: API + consumidor MQTT
│   ├── core/              # settings, urls
│   └── telemetry/         # models, serializers, views, consumidor MQTT
└── frontend/              # dashboard Next.js
```

## Sobre os dados

Cada dispositivo publica uplinks no tópico
`application/{applicationId}/device/{devEui}/event/up`, no formato de evento do ChirpStack v4.
As leituras já decodificadas ficam no campo `object` do payload, cujas chaves variam conforme o
modelo do dispositivo. Os detalhes de modelagem e das decisões técnicas estão no
[DECISIONS.md](DECISIONS.md).

## Desenvolvimento fora do Docker (opcional)

Para rodar o back-end direto na máquina durante o desenvolvimento (com o broker e o banco no
Docker):

```bash
# na raiz: subir só broker, generator e banco
docker compose up -d broker generator db

# back-end
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver        # API em http://localhost:8000
python manage.py run_mqtt_consumer  # em outro terminal, o consumidor

# front-end
cd frontend
npm install
npm run dev                       # dashboard em http://localhost:3000
```

Nesse modo, o back-end acessa o broker e o banco via `localhost` (as portas ficam expostas pelo
Docker Compose).