# 📚 Central de Documentação — AI Data Governance Agent

Esta área reúne a documentação funcional, técnica e arquitetural do **AI Data Governance Agent**.

O objetivo desta página é funcionar como um **índice remissivo central**, permitindo localizar rapidamente decisões, contratos, regras de governança, planejamento, critérios de aceite e materiais de avaliação do projeto.

---

<a id="sumario"></a>

## 📑 Sumário

- [Visão e planejamento](#visao-planejamento)
- [Arquitetura](#arquitetura)
- [Contratos de domínio](#contratos)
- [Governança e supervisão humana](#governanca)
- [Avaliação](#avaliacao)
- [Demonstração do Challenge](#demonstracao)
- [Fluxo recomendado de leitura](#fluxo-leitura)
- [Convenções da documentação](#convencoes)
- [Manutenção da documentação](#manutencao)

---

<a id="visao-planejamento"></a>

## 🎯 Visão e planejamento

Os documentos desta seção explicam **por que o projeto existe, o que será construído e em qual sequência**.

| Documento | Finalidade |
|---|---|
| [`PROJECT_CHARTER.md`](PROJECT_CHARTER.md) | Define problema, objetivos, usuários, escopo, não escopo e critérios de sucesso |
| [`ROADMAP.md`](ROADMAP.md) | Organiza o desenvolvimento em fases progressivas |
| [`BACKLOG.md`](BACKLOG.md) | Detalha entregas, prioridades, complexidade e critérios de aceite |

### Ordem recomendada

```text
PROJECT_CHARTER
      ↓
ROADMAP
      ↓
BACKLOG
```

O `PROJECT_CHARTER` apresenta a visão do produto.

O `ROADMAP` transforma essa visão em etapas.

O `BACKLOG` transforma as etapas em unidades concretas de implementação.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="arquitetura"></a>

## 🏗️ Arquitetura

As decisões arquiteturais relevantes são registradas por meio de **Architecture Decision Records (ADRs)**.

| ADR | Decisão |
|---|---|
| [`ADR-001 — Escopo e Stack Tecnológica`](adrs/ADR-001-project-scope-and-stack.md) | Define arquitetura inicial, tecnologias, restrições e trade-offs |

Um ADR deve explicar:

- contexto;
- decisão;
- justificativa;
- consequências;
- trade-offs;
- condições que justificariam revisão futura.

Novos ADRs devem ser adicionados quando uma decisão arquitetural relevante precisar permanecer registrada e auditável.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="contratos"></a>

## 📦 Contratos de domínio

Os contratos representam a especificação formal utilizada como base para a implementação.

Eles permitem que comportamento, validação e estrutura dos dados sejam definidos antes da construção das camadas de aplicação.

| Documento | Responsabilidade |
|---|---|
| [`INCIDENT_INPUT.md`](contracts/INCIDENT_INPUT.md) | Estrutura conceitual de entrada de um incidente |
| [`EVIDENCE_MODEL.md`](contracts/EVIDENCE_MODEL.md) | Estrutura e regras aplicadas a uma evidência |
| [`DOMAIN_ENUMS.md`](contracts/DOMAIN_ENUMS.md) | Valores normalizados utilizados pelos modelos |
| [`AGENT_RESPONSE.md`](contracts/AGENT_RESPONSE.md) | Estrutura conceitual da resposta produzida pelo agente |
| [`SEVERITY_AND_HUMAN_REVIEW.md`](contracts/SEVERITY_AND_HUMAN_REVIEW.md) | Regras de severidade e critérios de revisão humana |
| [`PROVIDER_INTERFACE.md`](contracts/PROVIDER_INTERFACE.md) | Contrato independente de fornecedor para geração estruturada |

### Relação conceitual

```text
IncidentInput
     │
     ├── Evidence
     │
     ├── Severity
     │
     └── outros valores normalizados
     │
     ▼
Fluxo de análise
     │
     ▼
AgentResponse
     │
     ├── BusinessImpact
     ├── RootCauseHypothesis
     ├── RecommendedAction
     ├── GovernanceControl
     ├── confidence
     └── human_review_required
```

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="governanca"></a>

## 🛡️ Governança e supervisão humana

A governança é tratada como parte da arquitetura da solução e não como uma camada adicionada apenas ao final.

Os principais princípios são:

```text
Rastreabilidade
      +
Evidência
      +
Incerteza explícita
      +
Supervisão humana
      +
Decisão auditável
```

Os controles centrais são detalhados principalmente em:

➡️ [`contracts/SEVERITY_AND_HUMAN_REVIEW.md`](contracts/SEVERITY_AND_HUMAN_REVIEW.md)

e:

➡️ [`contracts/AGENT_RESPONSE.md`](contracts/AGENT_RESPONSE.md)

### Princípios fundamentais

O sistema deve:

- distinguir evidência de hipótese;
- evitar afirmações sem suporte;
- preservar referências às evidências utilizadas;
- declarar explicitamente quando informações forem insuficientes;
- representar incerteza;
- utilizar regras determinísticas sempre que apropriado;
- exigir revisão humana em situações de maior risco.

### Supervisão humana

A solução possui caráter consultivo.

A decisão humana permanece obrigatória em cenários como:

- severidade crítica;
- baixa confiança;
- evidência insuficiente;
- evidência conflitante;
- exposição regulatória;
- exposição de governança;
- impacto material de negócio;
- recomendações destrutivas ou irreversíveis.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="avaliacao"></a>

## 📊 Avaliação

O framework de avaliação determinística está implementado e documentado em [`EVALUATION.md`](EVALUATION.md).

A documentação de avaliação cobre:

- dataset de avaliação;
- cenários de teste;
- resultados esperados;
- definição das métricas;
- execução das avaliações;
- resultados obtidos;
- limitações conhecidas;
- relatórios.

### Métricas implementadas

| Métrica | Objetivo |
|---|---|
| `schema_valid_rate` | Medir conformidade das respostas com o contrato |
| `severity_accuracy` | Avaliar classificação de severidade |
| `evidence_traceability_rate` | Medir rastreabilidade entre conclusão e evidência |
| `unsupported_rejection_rate` | Avaliar rejeição de conclusões sem suporte |
| `human_review_accuracy` | Avaliar as decisões de revisão humana |
| `tool_execution_success_rate` | Medir sucesso da execução das ferramentas |
| `response_latency` | Avaliar tempo de resposta |
| `test_pass_rate` | Acompanhar estabilidade da suíte de testes |

As definições matemáticas, critérios de cálculo, comandos de execução e limitações estão registrados em [`EVALUATION.md`](EVALUATION.md).

No quality gate da DG-1001, os 7 cenários versionados foram aprovados e as taxas funcionais ficaram em 100% para o dataset determinístico utilizado. Esses resultados não representam avaliação de qualidade de um LLM real em produção.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="demonstracao"></a>

## 🎬 Demonstração do Challenge

A demonstração oficial do projeto utiliza cenários representativos e uma
narrativa explícita sobre evidências, limites da IA, governança e supervisão
humana.

| Documento | Finalidade |
|---|---|
| [`demo/DEMO_NARRATIVE.md`](demo/DEMO_NARRATIVE.md) | Narrativa canônica da demonstração e seus nove elementos |
| [`demo/LIVE_DEMO_RUNBOOK.md`](demo/LIVE_DEMO_RUNBOOK.md) | Procedimento reproduzível para execução da demonstração ao vivo |
| [`demo/PRESENTATION_SCRIPT.md`](demo/PRESENTATION_SCRIPT.md) | Roteiro de fala principal e versão curta para apresentação |
| [`scenarios/DE-101.md`](scenarios/DE-101.md) | Cenário canônico de elegibilidade Silver → Gold |
| [`scenarios/DE-102.md`](scenarios/DE-102.md) | Cenário canônico de governança da métrica de receita |

A demonstração controlada mantém transparência sobre o uso de provider
determinístico nas etapas dependentes de geração estruturada.

Ela não deve ser apresentada como avaliação de qualidade de um LLM real em
produção.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="fluxo-leitura"></a>

## 📖 Fluxo recomendado de leitura

Para compreender o projeto desde o problema de negócio até os contratos técnicos, a ordem recomendada é:

```text
README principal
      │
      ▼
PROJECT_CHARTER
      │
      ▼
ROADMAP
      │
      ▼
ADR-001
      │
      ▼
INCIDENT_INPUT
      │
      ▼
DOMAIN_ENUMS
      │
      ▼
EVIDENCE_MODEL
      │
      ▼
AGENT_RESPONSE
      │
      ▼
SEVERITY_AND_HUMAN_REVIEW
      │
      ▼
BACKLOG
```

### 1. README principal

Apresenta o projeto para quem está conhecendo o repositório.

### 2. PROJECT_CHARTER

Explica problema, objetivos, usuários, escopo e critérios de sucesso.

### 3. ROADMAP

Mostra como o desenvolvimento foi dividido em fases.

### 4. ADR-001

Registra as principais decisões arquiteturais iniciais.

### 5. Contratos de domínio

Definem formalmente dados de entrada, evidências, saída e regras de governança.

### 6. BACKLOG

Transforma a arquitetura planejada em tarefas implementáveis e testáveis.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="convencoes"></a>

## ✍️ Convenções da documentação

A documentação utiliza **português brasileiro (PT-BR)** como idioma principal.

Nomes que fazem parte da implementação permanecem em inglês, incluindo:

- classes;
- campos;
- funções;
- endpoints;
- ferramentas;
- bibliotecas;
- tecnologias;
- métricas;
- identificadores de domínio.

Exemplos:

```text
IncidentInput
AgentResponse
Evidence
evidence_id
human_review_required
quality_analyzer
business_impact_analyzer
schema_valid_rate
```

Essa abordagem mantém a documentação acessível em português sem criar divergência entre os documentos e o código.

### Termos técnicos

Alguns termos consolidados da área poderão permanecer em inglês quando sua tradução reduzir precisão ou clareza, como:

- Data Quality;
- Data Governance;
- DataOps;
- guardrails;
- human-in-the-loop;
- pipeline;
- lakehouse;
- workflow;
- framework;
- endpoint;
- runtime;
- code freeze.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)

---

<a id="manutencao"></a>

## 🔄 Manutenção da documentação

A documentação deve acompanhar a evolução real do projeto.

Os documentos devem ser revisados sempre que houver alterações relevantes em:

- escopo;
- requisitos;
- contratos;
- arquitetura;
- regras de governança;
- critérios de aceite;
- comportamento do sistema;
- métricas;
- fluxo de execução;
- tecnologias adotadas.

### Princípio de consistência

O projeto deve evitar divergências entre:

```text
Documentação
     ↕
Contratos
     ↕
Código
     ↕
Testes
     ↕
Demonstração
```

Uma decisão documentada que não represente mais o sistema deve ser atualizada.

Uma mudança arquitetural relevante deve ser registrada de forma explícita.

---

## 🗂️ Estrutura documental

```text
docs/
├── README.md
├── PROJECT_CHARTER.md
├── ROADMAP.md
├── BACKLOG.md
├── EVALUATION.md
├── adrs/
│   └── ADR-001-project-scope-and-stack.md
├── contracts/
│   ├── INCIDENT_INPUT.md
│   ├── AGENT_RESPONSE.md
│   ├── DOMAIN_ENUMS.md
│   ├── EVIDENCE_MODEL.md
│   └── SEVERITY_AND_HUMAN_REVIEW.md
├── demo/
│   ├── DEMO_NARRATIVE.md
│   ├── LIVE_DEMO_RUNBOOK.md
│   └── PRESENTATION_SCRIPT.md
├── scenarios/
│   ├── DE-101.md
│   └── DE-102.md
├── hardening/
│   ├── DG-1001-QUALITY-GATE.md
│   ├── DG-1002-SECURITY-REVIEW.md
│   ├── DG-1003-DOCUMENTATION-REVIEW.md
│   └── DG-1004-CODE-FREEZE.md
├── delivery/
│   ├── DG-1101-FINAL-DELIVERY-REVIEW.md
│   └── DG-1102-DEMO-EVIDENCE-VALIDATION.md
└── policies/
    └── LOCAL_CONTROLS.md
```

---

## 🔗 Navegação rápida

### Planejamento

- [`PROJECT_CHARTER.md`](PROJECT_CHARTER.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`BACKLOG.md`](BACKLOG.md)

### Arquitetura

- [`ADR-001`](adrs/ADR-001-project-scope-and-stack.md)

### Contratos

- [`INCIDENT_INPUT.md`](contracts/INCIDENT_INPUT.md)
- [`EVIDENCE_MODEL.md`](contracts/EVIDENCE_MODEL.md)
- [`DOMAIN_ENUMS.md`](contracts/DOMAIN_ENUMS.md)
- [`AGENT_RESPONSE.md`](contracts/AGENT_RESPONSE.md)
- [`PROVIDER_INTERFACE.md`](contracts/PROVIDER_INTERFACE.md)
- [`SEVERITY_AND_HUMAN_REVIEW.md`](contracts/SEVERITY_AND_HUMAN_REVIEW.md)

### Avaliação

- [`EVALUATION.md`](EVALUATION.md)

### Políticas

- [`LOCAL_CONTROLS.md`](policies/LOCAL_CONTROLS.md)

### Demonstração

- [`DEMO_NARRATIVE.md`](demo/DEMO_NARRATIVE.md)
- [`LIVE_DEMO_RUNBOOK.md`](demo/LIVE_DEMO_RUNBOOK.md)
- [`PRESENTATION_SCRIPT.md`](demo/PRESENTATION_SCRIPT.md)
- [`DE-101.md`](scenarios/DE-101.md)
- [`DE-102.md`](scenarios/DE-102.md)

### Hardening

- [`DG-1001-QUALITY-GATE.md`](hardening/DG-1001-QUALITY-GATE.md)
- [`DG-1002-SECURITY-REVIEW.md`](hardening/DG-1002-SECURITY-REVIEW.md)
- [`DG-1003-DOCUMENTATION-REVIEW.md`](hardening/DG-1003-DOCUMENTATION-REVIEW.md)
- [`DG-1004-CODE-FREEZE.md`](hardening/DG-1004-CODE-FREEZE.md)

### Entrega

- [`DG-1101-FINAL-DELIVERY-REVIEW.md`](delivery/DG-1101-FINAL-DELIVERY-REVIEW.md)
- [`DG-1102-DEMO-EVIDENCE-VALIDATION.md`](delivery/DG-1102-DEMO-EVIDENCE-VALIDATION.md)
- [`DG-1103-SUBMISSION-PACKAGE.md`](delivery/DG-1103-SUBMISSION-PACKAGE.md)

---

> 📚 Esta central documental foi estruturada para tornar o **AI Data Governance Agent** compreensível tanto do ponto de vista de negócio quanto de Engenharia de Software, Engenharia de Dados, Inteligência Artificial e Governança.

[⬆️ Voltar ao índice](#sumario) · [🏠 README principal](../README.md)
