# Desafio Técnico: Desenvolvedor(a) Full-Stack Júnior

Stack obrigatória: Django / Django REST Framework + Next.js 15 + React Query.
Contexto: ingestão, persistência e visualização de dados IoT via MQTT.

Olá!

Este desafio faz parte do nosso processo seletivo para a vaga de Desenvolvedor(a) Full-Stack Júnior. Ele foi pensado para ser justo com o seu tempo e para entendermos como você pensa, organiza decisões técnicas e resolve problemas reais. Mais do que escrever código perfeito, queremos avaliar clareza, capacidade de priorização, modelagem, comunicação e entendimento da solução de ponta a ponta.

## O que você recebe

Você recebe um ambiente pronto para uso. Ao executar `docker compose up`, o projeto sobe um broker MQTT com dados simulados de dispositivos IoT sendo publicados continuamente em tópicos.

A estrutura dos tópicos e o formato dos payloads estão documentados no [README.md](README.md). Você não precisa alterar esse ambiente. Ele existe apenas como fonte de dados. Seu trabalho começa a partir do consumo dessas mensagens.

## O desafio

Sua missão é dar sentido aos dados recebidos via MQTT. Você deverá construir uma aplicação capaz de:

1. Consumir mensagens MQTT dentro de um serviço Django.
2. Modelar e persistir os dados recebidos.
3. Expor os dados por meio de uma API usando Django REST Framework.
4. Criar um dashboard simples em Next.js 15 com React Query para exibir a temperatura e a umidade dos dispositivos.
5. Orquestrar a solução para que tudo rode com `docker compose up`.

A modelagem dos dados é uma decisão sua. Pense em entidades como dispositivos, sensores e leituras ao longo do tempo. A escolha do banco de dados também é livre, desde que seja justificada.

## Organização do repositório

Faça um fork (ou clone) do repositório base e desenvolva dentro dele. O objetivo é que, na raiz, um único `docker compose up` suba tudo: broker, generator, o seu serviço Django e o seu dashboard.

Estrutura sugerida (a exata é decisão sua):

```
.
├── docker-compose.yml     # já existe; adicione aqui os seus serviços
├── mosquitto/             # não altere (fonte de dados)
├── generator/             # não altere (fonte de dados)
├── backend/               # seu serviço Django (consumidor + API)
└── frontend/              # seu dashboard (Next.js)
```

Adicione os seus serviços (back-end, dashboard e o banco de dados que escolher) ao `docker-compose.yml` existente, na mesma rede do `broker`. Não altere os serviços `broker` e `generator` nem o `mosquitto.conf`.

## Escopo esperado

A entrega mínima válida é um serviço que consiga consumir as mensagens MQTT, interpretar os payloads e persistir os dados corretamente.

A partir disso, esperamos que você avance o máximo possível nos seguintes pontos:

- API para consulta dos dados persistidos.
- Visualização da temperatura e da umidade atuais de cada dispositivo.
- Visualização do histórico de temperatura e umidade por dispositivo.
- Organização da aplicação para rodar de ponta a ponta via Docker Compose.

O dashboard não precisa ser visualmente sofisticado. Ele precisa ser funcional, claro e coerente com os dados disponíveis. O mais importante é que a parte que você declarar como implementada realmente funcione.

## Stack e regras

A stack obrigatória é:

- Back-end: Django + Django REST Framework.
- Front-end: Next.js 15 + React Query.
- Infra local: Docker Compose.

O uso de IA é liberado e incentivado. Use as ferramentas que você usaria no trabalho real. Em troca, pedimos transparência no `DECISIONS.md`, explicando onde a IA ajudou e quais sugestões foram aproveitadas, corrigidas ou descartadas.

Suposições são bem-vindas, desde que documentadas. Caso algo não esteja claro, você pode perguntar ou registrar a suposição adotada e seguir em frente. O que queremos evitar são decisões importantes tomadas sem explicação.

## O que entregar

Um repositório Git contendo:

1. O código da solução, com os seus serviços já integrados ao `docker-compose.yml`.
2. Um `README.md` com instruções claras para rodar o projeto localmente.
3. Um `DECISIONS.md` curto, explicando:
   - escolhas técnicas;
   - escolha do banco de dados;
   - raciocínio na modelagem;
   - suposições adotadas;
   - onde a IA ajudou e o que você aproveitou, corrigiu ou descartou.

## Diferenciais opcionais

Os itens abaixo contam a favor, mas não são requisitos:

- Autenticação.
- CI/CD.
- Testes automatizados.
- Tratamento de falhas na ingestão.
- Cache.
- Retenção de dados.
- Otimizações para séries temporais.
- Filtros no dashboard.
- Paginação ou agregações no histórico.

Não tente implementar todos os diferenciais se isso comprometer a qualidade do escopo principal.

## Critérios de avaliação

Vamos avaliar principalmente:

- Clareza da solução.
- Organização do código.
- Capacidade de modelar dados de dispositivos, sensores e leituras.
- Persistência correta dos dados.
- Qualidade e coerência da API.
- Funcionalidade do dashboard.
- Facilidade para rodar o projeto localmente.
- Capacidade de explicar o que foi feito.

Não esperamos uma solução perfeita. Esperamos uma solução compreensível, funcional e bem justificada.

## Próxima etapa

Depois da entrega, faremos um walkthrough ao vivo de aproximadamente 45 minutos. Será uma conversa técnica e colaborativa, em que você irá nos guiar pelo código, explicar suas escolhas e fazer uma ou duas pequenas alterações junto com a equipe.

A ideia é simular uma dinâmica parecida com o dia a dia de trabalho. Por isso, vale mais entregar algo que você realmente entende de ponta a ponta do que uma solução grande demais e difícil de explicar.

## Como entregar

Suba o código em um repositório Git, no GitHub ou GitLab, e compartilhe o link pelo mesmo canal usado no processo seletivo, dentro do prazo combinado. Caso o repositório seja privado, garanta o acesso para a equipe avaliadora.
