# 🗺️ AI Data Governance Agent — Roadmap

Este documento apresenta a evolução planejada do **AI Data Governance Agent**, organizada em fases incrementais.

O objetivo do roadmap é preservar foco, reduzir risco de implementação e garantir que cada etapa produza entregas verificáveis antes do avanço para a próxima.

---

<a id="sumario"></a>

## 📑 Sumário

- [Datas principais](#datas)
- [Princípios do roadmap](#principios)
- [Fase 0 — Planejamento e Bootstrap](#fase-0)
- [Fase 1 — Modelos e Contratos de Domínio](#fase-1)
- [Fase 2 — Ferramentas Determinísticas](#fase-2)
- [Fase 3 — Abstração de Provedores](#fase-3)
- [Fase 4 — Workflow com LangGraph](#fase-4)
- [Fase 5 — Guardrails e Governança](#fase-5)
- [Fase 6 — API FastAPI](#fase-6)
- [Fase 7 — Framework de Avaliação](#fase-7)
- [Fase 8 — Interface Web](#fase-8)
- [Fase 9 — Cenários Representativos](#fase-9)
- [Fase 10 — Hardening Final](#fase-10)
- [Fase 11 — Preparação da Entrega](#fase-11)
- [Regra de controle de escopo](#controle-escopo)

---

<a id="datas"></a>

## 📅 Datas principais

| Marco | Data |
|---|---|
| Code freeze efetivo | **08/10/2026** |
| Entrega oficial do Challenge | **08/11/2026** |

O período após o code freeze será reservado para:

- validação final;
- revisão documental;
- limpeza do repositório;
- preparação da demonstração;
- captura de evidências;
- revisão de links;
- ensaio da apresentação;
- submissão final.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="principios"></a>

## 🧭 Princípios do roadmap

A evolução do projeto seguirá os seguintes princípios:

- construir primeiro a base;
- definir contratos antes da orquestração;
- implementar componentes determinísticos antes da IA generativa;
- testar cada camada isoladamente;
- preservar rastreabilidade;
- manter CI independente de serviços externos;
- limitar o escopo;
- priorizar demonstrabilidade e qualidade.

Fluxo geral:

```text
Planejamento
     ↓
Contratos
     ↓
Modelos
     ↓
Ferramentas determinísticas
     ↓
Providers
     ↓
Orquestração
     ↓
Guardrails
     ↓
API
     ↓
Avaliação
     ↓
Interface
     ↓
Demonstração
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-0"></a>

# ✅ Fase 0 — Planejamento e Bootstrap

## Objetivo

Criar uma fundação reproduzível e definir o escopo inicial antes da implementação funcional.

## Entregas

- estrutura do repositório;
- Python 3.12;
- ambiente virtual;
- `pyproject.toml`;
- pytest;
- Ruff;
- CI inicial;
- Project Charter;
- roadmap;
- backlog;
- ADR inicial;
- contratos conceituais;
- README inicial.

## Status

**✅ CONCLUÍDA**

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-1"></a>

# 📦 Fase 1 — Modelos e Contratos de Domínio

## Objetivo

Transformar os contratos conceituais em estruturas de domínio explícitas, consistentes e testáveis.

## Entregas previstas

- `IncidentInput`;
- `Evidence`;
- enums de domínio;
- severidade;
- classificação;
- `BusinessImpact`;
- `GovernanceControl`;
- `RecommendedAction`;
- `RootCauseHypothesis`;
- `AgentResponse`;
- representação de confidence;
- regras determinísticas de revisão humana;
- fixtures de incidentes;
- testes de validação.

## Diretriz

Nenhuma integração obrigatória com modelo real é necessária nesta fase.

## Resultado esperado

Ao final da fase, os principais contratos deverão estar:

- implementados;
- validados;
- testados;
- serializáveis;
- documentados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-2"></a>

# 🛠️ Fase 2 — Ferramentas Determinísticas

## Objetivo

Implementar capacidades analíticas independentes da camada de orquestração.

## Ferramentas iniciais

### `evidence_collector`

Responsável por organizar e preservar as evidências do incidente.

### `quality_analyzer`

Responsável por analisar sinais de qualidade dos dados.

### `business_impact_analyzer`

Responsável por avaliar possíveis impactos de negócio.

### `policy_retriever`

Responsável por recuperar políticas ou controles de governança aplicáveis.

## Requisitos

Cada ferramenta deverá possuir:

- entrada explícita;
- saída explícita;
- comportamento previsível;
- tratamento de erro;
- rastreabilidade;
- testes unitários.

## Resultado esperado

As ferramentas devem poder ser executadas e testadas sem LangGraph e sem modelo externo.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-3"></a>

# 🔌 Fase 3 — Abstração de Provedores

## Objetivo

Separar comportamento dependente de modelos da lógica principal de negócio.

## Entregas previstas

- interface ou protocolo de provider;
- provider determinístico para testes;
- provider real opcional;
- configuração por variáveis de ambiente;
- tratamento seguro de credenciais ausentes.

## Princípio arquitetural

```text
Lógica de negócio
       │
       ▼
Provider Interface
       │
   ┌───┴────┐
   │        │
Teste      Real
```

## Requisitos

A CI deverá permanecer funcional:

- sem chave de API;
- sem chamadas externas obrigatórias;
- com comportamento reproduzível.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-4"></a>

# 🧠 Fase 4 — Workflow com LangGraph

## Objetivo

Orquestrar a análise do incidente de forma explícita e controlada.

## Fluxo inicial

```text
Validar incidente
       ↓
Coletar evidências
       ↓
Analisar Data Quality
       ↓
Avaliar impacto de negócio
       ↓
Consultar governança
       ↓
Construir hipóteses
       ↓
Gerar recomendações
       ↓
Avaliar confidence
       ↓
Determinar revisão humana
       ↓
Construir AgentResponse
```

## Entregas previstas

- estado do grafo;
- nodes;
- transições;
- tratamento de falhas;
- integração das ferramentas;
- integração do provider;
- testes do workflow.

## Diretriz

A primeira versão permanecerá com **arquitetura de agente único**.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-5"></a>

# 🛡️ Fase 5 — Guardrails e Governança

## Objetivo

Tornar o comportamento do agente mais seguro, rastreável e explícito quanto à incerteza.

## Entregas previstas

- rejeição de afirmações sem suporte;
- comportamento com evidência insuficiente;
- validação de rastreabilidade;
- regras de confidence;
- revisão humana obrigatória;
- separação entre fatos e hipóteses;
- respostas de falha estruturadas.

## Princípio

```text
Sem evidência suficiente
        ↓
Não afirmar como fato
        ↓
Qualificar ou rejeitar
        ↓
Solicitar revisão humana quando necessário
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-6"></a>

# 🌐 Fase 6 — API FastAPI

## Objetivo

Disponibilizar o workflow por meio de um contrato HTTP estável.

## Entregas previstas

### Health check

```text
GET /health
```

### Análise de incidente

```text
POST /api/v1/incidents/analyze
```

## Requisitos

- validação de request;
- execução do workflow;
- resposta estruturada;
- tratamento de erros;
- testes de API;
- documentação OpenAPI.

## Resultado esperado

A aplicação deverá poder ser consumida por clientes externos de forma previsível.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-7"></a>

# 📊 Fase 7 — Framework de Avaliação

## Objetivo

Medir o comportamento da solução de forma objetiva.

## Métricas iniciais

- `schema_valid_rate`;
- `severity_accuracy`;
- `evidence_traceability_rate`;
- `unsupported_rejection_rate`;
- `human_review_accuracy`;
- `tool_execution_success_rate`;
- `response_latency`;
- `test_pass_rate`.

## Entregas previstas

- fixtures de avaliação;
- cenários controlados;
- expected outcomes;
- runner de avaliação;
- cálculo das métricas;
- relatório de resultados.

## Resultado esperado

A avaliação deverá ser:

- reproduzível;
- interpretável;
- adequada para demonstração;
- independente de comportamento imprevisível sempre que possível.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-8"></a>

# 🖥️ Fase 8 — Interface Web

## Objetivo

Criar uma experiência visual profissional para demonstração da solução.

## Stack principal

- Node.js;
- Express;
- EJS;
- Vanilla JavaScript.

## Capacidades previstas

- inserir incidente;
- carregar cenário predefinido;
- enviar análise;
- visualizar classificação;
- visualizar severidade;
- exibir resumo executivo;
- exibir evidências;
- exibir impacto de negócio;
- exibir hipóteses;
- exibir recomendações;
- exibir controles de governança;
- exibir confidence;
- destacar revisão humana.

## Diretriz

A interface deve privilegiar:

- clareza;
- legibilidade;
- hierarquia visual;
- demonstração do valor do projeto.

Streamlit permanece apenas como opção de contingência.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-9"></a>

# 🎬 Fase 9 — Cenários Representativos

## Objetivo

Demonstrar o agente com situações próximas de problemas reais de Engenharia de Dados.

## Cenários iniciais

### Cenário 1

Inspirado em padrões do incidente **DE-101** do repositório:

```text
aws-lakehouse-engineering-lab
```

### Cenário 2

Inspirado em padrões do incidente **DE-102**.

### Cenários sintéticos

Também poderão ser utilizados casos específicos para avaliar:

- evidência insuficiente;
- evidência conflitante;
- baixa severidade;
- severidade crítica;
- afirmação sem suporte;
- necessidade de revisão humana.

## Regra

Os repositórios de referência permanecem independentes e inalterados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-10"></a>

# 🔒 Fase 10 — Hardening Final

## Objetivo

Preparar o projeto para o code freeze.

## Atividades

- execução completa do pytest;
- validação com Ruff;
- validação da CI;
- revisão de dependências;
- revisão da documentação;
- remoção de código morto;
- remoção de arquivos temporários;
- revisão de segredos;
- instalação em ambiente limpo;
- validação de reprodutibilidade;
- revisão dos links;
- ensaio da demonstração.

## Quality gates

```bash
python -m pip check
ruff check .
ruff format --check .
pytest
```

## Data efetiva

**08/10/2026**

O code freeze foi antecipado em relação à meta interna original de **06/11/2026**.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-11"></a>

# 🏁 Fase 11 — Preparação da Entrega

## Período

**08/10/2026 a 08/11/2026**

A preparação da entrega foi antecipada após o code freeze efetivo em **08/10/2026**.

## Objetivo

Preparar a entrega final sem introduzir complexidade nova.

## Atividades

- revisão final do README;
- revisão do índice documental;
- validação dos screenshots;
- preparação da narrativa;
- validação da demonstração;
- revisão do repositório público;
- validação dos links;
- preparação da submissão.

## Regra

Nenhuma funcionalidade significativa deverá ser iniciada nesta fase.

Somente correções necessárias para estabilidade ou apresentação deverão ser realizadas.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="controle-escopo"></a>

# 🧭 Regra de controle de escopo

Uma nova funcionalidade deve entrar no roadmap anterior à entrega somente quando melhorar materialmente pelo menos um destes aspectos:

- aderência aos requisitos do Challenge;
- demonstrabilidade;
- confiabilidade;
- governança;
- rastreabilidade;
- explicabilidade;
- segurança;
- qualidade da avaliação;
- valor profissional do portfólio.

Caso contrário, deverá ser adiada.

---

## 🧊 Itens deliberadamente adiados

Antes da entrega, não fazem parte do escopo principal:

- Kubernetes;
- arquitetura multi-agent;
- Redis;
- Qdrant;
- Airflow no runtime;
- Spark no runtime;
- React;
- Next.js;
- IAM corporativo;
- infraestrutura distribuída;
- remediação autônoma;
- escalabilidade empresarial completa.

Esses itens poderão ser revisitados após o Challenge caso exista benefício concreto.

---

## 📈 Visão resumida

```text
FASE 0   ✅ Planejamento e Bootstrap
FASE 1   ✅ Modelos e Contratos
FASE 2   ✅ Ferramentas Determinísticas
FASE 3   ✅ Providers
FASE 4   ✅ LangGraph
FASE 5   ✅ Guardrails
FASE 6   ✅ FastAPI
FASE 7   ✅ Avaliação
FASE 8   ✅ Interface Web
FASE 9   ✅ Cenários
FASE 10  ✅ Hardening
FASE 11  🚧 Entrega
```

---

> 🗺️ O roadmap do **AI Data Governance Agent** prioriza evolução incremental, qualidade técnica, rastreabilidade e controle de escopo até a entrega final do Challenge.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)
