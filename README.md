# 🤖 AI Data Governance Agent

[![CI](https://github.com/brodyandre/ai-data-governance-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/brodyandre/ai-data-governance-agent/actions/workflows/ci.yml)

Agente de IA para análise estruturada de incidentes de dados, com foco em **Data Quality, impacto de negócio, governança, rastreabilidade de evidências e supervisão humana**.

Este repositório está sendo desenvolvido como projeto individual do Challenge da **Imersão de Agentes de IA para Negócios — Alura + Oracle Next Education (ONE)**.

---

<a id="sumario"></a>

## 📚 Sumário

- [Visão geral](#visao-geral)
- [Problema](#problema)
- [Objetivos](#objetivos)
- [Como a solução funciona](#como-funciona)
- [Ferramentas do agente](#ferramentas)
- [Resposta estruturada](#resposta-estruturada)
- [Supervisão humana](#supervisao-humana)
- [Princípios de evidência](#principios-evidencia)
- [Arquitetura e tecnologias](#arquitetura)
- [Estrutura do projeto](#estrutura)
- [Desenvolvimento local](#desenvolvimento-local)
- [Qualidade e testes](#qualidade)
- [Avaliação](#avaliacao)
- [Roadmap](#roadmap)
- [Documentação](#documentacao)
- [Projetos de referência](#projetos-referencia)
- [Princípios de desenvolvimento](#principios-desenvolvimento)
- [Prazo do Challenge](#prazo)
- [Autor](#autor)

---

<a id="visao-geral"></a>

## 🎯 Visão geral

O **AI Data Governance Agent** tem como objetivo auxiliar profissionais de dados na investigação de incidentes por meio da organização de evidências técnicas e de negócio.

A solução deverá produzir análises estruturadas, rastreáveis e explícitas quanto ao nível de confiança, sem substituir a decisão humana em situações críticas.

O projeto combina conceitos de:

- Engenharia de Dados;
- Inteligência Artificial aplicada a negócios;
- Data Quality;
- Data Governance;
- DataOps;
- observabilidade;
- segurança aplicada à IA;
- human-in-the-loop.

### 📌 Status atual

| Item | Status |
|---|---|
| Fase 0 — Planejamento e Bootstrap | ✅ Concluída |
| Fase 1 — Modelos e Contratos de Domínio | 🚧 Em andamento |
| Infraestrutura inicial | ✅ Concluída |
| CI com GitHub Actions | ✅ Operacional |
| Contratos conceituais | ✅ Definidos |
| Implementação do agente | ⏳ Planejada |
| Interface web | ⏳ Planejada |

> O projeto está sendo construído de forma incremental, com contratos de domínio, testes e critérios de aceite definidos antes da implementação das camadas de maior complexidade.

[⬆️ Voltar ao índice](#sumario)

---

<a id="problema"></a>

## 🔎 Problema

Incidentes de dados normalmente são investigados a partir de informações fragmentadas, como:

- relatórios de pipelines;
- resultados de validações;
- diferenças de reconciliação;
- logs;
- verificações de Data Quality;
- regras de negócio;
- políticas de governança;
- observações de analistas.

Essa fragmentação pode tornar a investigação mais lenta e produzir avaliações inconsistentes sobre:

- severidade;
- impacto no negócio;
- causa raiz;
- consumidores afetados;
- controles de governança;
- prioridade de remediação.

O projeto busca organizar essas informações e transformá-las em uma análise **estruturada, explicável e auditável**.

[⬆️ Voltar ao índice](#sumario)

---

<a id="objetivos"></a>

## 🚀 Objetivos

O fluxo planejado deverá ser capaz de:

1. receber um incidente estruturado;
2. organizar as evidências disponíveis;
3. analisar sinais de Data Quality;
4. avaliar possíveis impactos de negócio;
5. consultar controles e políticas de governança;
6. produzir hipóteses de causa raiz;
7. recomendar próximos passos;
8. estimar o nível de confiança da análise;
9. identificar situações que exigem revisão humana;
10. retornar uma resposta estruturada e rastreável.

[⬆️ Voltar ao índice](#sumario)

---

<a id="como-funciona"></a>

## 🔄 Como a solução funciona

Fluxo conceitual do MVP:

```text
Incidente
   │
   ▼
Validação do contrato
   │
   ▼
Coleta e organização de evidências
   │
   ▼
Análise de Data Quality
   │
   ▼
Avaliação de impacto de negócio
   │
   ▼
Consulta a controles de governança
   │
   ▼
Hipóteses e recomendações
   │
   ▼
Regras de supervisão humana
   │
   ▼
Resposta estruturada e rastreável
```

O fluxo será orquestrado com **LangGraph**, mantendo inicialmente uma arquitetura de agente único.

A proposta é combinar componentes determinísticos com capacidades de IA sem transferir decisões críticas exclusivamente para o modelo.

[⬆️ Voltar ao índice](#sumario)

---

<a id="ferramentas"></a>

## 🛠️ Ferramentas do agente

O MVP prevê quatro ferramentas determinísticas principais:

| Ferramenta | Responsabilidade |
|---|---|
| `quality_analyzer` | Avaliar sinais e problemas relacionados à qualidade dos dados |
| `business_impact_analyzer` | Relacionar problemas técnicos a possíveis impactos de negócio |
| `policy_retriever` | Recuperar políticas e controles de governança aplicáveis |
| `evidence_collector` | Organizar e preservar a rastreabilidade das evidências |

A separação dessas responsabilidades permite testar cada capacidade de forma independente e manter o fluxo mais previsível.

[⬆️ Voltar ao índice](#sumario)

---

<a id="resposta-estruturada"></a>

## 📦 Resposta estruturada

A resposta do agente será representada por um contrato estruturado contendo campos como:

```text
incident_id
classification
severity
executive_summary
evidence
business_impact
root_cause_hypotheses
recommended_actions
governance_controls
confidence
human_review_required
human_review_reasons
```

Os contratos de entrada e saída são definidos antes da implementação para reduzir ambiguidades e manter estabilidade entre as diferentes camadas da aplicação.

[⬆️ Voltar ao índice](#sumario)

---

<a id="supervisao-humana"></a>

## 👤 Supervisão humana

O agente possui caráter **consultivo**.

Situações de maior risco deverão exigir revisão humana, incluindo casos de:

- severidade crítica;
- impacto material de negócio;
- baixa confiança;
- evidências insuficientes;
- evidências conflitantes;
- possível exposição regulatória;
- possível violação de governança;
- impacto de privacidade;
- recomendações destrutivas ou irreversíveis.

O agente não executará automaticamente ações críticas de remediação.

A decisão final permanece sob responsabilidade de uma pessoa ou equipe devidamente autorizada.

[⬆️ Voltar ao índice](#sumario)

---

<a id="principios-evidencia"></a>

## 🧾 Princípios de evidência

A solução diferencia explicitamente:

```text
Evidência observada
        ↓
Resultado determinístico
        ↓
Hipótese
        ↓
Recomendação
```

Uma hipótese não deve ser apresentada como fato confirmado sem evidência que a sustente.

Quando as informações forem insuficientes, o sistema deverá declarar essa limitação em vez de produzir evidências inexistentes.

A rastreabilidade é um requisito central do projeto.

O objetivo é permitir perguntas como:

- qual evidência sustenta esta conclusão?
- de onde essa evidência veio?
- a conclusão foi observada, calculada ou inferida?
- qual é o nível de confiança?
- por que uma revisão humana foi exigida?

[⬆️ Voltar ao índice](#sumario)

---

<a id="arquitetura"></a>

## 🏗️ Arquitetura e tecnologias

### Backend

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Linguagem principal |
| FastAPI | API HTTP |
| Pydantic | Contratos e validação |
| LangGraph | Orquestração do fluxo do agente |

### Qualidade e testes

| Tecnologia | Uso |
|---|---|
| pytest | Testes automatizados |
| pytest-cov | Cobertura de testes |
| Ruff | Lint e formatação |
| GitHub Actions | Integração contínua |

### Inteligência Artificial

A arquitetura prevê uma camada de abstração para provedores de modelos.

Os testes automatizados e a integração contínua deverão funcionar de forma determinística e sem dependência obrigatória de um modelo externo.

A integração com um modelo real será utilizada apenas nos cenários em que essa capacidade seja necessária.

### Interface web

Stack planejada:

```text
Node.js
Express
EJS
Vanilla JavaScript
```

O objetivo é produzir uma interface limpa e profissional sem introduzir complexidade desnecessária no frontend.

[⬆️ Voltar ao índice](#sumario)

---

<a id="estrutura"></a>

## 📁 Estrutura do projeto

```text
ai-data-governance-agent/
├── .github/
│   └── workflows/
├── docs/
│   ├── adrs/
│   ├── contracts/
│   ├── evaluation/
│   ├── BACKLOG.md
│   ├── PROJECT_CHARTER.md
│   ├── README.md
│   └── ROADMAP.md
├── src/
│   └── ai_data_governance_agent/
├── tests/
├── web/
├── pyproject.toml
└── README.md
```

As principais responsabilidades estão separadas entre código, testes, documentação, contratos e interface de demonstração.

[⬆️ Voltar ao índice](#sumario)

---

<a id="desenvolvimento-local"></a>

## 💻 Desenvolvimento local

### Pré-requisitos

- Python 3.12;
- Git;
- Linux, WSL2 ou ambiente equivalente.

### 1. Clonar o repositório

```bash
git clone https://github.com/brodyandre/ai-data-governance-agent.git
cd ai-data-governance-agent
```

### 2. Criar o ambiente virtual

```bash
python3.12 -m venv .venv
```

### 3. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

### 4. Instalar o projeto

```bash
python -m pip install -e ".[dev]"
```

### 5. Validar as dependências

```bash
python -m pip check
```

[⬆️ Voltar ao índice](#sumario)

---

<a id="qualidade"></a>

## ✅ Qualidade e testes

O projeto utiliza quality gates locais e automáticos.

### Validar dependências

```bash
python -m pip check
```

### Executar lint

```bash
ruff check .
```

### Validar formatação

```bash
ruff format --check .
```

### Executar testes

```bash
pytest
```

A integração contínua executa os principais quality gates automaticamente por meio do **GitHub Actions**.

### Estado atual

```text
pip check             ✅
Ruff lint             ✅
Ruff format           ✅
pytest                ✅
GitHub Actions CI     ✅
```

[⬆️ Voltar ao índice](#sumario)

---

<a id="avaliacao"></a>

## 📊 Avaliação

O projeto prevê avaliação objetiva do comportamento da solução.

As métricas planejadas incluem:

| Métrica | Objetivo |
|---|---|
| `schema_valid_rate` | Validar conformidade das respostas |
| `severity_accuracy` | Avaliar classificação de severidade |
| `evidence_traceability_rate` | Medir rastreabilidade das conclusões |
| `unsupported_rejection_rate` | Medir rejeição de conclusões sem suporte |
| `human_review_accuracy` | Avaliar decisões de revisão humana |
| `tool_execution_success_rate` | Medir execução das ferramentas |
| `response_latency` | Avaliar latência |
| `test_pass_rate` | Acompanhar estabilidade dos testes |

As definições detalhadas serão mantidas em:

```text
docs/evaluation/
```

A avaliação deverá permanecer reproduzível e, sempre que possível, independente de serviços externos.

[⬆️ Voltar ao índice](#sumario)

---

<a id="roadmap"></a>

## 🗺️ Roadmap

O desenvolvimento foi dividido em fases progressivas:

```text
0   Planejamento e Bootstrap
1   Modelos e Contratos de Domínio
2   Ferramentas Determinísticas
3   Abstração de Provedores
4   Workflow LangGraph
5   Guardrails e Governança
6   API FastAPI
7   Framework de Avaliação
8   Interface Web
9   Cenários Representativos
10  Hardening Final
11  Preparação da Entrega
```

A visão completa está disponível em:

➡️ [`docs/ROADMAP.md`](docs/ROADMAP.md)

[⬆️ Voltar ao índice](#sumario)

---

<a id="documentacao"></a>

## 📚 Documentação

A documentação técnica e de projeto possui um índice central em:

### ➡️ [`docs/README.md`](docs/README.md)

Principais documentos:

| Documento | Conteúdo |
|---|---|
| [`PROJECT_CHARTER.md`](docs/PROJECT_CHARTER.md) | Visão, objetivos, escopo e critérios de sucesso |
| [`ROADMAP.md`](docs/ROADMAP.md) | Fases e estratégia de desenvolvimento |
| [`BACKLOG.md`](docs/BACKLOG.md) | Itens de implementação e critérios de aceite |
| [`DEMO_NARRATIVE.md`](docs/demo/DEMO_NARRATIVE.md) | Narrativa oficial da demonstração do Challenge |
| [`LIVE_DEMO_RUNBOOK.md`](docs/demo/LIVE_DEMO_RUNBOOK.md) | Execução reproduzível da demonstração ao vivo |
| [`PRESENTATION_SCRIPT.md`](docs/demo/PRESENTATION_SCRIPT.md) | Roteiro de apresentação e fala curta |
| [`ADR-001`](docs/adrs/ADR-001-project-scope-and-stack.md) | Decisão inicial de arquitetura |
| [`INCIDENT_INPUT.md`](docs/contracts/INCIDENT_INPUT.md) | Contrato conceitual de entrada |
| [`AGENT_RESPONSE.md`](docs/contracts/AGENT_RESPONSE.md) | Contrato conceitual da resposta |
| [`DOMAIN_ENUMS.md`](docs/contracts/DOMAIN_ENUMS.md) | Valores normalizados de domínio |
| [`EVIDENCE_MODEL.md`](docs/contracts/EVIDENCE_MODEL.md) | Contrato do modelo de evidência |
| [`SEVERITY_AND_HUMAN_REVIEW.md`](docs/contracts/SEVERITY_AND_HUMAN_REVIEW.md) | Regras de severidade e supervisão humana |

A documentação do projeto utiliza **português brasileiro** como idioma principal.

Nomes de classes, campos, funções, métricas e componentes técnicos permanecem em inglês quando fazem parte dos contratos de software.

[⬆️ Voltar ao índice](#sumario)

---

<a id="projetos-referencia"></a>

## 🔗 Projetos de referência

Alguns padrões técnicos e cenários utilizados neste projeto têm origem em experimentos independentes presentes em outros repositórios do portfólio:

- `aws-lakehouse-engineering-lab`;
- `databricks-lakehouse-data-engineering-lab`;
- `agente-ia-manuais-rh-rag`;
- `edudocs-ai-agent-oci`;
- `growth_equestre_hackathon_2026`.

Esses projetos permanecem independentes.

Os repositórios de referência podem contribuir com:

- padrões de Engenharia de Dados;
- cenários de Data Quality;
- arquitetura lakehouse;
- RAG;
- guardrails;
- avaliação;
- FastAPI;
- LangGraph;
- experiência de demonstração.

[⬆️ Voltar ao índice](#sumario)

---

<a id="principios-desenvolvimento"></a>

## 🧭 Princípios de desenvolvimento

O projeto segue um fluxo incremental:

```text
Planejamento
   ↓
Critérios de aceite
   ↓
Implementação com escopo controlado
   ↓
Testes e validação
   ↓
Revisão
   ↓
Versionamento
   ↓
Próxima entrega
```

As decisões priorizam:

- simplicidade;
- rastreabilidade;
- testabilidade;
- segurança;
- explicabilidade;
- baixo acoplamento;
- comportamento determinístico sempre que aplicável;
- controle de escopo.

O projeto prioriza uma solução **confiável, demonstrável e bem documentada** em vez de complexidade arquitetural sem benefício concreto.

[⬆️ Voltar ao índice](#sumario)

---

<a id="prazo"></a>

## 📅 Prazo do Challenge

| Marco | Data |
|---|---|
| Code freeze interno | **06/11/2026** |
| Entrega oficial | **08/11/2026** |

O período após o code freeze será reservado para:

- validação final;
- revisão da documentação;
- limpeza do repositório;
- preparação da demonstração;
- revisão da apresentação;
- validação dos links;
- preparação da submissão final.

[⬆️ Voltar ao índice](#sumario)

---

<a id="autor"></a>

## 👨‍💻 Autor

**Luiz André de Souza**

Projeto desenvolvido como parte do portfólio profissional em:

- Engenharia de Dados;
- Inteligência Artificial aplicada a negócios;
- Data Quality;
- Governança de Dados.

---

> 🤖 **AI Data Governance Agent** — transformando evidências fragmentadas de incidentes de dados em análises estruturadas, rastreáveis e orientadas à governança.

[⬆️ Voltar ao índice](#sumario)
