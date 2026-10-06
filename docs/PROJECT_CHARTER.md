# 🎯 AI Data Governance Agent — Project Charter

Este documento define a visão, o problema, os objetivos, o escopo e os critérios de sucesso do **AI Data Governance Agent**.

O projeto está sendo desenvolvido como Challenge individual da **Imersão de Agentes de IA para Negócios — Alura + Oracle Next Education (ONE)**.

---

## 📑 Sumário

- [Visão do projeto](#visao)
- [Problema](#problema)
- [Usuários](#usuarios)
- [Objetivo](#objetivo)
- [Posicionamento](#posicionamento)
- [Escopo do MVP](#escopo)
- [Fora do escopo](#fora-escopo)
- [Ferramentas iniciais](#ferramentas)
- [Resposta estruturada](#resposta)
- [Supervisão humana](#supervisao)
- [Princípios de evidência](#evidencia)
- [Projetos de referência](#referencias)
- [Métricas de avaliação](#metricas)
- [Princípios de desenvolvimento](#desenvolvimento)
- [Critérios de sucesso](#sucesso)
- [Princípio de entrega](#entrega)

---

<a id="visao"></a>

## 🌐 1. Visão do projeto

O **AI Data Governance Agent** é uma solução de Inteligência Artificial aplicada à investigação de incidentes de dados.

Seu propósito é auxiliar profissionais de dados na organização de evidências, avaliação de problemas de Data Quality, análise de possíveis impactos de negócio e identificação de controles de governança relevantes.

O projeto busca demonstrar a aplicação integrada de:

- Engenharia de Dados;
- Inteligência Artificial;
- Data Quality;
- Data Governance;
- DataOps;
- rastreabilidade;
- explicabilidade;
- supervisão humana.

### Datas principais

| Marco | Data |
|---|---|
| Code freeze interno | **06/11/2026** |
| Entrega oficial do Challenge | **08/11/2026** |

---

<a id="problema"></a>

## 🔎 2. Problema

Incidentes de dados frequentemente são investigados a partir de informações distribuídas entre diferentes fontes, como:

- relatórios de pipelines;
- resultados de validações;
- logs;
- verificações de Data Quality;
- diferenças de reconciliação;
- regras de negócio;
- políticas de governança;
- observações de analistas.

Essa fragmentação pode tornar a investigação mais lenta e gerar avaliações inconsistentes sobre:

- severidade do incidente;
- datasets afetados;
- impacto no negócio;
- possíveis causas;
- controles de governança;
- prioridade de remediação.

O **AI Data Governance Agent** busca reduzir essa fragmentação organizando evidências e produzindo uma análise estruturada e rastreável.

O sistema possui caráter consultivo e não substitui a tomada de decisão humana em situações críticas.

---

<a id="usuarios"></a>

## 👥 3. Usuários

O público principal é formado por profissionais responsáveis pela investigação, análise ou governança de incidentes de dados.

Perfis representativos incluem:

- Data Engineer;
- Analytics Engineer;
- Data Quality Analyst;
- Data Governance Analyst;
- Data Platform Engineer;
- profissionais responsáveis por observabilidade e confiabilidade de dados.

A solução deve ser compreensível tanto para profissionais técnicos quanto para responsáveis por decisões de negócio e governança.

---

<a id="objetivo"></a>

## 🚀 4. Objetivo

Construir um fluxo assistido por IA capaz de:

1. receber um incidente de dados estruturado;
2. validar as informações de entrada;
3. organizar as evidências disponíveis;
4. analisar sinais de qualidade de dados;
5. avaliar possíveis impactos de negócio;
6. identificar políticas ou controles de governança aplicáveis;
7. produzir hipóteses de causa raiz;
8. recomendar ações de investigação ou remediação;
9. estimar o nível de confiança da análise;
10. identificar quando revisão humana é obrigatória;
11. retornar uma resposta estruturada, explicável e rastreável.

---

<a id="posicionamento"></a>

## 🧭 5. Posicionamento

O projeto foi concebido para reforçar competências relacionadas a:

- Engenharia de Dados;
- IA aplicada a negócios;
- arquitetura de agentes;
- Data Quality;
- Data Governance;
- DataOps;
- APIs;
- avaliação de sistemas de IA;
- testes automatizados;
- segurança e guardrails;
- human-in-the-loop.

O foco está em demonstrar **qualidade de engenharia e capacidade de resolver um problema real**, e não simplesmente acumular tecnologias.

---

<a id="escopo"></a>

## 📦 6. Escopo do MVP

O MVP deverá incluir:

### Backend

- Python 3.12;
- FastAPI;
- Pydantic;
- LangGraph.

### Domínio

- contratos estruturados de entrada;
- modelo de evidências;
- classificação de incidente;
- severidade;
- impacto de negócio;
- hipóteses de causa raiz;
- recomendações;
- controles de governança;
- resposta estruturada.

### Ferramentas

Quatro capacidades iniciais:

```text
quality_analyzer
business_impact_analyzer
policy_retriever
evidence_collector
```

### Inteligência Artificial

- abstração de provider;
- comportamento determinístico para testes;
- integração opcional com modelo real;
- CI independente de credenciais externas.

### Governança

- rastreabilidade de evidências;
- tratamento de evidência insuficiente;
- separação entre fatos e hipóteses;
- confidence;
- revisão humana;
- guardrails.

### Qualidade

- pytest;
- pytest-cov;
- Ruff;
- GitHub Actions;
- testes unitários;
- testes de integração;
- avaliação objetiva.

### Interface

Interface de demonstração utilizando:

```text
Node.js
Express
EJS
Vanilla JavaScript
```

---

<a id="fora-escopo"></a>

## 🧊 7. Fora do escopo antes da entrega

As seguintes tecnologias ou capacidades permanecem fora do MVP salvo necessidade explícita:

- Kubernetes;
- arquitetura multi-agent;
- infraestrutura cloud obrigatória;
- bancos relacionais complexos;
- bancos NoSQL complexos;
- Qdrant;
- Redis;
- execução de Airflow no runtime do Challenge;
- execução de Spark no runtime do Challenge;
- React;
- Next.js;
- autenticação corporativa complexa;
- IAM empresarial;
- remediação autônoma de produção;
- execução automática de ações destrutivas;
- arquitetura distribuída sem benefício demonstrável.

Essas decisões reduzem risco de implementação e ajudam a manter foco no problema principal.

---

<a id="ferramentas"></a>

## 🛠️ 8. Ferramentas iniciais

### `quality_analyzer`

Responsável por analisar evidências relacionadas à qualidade dos dados.

Exemplos:

- registros inválidos;
- relacionamentos ausentes;
- diferenças de reconciliação;
- falhas de validação;
- problemas de integridade;
- divergências de volume.

---

### `business_impact_analyzer`

Responsável por traduzir descobertas técnicas em possíveis consequências de negócio.

Deve diferenciar claramente:

- impacto confirmado;
- impacto potencial;
- impacto desconhecido.

---

### `policy_retriever`

Responsável por identificar políticas, regras ou controles de governança relacionados ao incidente.

A implementação inicial deverá permanecer simples, previsível e testável.

---

### `evidence_collector`

Responsável por coletar, normalizar e organizar as evidências utilizadas durante a análise.

Sua função é preservar a rastreabilidade entre:

```text
Evidência
   ↓
Finding
   ↓
Hipótese
   ↓
Recomendação
```

---

<a id="resposta"></a>

## 📑 9. Resposta estruturada

O contrato final deverá representar informações como:

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

Os detalhes formais são mantidos nos contratos localizados em:

```text
docs/contracts/
```

A resposta deve ser serializável, validável e adequada tanto para API quanto para interface web.

---

<a id="supervisao"></a>

## 👤 10. Supervisão humana

O agente possui caráter **consultivo**.

A revisão humana deve ser obrigatória quando houver condições de maior risco.

Exemplos:

- severidade crítica;
- impacto material de negócio;
- baixa confidence;
- evidência insuficiente;
- evidências conflitantes;
- exposição regulatória;
- problema de governança;
- problema de privacidade;
- recomendação destrutiva;
- ação irreversível;
- causa raiz altamente incerta.

O agente não deve executar automaticamente ações críticas de remediação.

### Princípio

```text
Maior risco
    ↓
Maior necessidade de supervisão humana
```

---

<a id="evidencia"></a>

## 🧾 11. Princípios de evidência e grounding

O sistema deve distinguir explicitamente entre:

- evidência observada;
- resultado de ferramenta determinística;
- hipótese;
- recomendação.

Uma hipótese gerada durante a análise não pode ser apresentada como fato confirmado sem evidência adequada.

Quando a evidência for insuficiente, o sistema deverá declarar a limitação explicitamente.

### Comportamento esperado

```text
Evidência suficiente
      ↓
Conclusão sustentada

Evidência parcial
      ↓
Conclusão qualificada

Evidência insuficiente
      ↓
Limitação explícita
      +
Revisão humana quando aplicável
```

### Princípio de rastreabilidade

Conclusões importantes devem ser associáveis às evidências utilizadas.

Isso permite responder:

- de onde veio esta informação?
- qual evidência sustenta esta conclusão?
- esta informação é observada ou inferida?
- qual o grau de confiança?
- por que revisão humana foi exigida?

---

<a id="referencias"></a>

## 🔗 12. Projetos de referência

Outros repositórios do portfólio poderão fornecer padrões técnicos, cenários ou exemplos.

Eles permanecem projetos independentes.

### `aws-lakehouse-engineering-lab`

Referência principal para:

- incidentes de Data Quality;
- cenários DE-101;
- cenários DE-102;
- investigação de divergências;
- evidências de pipeline.

### `databricks-lakehouse-data-engineering-lab`

Referência para:

- Engenharia de Dados;
- arquitetura lakehouse;
- Databricks;
- padrões de pipelines.

### `agente-ia-manuais-rh-rag`

Referência para:

- FastAPI;
- RAG;
- guardrails;
- rastreabilidade de fontes;
- comportamento com evidência insuficiente.

### `edudocs-ai-agent-oci`

Referência para:

- LangGraph;
- abstração de provider;
- avaliação;
- métricas;
- comportamento determinístico.

### `growth_equestre_hackathon_2026`

Referência para:

- Node.js;
- Express;
- EJS;
- experiência de demonstração.

Nenhum desses repositórios deverá ser transformado diretamente no projeto atual.

---

<a id="metricas"></a>

## 📊 13. Métricas de avaliação

As métricas inicialmente planejadas são:

| Métrica | Objetivo |
|---|---|
| `schema_valid_rate` | Conformidade das respostas com o schema |
| `severity_accuracy` | Precisão da classificação de severidade |
| `evidence_traceability_rate` | Rastreabilidade das conclusões |
| `unsupported_rejection_rate` | Rejeição de afirmações sem suporte |
| `human_review_accuracy` | Precisão das decisões de revisão humana |
| `tool_execution_success_rate` | Sucesso das ferramentas |
| `response_latency` | Tempo de resposta |
| `test_pass_rate` | Estabilidade da suíte de testes |

As definições exatas serão mantidas em:

```text
docs/evaluation/
```

---

<a id="desenvolvimento"></a>

## ⚙️ 14. Princípios de desenvolvimento

O desenvolvimento segue um processo incremental:

```text
Planejar
   ↓
Definir contrato
   ↓
Definir critérios de aceite
   ↓
Implementar
   ↓
Testar
   ↓
Executar quality gates
   ↓
Revisar
   ↓
Versionar
```

### Diretrizes

As tarefas devem, sempre que possível:

- possuir escopo pequeno;
- ter comportamento previsível;
- ter testes automatizados;
- evitar acoplamento desnecessário;
- preservar rastreabilidade;
- manter CI determinística;
- evitar dependência obrigatória de serviços externos.

Tarefas grandes devem ser divididas antes da implementação quando isso reduzir risco.

---

<a id="sucesso"></a>

## ✅ 15. Critérios de sucesso do MVP

O MVP será considerado bem-sucedido quando:

- um incidente válido puder ser submetido ao sistema;
- os contratos forem validados corretamente;
- as ferramentas necessárias forem executadas;
- a resposta final respeitar o schema;
- evidências puderem ser rastreadas;
- conclusões sem suporte forem rejeitadas ou qualificadas;
- situações críticas exigirem revisão humana;
- cenários determinísticos funcionarem sem modelo externo;
- testes automatizados forem aprovados;
- Ruff for aprovado;
- CI estiver aprovada;
- pelo menos um incidente representativo puder ser demonstrado de ponta a ponta;
- a solução puder ser explicada claramente em termos técnicos e de negócio.

---

<a id="entrega"></a>

## 🏁 16. Princípio de entrega

O projeto prioriza:

```text
Confiabilidade
      +
Explicabilidade
      +
Testabilidade
      +
Rastreabilidade
      +
Demonstrabilidade
```

sobre complexidade arquitetural sem benefício concreto.

Qualidade profissional será demonstrada por:

- decisões claras;
- arquitetura coerente;
- contratos explícitos;
- testes;
- CI;
- documentação;
- métricas;
- rastreabilidade;
- governança.

---

> 🎯 O objetivo do **AI Data Governance Agent** não é substituir especialistas, mas oferecer uma camada estruturada de análise que transforme evidências fragmentadas em informações rastreáveis e úteis para tomada de decisão.