# DECISIONS.md

## Banco de dados

Escolhi **PostgreSQL**. É o banco relacional com o qual tenho mais familiaridade, é robusto e
lida bem tanto com os relacionamentos entre dispositivos, sensores e leituras quanto com o
volume de série temporal deste desafio.

Alternativas que considerei:

- **SQLite**: ótimo para começar rápido e sem infra, mas menos representativo de um cenário real
  de ingestão contínua de dados. Como o próprio desafio simula um fluxo constante de mensagens,
  preferi já usar algo mais próximo de produção.
- **Bancos de série temporal (TimescaleDB, InfluxDB)**: são mais otimizados para time-series, mas
  trariam complexidade desnecessária para o volume deste desafio. Ficam como evolução natural se o
  volume crescesse muito.

Suposição de escala: são 5 dispositivos publicando uma leitura a cada ~15 segundos cada
(o gerador cicla entre eles a cada 3s). Isso é um volume baixo, que o Postgres puro atende
tranquilamente sem otimizações especiais de série temporal.

## Modelagem de dados

Modelei em três entidades: **Device → Sensor → Reading**.

- **Device**: o dispositivo físico, identificado pelo `devEui` (único). Guarda também nome e o
  perfil (`deviceProfileId`/`deviceProfileName`).
- **Sensor**: cada métrica individual de um dispositivo (ex.: `TempC_SHT`, `Hum_SHT`). Pertence a
  um Device e é único por `(device, metric_key)`.
- **Reading**: cada leitura de um sensor no tempo (valor + timestamp).

A decisão central foi como lidar com o `object`, que é um dicionário plano cujas chaves mudam
conforme o modelo do dispositivo. Optei **por não criar colunas fixas** (tipo `temperatura`,
`umidade`), porque isso só funcionaria para o DTL110 e quebraria o schema assim que aparecesse um
modelo com chaves diferentes. Em vez disso, o consumidor **descobre os sensores dinamicamente**:
para cada chave do `object`, faz um `get_or_create` de Sensor e cria uma Reading. Assim, um modelo
novo de dispositivo é persistido sem nenhuma mudança de schema.

Para deixar os dados legíveis no dashboard sem perder a chave crua, adicionei uma camada de
normalização (`metric_type`, `label` e `unit`) que mapeia cada `metric_key` para um significado
amigável — por exemplo, `TempC_SHT` vira "Temperatura interna", em °C. Se aparecer uma chave
desconhecida, ela ainda é persistida (com `metric_type` "unknown"), então nenhum dado é perdido.

Valores não numéricos do `object` (como `Modo`, que é uma string) são ignorados na ingestão,
já que Reading guarda um valor numérico.

## Arquitetura e API

As peças se encaixam assim:

- **Consumidor MQTT**: implementado como um *management command* do Django
  (`python manage.py run_mqtt_consumer`). Ele assina o tópico wildcard
  `application/+/device/+/event/up`, faz o parse do uplink, e persiste os dados usando os models.
  Usei um management command (em vez de um script solto) para rodar dentro do contexto do Django e
  ter acesso direto ao ORM.
- **Back-end (Django + DRF)**: expõe os dados persistidos via API REST.
- **Dashboard (Next.js 15 + React Query)**: consome a API e exibe estado atual e histórico.

A API tem dois endpoints principais, espelhando as duas necessidades do dashboard:

- `GET /api/devices/` — lista os dispositivos, cada um com um `current_state` embutido (a leitura
  mais recente de cada sensor). Serve a tela principal de "estado atual de todos".
- `GET /api/devices/{id}/readings/` — histórico de leituras de um dispositivo, para os gráficos.

Escolhi embutir o `current_state` na listagem de devices para o dashboard montar os cards com uma
única requisição, em vez de buscar as leituras de cada dispositivo separadamente.

## Suposições

- **Identidade do dispositivo**: usei o `devEui` como identificador único (é o identificador
  físico do dispositivo na rede LoRaWAN).
- **"Estado atual"**: interpretei como a leitura mais recente de cada sensor do dispositivo.
- **Deduplicação**: não implementei deduplicação por `deduplicationId`; assumi que cada uplink
  recebido é uma leitura nova válida.
- **Multi-tenancy**: o tenant e a aplicação são fixos (o README do desafio confirma isso), então
  não tratei múltiplos tenants.
- **`Bat_status` e `Modo`**: no gerador são valores constantes; `Modo` é string e é ignorado,
  `Bat_status` é persistido mas não tem muito valor de monitoramento.
- **Horizonte de histórico**: o endpoint de histórico retorna todas as leituras do dispositivo
  (sem recorte de janela), o que é aceitável para o volume do desafio.

## Trade-offs e o que ficou de fora

Priorizei ter o fluxo completo funcionando de ponta a ponta e bem compreensível — ingestão,
persistência, API e dashboard — em vez de cobrir muitos diferenciais de forma superficial.

Ficaram de fora, de propósito, para caber no tempo:

- Autenticação.
- Testes automatizados.
- Tratamento mais robusto de falhas na ingestão (reconexão automática do MQTT, mensagens
  malformadas, etc.).
- Paginação/agregação no endpoint de histórico.
- Filtros no dashboard.

Com mais algumas horas, eu priorizaria **paginação e agregação no histórico** (hoje ele traz todas
as leituras) e uma primeira camada de **testes automatizados** cobrindo o parse do uplink e a API.

## Uso de IA

Usei o **Claude** como apoio ao longo do desafio, principalmente porque parte da stack era nova
para mim — eu não tinha experiência com Django/DRF, e os conceitos de MQTT/LoRaWAN/ChirpStack
também eram novos. Usei a IA para entender esses conceitos, estruturar o consumidor MQTT
(especialmente o padrão de callbacks do paho-mqtt), pensar o trade-off de modelagem do `object`
com chaves variáveis, e destravar vários problemas de ambiente (versão de Python, Docker em uma
distro antiga, etc.).

Escrevi o código eu mesmo, com orientação passo a passo, e revisei/ajustei o que foi sugerido —
por exemplo, ajustei os `label`/`unit` das métricas para nomes que fizessem sentido no dashboard,
corrigi erros de digitação e de lógica ao longo do caminho, e tomei as decisões de modelagem e de
API. Entendo cada parte da solução de ponta a ponta.