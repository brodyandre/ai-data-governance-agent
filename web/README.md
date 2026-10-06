# 🖥️ Interface Web — AI Data Governance Agent

Este diretório está reservado para a interface web de demonstração do **AI Data Governance Agent**.

A interface será implementada após a estabilização dos contratos do backend e da API.

---

## 🎯 Objetivo

A camada web terá como principal função demonstrar, de forma clara e profissional, o fluxo de análise de incidentes realizado pelo sistema.

A interface deverá permitir:

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

---

## 🧰 Stack planejada

A implementação principal utilizará:

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

---

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

A interface web não deverá duplicar regras de negócio já existentes no backend.

Seu papel principal será consumir e apresentar os contratos expostos pela API.

---

## 🔌 Dependência da API

A implementação da interface será iniciada somente depois que o contrato principal da API estiver definido e estável.

Endpoint planejado:

```text
POST /api/v1/incidents/analyze
```

A interface deverá consumir a resposta estruturada definida em:

```text
docs/contracts/AGENT_RESPONSE.md
```

---

## 🎨 Diretrizes de experiência

A apresentação deverá priorizar:

- hierarquia visual;
- legibilidade;
- clareza;
- navegação simples;
- visualização objetiva de riscos;
- destaque para severidade;
- destaque para revisão humana;
- rastreabilidade das evidências.

A interface deverá comunicar tanto os aspectos técnicos quanto o impacto de negócio da análise.

---

## 🧪 Comportamento de demonstração

A aplicação poderá oferecer cenários predefinidos para facilitar a demonstração do projeto.

Exemplos planejados:

- incidente de Data Quality;
- divergência de reconciliação;
- evidência insuficiente;
- evidências conflitantes;
- incidente de alta severidade;
- incidente crítico;
- situação que exige revisão humana.

Esses cenários deverão utilizar contratos válidos e permanecer reproduzíveis.

---

## 🛟 Alternativa de contingência

Caso a interface Node.js não possa ser concluída dentro do prazo com qualidade adequada, **Streamlit** poderá ser utilizado como alternativa.

Essa opção permanece apenas como contingência.

A abordagem principal continua sendo:

```text
Node.js + Express + EJS + Vanilla JavaScript
```

---

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

---

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

> 🖥️ A camada web do **AI Data Governance Agent** será uma interface de demonstração orientada à clareza, rastreabilidade e comunicação do valor técnico e de negócio da solução.