# 🖥️ Interface Web — AI Data Governance Agent

Este diretório contém a interface web de demonstração do **AI Data Governance Agent**.

A interface está implementada em Node.js, Express, EJS e Vanilla JavaScript e consome a API FastAPI sem duplicar as regras centrais de negócio.

---

<a id="sumario"></a>

## 📑 Sumário

- [Objetivo](#objetivo)
- [Stack implementada](#stack)
- [Arquitetura conceitual](#arquitetura)
- [Dependência da API](#api)
- [Diretrizes de experiência](#experiencia)
- [Comportamento de demonstração](#demonstracao)
- [Alternativa de contingência](#contingencia)
- [Limites de escopo](#limites)
- [Princípio](#principio)

---

<a id="objetivo"></a>

## 🎯 Objetivo

A camada web tem como principal função demonstrar, de forma clara e profissional, o fluxo de análise de incidentes realizado pelo sistema.

A interface permite:

- informar ou carregar um incidente;
- enviar o incidente para análise;
- visualizar a classificação atribuída;
- visualizar a severidade;
- consultar o resumo executivo;
- examinar as evidências utilizadas;
- visualizar impacto de negócio;
- consultar hipóteses de causa raiz;
- visualizar ações recomendadas;
- consultar controles de governança;
- visualizar o nível de `confidence`;
- identificar quando revisão humana é obrigatória.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="stack"></a>

## 🧰 Stack implementada

A implementação utiliza:

```text
Node.js
Express
EJS
Vanilla JavaScript
```

Essa combinação foi escolhida para manter a interface:

- simples;
- leve;
- de fácil manutenção;
- adequada para demonstração;
- integrada à API FastAPI sem complexidade desnecessária.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="arquitetura"></a>

## 🏗️ Arquitetura conceitual

```text
Usuário
   │
   ▼
Interface Web
Node.js + Express + EJS
   │
   ▼
FastAPI
   │
   ▼
Workflow do Agente
   │
   ▼
AgentResponse
   │
   ▼
Interface Web
```

A interface web não duplica regras de negócio existentes no backend.

Seu papel principal é consumir e apresentar os contratos expostos pela API.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="api"></a>

## 🔌 Dependência da API

A interface utiliza o endpoint estável exposto pela API FastAPI.

Endpoint:

```text
POST /api/v1/incidents/analyze
```

A interface consome a resposta estruturada definida em:

```text
docs/contracts/AGENT_RESPONSE.md
```

O servidor Express recebe `POST /api/analyze` e encaminha o incidente ao backend FastAPI configurado por `API_BASE_URL`.

O valor padrão é `http://127.0.0.1:8000`.

### Execução local

Instalar dependências:

`npm ci`

Executar testes:

`npm test`

Iniciar a interface:

`npm start`

Por padrão, a interface utiliza a porta `3000`. As variáveis operacionais suportadas são `API_BASE_URL` e `PORT`.

O runtime não exige credenciais. A API padrão não configura automaticamente um provider; nesse caso, uma tentativa de análise recebe `503 provider_not_configured`.

Para a demonstração controlada dos cenários DE-101 e DE-102, utilizar o [`LIVE_DEMO_RUNBOOK.md`](../docs/demo/LIVE_DEMO_RUNBOOK.md).

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="experiencia"></a>

## 🎨 Diretrizes de experiência

A apresentação prioriza:

- hierarquia visual;
- legibilidade;
- clareza;
- navegação simples;
- visualização objetiva de riscos;
- destaque para severidade;
- destaque para revisão humana;
- rastreabilidade das evidências.

A interface comunica tanto os aspectos técnicos quanto o impacto de negócio da análise.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="demonstracao"></a>

## 🧪 Comportamento de demonstração

A aplicação oferece dois cenários canônicos carregáveis diretamente pela interface:

- [`DE-101`](../docs/scenarios/DE-101.md) — elegibilidade e reconciliação Silver → Gold;
- [`DE-102`](../docs/scenarios/DE-102.md) — governança da semântica de receita.

Cenários adversariais adicionais, como evidência insuficiente, evidência conflitante, severidade crítica e afirmação sem suporte, permanecem versionados no framework de avaliação determinística.

Os cenários utilizam contratos válidos e permanecem reproduzíveis.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="contingencia"></a>

## 🛟 Alternativa de contingência

A interface Node.js foi concluída e é a implementação oficial do MVP.

A alternativa em Streamlit não foi necessária e permanece fora do caminho principal da demonstração.

A stack oficial é:

```text
Node.js + Express + EJS + Vanilla JavaScript
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="limites"></a>

## 🚧 Limites de escopo

Antes da entrega do Challenge, a interface não precisa incluir:

- React;
- Next.js;
- arquitetura SPA complexa;
- autenticação corporativa;
- IAM;
- WebSockets;
- processamento em tempo real complexo;
- banco de dados próprio;
- infraestrutura distribuída.

O foco é demonstrar claramente o valor funcional do agente.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)

---

<a id="principio"></a>

## 🧭 Princípio

```text
Backend
   ↓
Produz análise estruturada
   ↓
Interface
   ↓
Apresenta a análise com clareza
```

A interface deve permanecer desacoplada das regras centrais de negócio.

---

> 🖥️ A camada web do **AI Data Governance Agent** é uma interface de demonstração orientada à clareza, rastreabilidade e comunicação do valor técnico e de negócio da solução.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../docs/README.md)
