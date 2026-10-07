# 📋 AI Data Governance Agent — Backlog de Desenvolvimento

Este documento organiza as entregas planejadas do **AI Data Governance Agent** em unidades incrementais, testáveis e alinhadas ao escopo do Challenge.

O backlog complementa o [`ROADMAP.md`](ROADMAP.md), transformando cada fase do projeto em tarefas objetivas com prioridade, complexidade e critérios claros de aceite.

---

<a id="sumario"></a>

## 📑 Sumário

- [Informações da entrega](#informacoes-entrega)
- [Prioridades](#prioridades)
- [Complexidade das tarefas](#complexidade)
- [Fase 0 — Planejamento e Bootstrap](#fase-0)
- [Fase 1 — Modelos e Contratos de Domínio](#fase-1)
- [Fase 2 — Ferramentas Determinísticas](#fase-2)
- [Fase 3 — Abstração de Provedores](#fase-3)
- [Fase 4 — Workflow do Agente](#fase-4)
- [Fase 5 — Guardrails](#fase-5)
- [Fase 6 — FastAPI](#fase-6)
- [Fase 7 — Avaliação](#fase-7)
- [Fase 8 — Interface Web](#fase-8)
- [Fase 9 — Demonstração do Challenge](#fase-9)
- [Fase 10 — Hardening Final](#fase-10)
- [Itens adiados](#itens-adiados)
- [Regra de controle do backlog](#regra-backlog)

---

<a id="informacoes-entrega"></a>

## 📅 Informações da entrega

| Marco | Data |
|---|---|
| Code freeze interno | **06/11/2026** |
| Entrega oficial do Challenge | **08/11/2026** |

O período posterior ao code freeze deve ser reservado para:

- validação final;
- correções bloqueadoras;
- revisão documental;
- preparação da demonstração;
- captura de evidências;
- ensaio da apresentação;
- submissão final.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="prioridades"></a>

## 🎯 Prioridades

| Prioridade | Significado |
|---|---|
| `P0` | Obrigatório para o MVP do Challenge |
| `P1` | Importante para qualidade profissional e demonstração |
| `P2` | Melhoria relevante caso haja tempo disponível |
| `P3` | Pós-Challenge ou melhoria opcional |

Uma tarefa `P0` deve ser tratada antes de funcionalidades opcionais.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="complexidade"></a>

## 🧩 Complexidade das tarefas

Cada tarefa de implementação é classificada previamente para auxiliar no controle de escopo.

### BAIXA

Alteração:

- pequena;
- localizada;
- com comportamento claramente definido;
- com baixo risco arquitetural.

### MÉDIA

Alteração que normalmente envolve:

- múltiplos modelos;
- regras de negócio;
- integração entre componentes;
- testes mais abrangentes;
- validação de contratos.

### ALTA

Alteração que envolve:

- forte impacto arquitetural;
- múltiplas camadas;
- alto risco de regressão;
- grande quantidade de decisões interdependentes.

Sempre que possível, tarefas de complexidade `ALTA` devem ser divididas em entregas menores.

### NÃO APLICÁVEL

Usado para atividades essencialmente:

- documentais;
- administrativas;
- de planejamento;
- de validação manual.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-0"></a>

# ✅ Fase 0 — Planejamento e Bootstrap

Objetivo: estabelecer uma fundação reproduzível antes do início da implementação funcional.

---

## DG-001 — Bootstrap do repositório

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ✅ CONCLUÍDO

### Escopo

- criar estrutura inicial do repositório;
- inicializar Git;
- configurar Python 3.12;
- criar `.venv`;
- configurar layout `src`;
- configurar pytest;
- configurar Ruff;
- instalar dependências iniciais.

### Critérios de aceite

- Python 3.12 operacional;
- ambiente virtual funcional;
- instalação editável bem-sucedida;
- `pip check` aprovado;
- Ruff aprovado;
- pytest aprovado.

---

## DG-002 — Project Charter

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ✅ CONCLUÍDO

### Escopo

Definir:

- problema;
- usuários;
- objetivos;
- MVP;
- não escopo;
- supervisão humana;
- princípios de evidência;
- métricas de avaliação.

### Critérios de aceite

- `docs/PROJECT_CHARTER.md` existente;
- escopo explícito;
- não escopo explícito;
- critérios de sucesso documentados.

---

## DG-003 — Roadmap do projeto

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- fases documentadas;
- code freeze documentado;
- período final de entrega documentado;
- controle de escopo definido.

---

## DG-004 — Decisão inicial de arquitetura

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ✅ CONCLUÍDO

### Entrega

`docs/adrs/ADR-001-project-scope-and-stack.md`

### Critérios de aceite

- stack principal registrada;
- tecnologias deliberadamente excluídas documentadas;
- justificativa arquitetural explícita;
- trade-offs documentados.

---

## DG-005 — Contratos iniciais de domínio

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ✅ CONCLUÍDO

### Entregas

- `docs/contracts/INCIDENT_INPUT.md`;
- `docs/contracts/AGENT_RESPONSE.md`;
- `docs/contracts/SEVERITY_AND_HUMAN_REVIEW.md`.

### Critérios de aceite

- contrato conceitual de entrada definido;
- contrato conceitual de saída definido;
- níveis de severidade definidos;
- critérios de revisão humana definidos;
- princípios de rastreabilidade explícitos.

---

## DG-006 — Bootstrap do GitHub Actions

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ✅ CONCLUÍDO

### Escopo

Criar workflow de CI para:

- Python 3.12;
- instalação do projeto;
- validação de dependências;
- Ruff lint;
- validação de formatação;
- pytest.

### Critérios de aceite

- workflow executa em `push`;
- workflow está configurado para `pull_request`;
- CI não exige credenciais de modelos externos;
- CI aprovada na `main`.

---

## DG-007 — Publicação inicial do repositório

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ✅ CONCLUÍDO

### Escopo

- criar repositório no GitHub;
- realizar commit inicial;
- publicar `main`;
- validar CI;
- validar README.

### Critérios de aceite

- repositório público disponível;
- working tree limpa;
- `main` sincronizada;
- CI aprovada.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-1"></a>

# 🚧 Fase 1 — Modelos e Contratos de Domínio

Objetivo: transformar os contratos conceituais em estruturas de domínio consistentes e testáveis.

---

## DG-101 — Enums de severidade e classificação

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ✅ CONCLUÍDO

### Escopo

Implementar valores normalizados para:

- severity;
- incident classification;
- evidence type;
- evidence reliability;
- business impact status;
- action priority.

### Contrato

`docs/contracts/DOMAIN_ENUMS.md`

### Critérios de aceite

- valores válidos aceitos;
- valores inválidos rejeitados;
- aliases não documentados rejeitados;
- casing preservado;
- serialização previsível;
- testes unitários implementados;
- Ruff aprovado;
- pytest aprovado.

---

## DG-102 — Modelo Evidence

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ✅ CONCLUÍDO

### Escopo

Implementar o modelo Pydantic responsável por representar uma evidência individual.

### Contrato

`docs/contracts/EVIDENCE_MODEL.md`

### Critérios de aceite

- `evidence_id` obrigatório;
- `evidence_type` validado;
- `source` obrigatório;
- reliability opcional e validada;
- datetime validado;
- metadata suportada;
- campos extras rejeitados;
- serialização previsível;
- IDs duplicados permanecem responsabilidade de camada superior;
- testes aprovados.

---

## DG-103 — Modelo IncidentInput

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Escopo

Converter `INCIDENT_INPUT.md` em modelos Pydantic.

### Responsabilidades

- campos obrigatórios;
- campos opcionais;
- timestamps;
- coleção de `Evidence`;
- `initial_severity`;
- tags;
- datasets afetados;
- validação de identificadores duplicados de evidência.

### Critérios de aceite

- campos obrigatórios efetivamente exigidos;
- campos opcionais aceitos;
- timestamps inválidos rejeitados;
- evidências estruturadas;
- IDs duplicados tratados deterministicamente;
- requests malformadas falham de forma previsível;
- testes válidos e inválidos implementados.

---

## DG-104 — Modelos AgentResponse

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Escopo

Implementar:

- `BusinessImpact`;
- `RootCauseHypothesis`;
- `RecommendedAction`;
- `GovernanceControl`;
- `AgentResponse`.

### Critérios de aceite

- confidence restrita ao intervalo definido;
- severity normalizada;
- `human_review_required` booleano;
- supporting evidence representável;
- hipóteses possuem status;
- serialização determinística;
- testes aprovados.

---

## DG-105 — Regras determinísticas de revisão humana

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Escopo

Implementar as regras definidas em:

`docs/contracts/SEVERITY_AND_HUMAN_REVIEW.md`

### Critérios de aceite

Revisão humana deve ser exigida quando aplicável a:

- severidade crítica;
- severidade alta com impacto material;
- confidence inferior a `0.70`;
- evidência insuficiente;
- evidência conflitante;
- exposição de governança;
- exposição regulatória;
- impacto de privacidade;
- ação destrutiva;
- ação irreversível;
- causa raiz altamente incerta;
- impossibilidade de determinar recomendação segura;
- processo crítico afetado.

Todas as regras devem possuir testes automatizados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-2"></a>

# 🛠️ Fase 2 — Ferramentas Determinísticas

Objetivo: implementar capacidades analíticas independentes da camada de orquestração.

---

## DG-201 — `evidence_collector`

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Objetivo

Normalizar e organizar as evidências associadas a um incidente.

### Critérios de aceite

- IDs preservados;
- rastreabilidade mantida;
- duplicidades detectadas;
- estruturas não suportadas tratadas explicitamente;
- comportamento determinístico;
- testes aprovados.

---

## DG-202 — `quality_analyzer`

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Objetivo

Analisar sinais determinísticos relacionados à qualidade dos dados.

### Padrões iniciais

- registros inválidos;
- divergência de reconciliação;
- relacionamentos ausentes;
- falhas de validação;
- divergência de contagem;
- inconsistências de integridade.

### Critérios de aceite

- findings referenciam evidências;
- fixtures conhecidas produzem resultados previsíveis;
- conclusões sem suporte não são geradas;
- testes aprovados.

---

## DG-203 — `business_impact_analyzer`

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Objetivo

Relacionar problemas técnicos a possíveis consequências de negócio.

### Critérios de aceite

- impacto confirmado e potencial diferenciados;
- estado `unknown` representável;
- evidências de suporte referenciadas;
- resultados determinísticos;
- testes aprovados.

---

## DG-204 — `policy_retriever`

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Objetivo

Recuperar controles ou políticas de governança aplicáveis ao incidente.

### Diretriz

A primeira implementação deve permanecer leve e determinística.

### Critérios de aceite

- políticas disponíveis localmente;
- recuperação previsível;
- controles contendo referência de origem;
- CI independente de banco vetorial;
- testes aprovados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-3"></a>

# 🔌 Fase 3 — Abstração de Provedores

Objetivo: separar comportamento dependente de modelos da lógica central de negócio.

---

## DG-301 — Interface de provider

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ✅ CONCLUÍDO

### Escopo

Definir uma abstração independente de fornecedor para interação com modelos.

### Critérios de aceite

- lógica central não acoplada diretamente a um fornecedor;
- interface compatível com saída estruturada;
- contrato documentado;
- comportamento testável.

---

## DG-302 — FakeProvider

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Objetivo

Fornecer comportamento previsível para:

- testes unitários;
- testes de integração;
- CI;
- desenvolvimento offline.

### Critérios de aceite

- sem credenciais;
- sem rede;
- respostas reproduzíveis;
- suporte a simulação de erros;
- testes aprovados.

---

## DG-303 — Provider real controlado

**Prioridade:** P1
**Complexidade:** MÉDIA
**Status:** ⏳ PENDENTE

### Critérios de aceite

- configuração por variáveis de ambiente;
- credenciais ausentes falham com segurança;
- nenhum segredo versionado;
- provider real opcional;
- CI independente dessa integração.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-4"></a>

# 🧠 Fase 4 — Workflow do Agente

Objetivo: orquestrar o processo de análise do incidente utilizando LangGraph.

---

## DG-401 — Estado do LangGraph

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

O estado deve representar explicitamente:

- incidente;
- evidências;
- resultados das ferramentas;
- erros;
- progresso do fluxo;
- resposta final.

---

## DG-402 — Nodes do LangGraph

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Nodes iniciais

- validar incidente;
- coletar evidências;
- analisar qualidade;
- analisar impacto de negócio;
- recuperar políticas;
- gerar hipóteses;
- gerar recomendações;
- determinar revisão humana;
- construir resposta final.

### Critérios de aceite

- responsabilidades estreitas;
- comportamento previsível;
- nodes testáveis individualmente quando aplicável;
- falhas representadas explicitamente.

---

## DG-403 — Orquestração LangGraph

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- grafo compila;
- fluxo de agente único;
- execução determinística com `FakeProvider`;
- ferramentas executadas na sequência esperada;
- `AgentResponse` final válida;
- testes de integração aprovados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-5"></a>

# 🛡️ Fase 5 — Guardrails

Objetivo: proteger a solução contra conclusões sem suporte e tornar incertezas explícitas.

---

## DG-501 — Guardrail de afirmações sem suporte

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- conclusões sem suporte são rejeitadas ou qualificadas;
- hipótese não se transforma silenciosamente em fato;
- testes incluem cenários sem evidência suficiente.

---

## DG-502 — Comportamento com evidência insuficiente

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- incidentes estruturalmente válidos continuam aceitos;
- confidence reduzida;
- evidência ausente explicitada;
- investigação adicional recomendada;
- revisão humana ativada quando aplicável;
- fabricação de evidências proibida.

---

## DG-503 — Validação de rastreabilidade

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- conclusões importantes referenciam IDs de evidência;
- referências inválidas detectadas;
- rastreabilidade mensurável;
- testes aprovados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-6"></a>

# 🌐 Fase 6 — FastAPI

Objetivo: disponibilizar o fluxo por meio de um contrato HTTP estável.

---

## DG-601 — Bootstrap FastAPI

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- aplicação inicia;
- endpoint `/health` operacional;
- configuração mínima;
- teste do endpoint aprovado.

---

## DG-602 — Endpoint de análise

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Endpoint esperado

```text
POST /api/v1/incidents/analyze
```

### Critérios de aceite

- recebe `IncidentInput`;
- executa workflow;
- retorna `AgentResponse`;
- requests inválidas recebem status apropriado;
- testes de API aprovados.

---

## DG-603 — Tratamento de erros da API

**Prioridade:** P1
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- erros de validação estruturados;
- detalhes sensíveis não expostos;
- falhas de provider tratadas;
- falhas internas tratadas com segurança;
- testes aprovados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-7"></a>

# 📊 Fase 7 — Avaliação

Objetivo: medir objetivamente o comportamento da solução.

---

## DG-701 — Dataset de avaliação

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Cenários iniciais

- incidente inspirado em DE-101;
- incidente inspirado em DE-102;
- evidência insuficiente;
- evidência conflitante;
- incidente de baixa severidade;
- incidente crítico;
- tentativa de afirmação sem suporte.

Os repositórios de origem permanecem inalterados.

---

## DG-702 — Métricas de avaliação

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Métricas

- `schema_valid_rate`;
- `severity_accuracy`;
- `evidence_traceability_rate`;
- `unsupported_rejection_rate`;
- `human_review_accuracy`;
- `tool_execution_success_rate`;
- `response_latency`;
- `test_pass_rate`.

### Critérios de aceite

- métricas formalmente definidas;
- cálculo reproduzível;
- avaliação determinística disponível;
- resultados interpretáveis.

---

## DG-703 — Relatório de avaliação

**Prioridade:** P1
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- comando de avaliação gera resumo;
- métricas legíveis;
- resultados reutilizáveis no README;
- resultados reutilizáveis na apresentação do Challenge.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-8"></a>

# 🖥️ Fase 8 — Interface Web

Objetivo: criar experiência profissional de demonstração sem complexidade desnecessária.

---

## DG-801 — Bootstrap Node.js

**Prioridade:** P1
**Complexidade:** BAIXA
**Status:** ✅ CONCLUÍDO

### Stack

- Node.js;
- Express;
- EJS;
- Vanilla JavaScript.

### Critérios de aceite

- aplicação inicia localmente;
- configuração simples;
- integração prevista com API;
- React ou Next.js não introduzidos.

---

## DG-802 — Tela de entrada do incidente

**Prioridade:** P1
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Critérios de aceite

- preenchimento manual de incidente;
- carregamento de cenário de demonstração;
- validação básica;
- envio para análise.

---

## DG-803 — Tela de resultado

**Prioridade:** P1
**Complexidade:** MÉDIA
**Status:** ✅ CONCLUÍDO

### Exibir

- classificação;
- severidade;
- resumo executivo;
- evidências;
- impacto de negócio;
- hipóteses;
- recomendações;
- controles de governança;
- confidence;
- necessidade de revisão humana.

---

## DG-804 — Polimento da demonstração

**Prioridade:** P2
**Complexidade:** BAIXA
**Status:** ✅ CONCLUÍDO

### Escopo

- hierarquia visual;
- identificação clara de severidade;
- aviso de revisão humana;
- cards de evidência;
- loading state;
- error state;
- legibilidade;
- responsividade básica.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-9"></a>

# 🎬 Fase 9 — Demonstração do Challenge

Objetivo: demonstrar valor técnico e de negócio por meio de cenários representativos.

---

## DG-901 — Cenário DE-101

**Prioridade:** P0
**Complexidade:** MÉDIA
**Status:** ⏳ PENDENTE

### Objetivo

Construir um incidente representativo baseado nos padrões de Data Quality previamente investigados no:

`aws-lakehouse-engineering-lab`

O repositório original permanecerá inalterado.

---

## DG-902 — Cenário DE-102

**Prioridade:** P1
**Complexidade:** MÉDIA
**Status:** ⏳ PENDENTE

### Objetivo

Criar um segundo cenário representativo para demonstrar capacidade de generalização.

---

## DG-903 — Narrativa da demonstração

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ⏳ PENDENTE

### Narrativa esperada

1. problema de negócio;
2. incidente recebido;
3. evidências disponíveis;
4. ferramentas utilizadas;
5. limites do raciocínio baseado em IA;
6. controles de governança;
7. supervisão humana;
8. resultados mensuráveis;
9. valor de negócio.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="fase-10"></a>

# 🔒 Fase 10 — Hardening Final

Objetivo: preparar o repositório para o code freeze.

---

## DG-1001 — Quality gate completo

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ⏳ PENDENTE

### Validações obrigatórias

```bash
python -m pip check
ruff check .
ruff format --check .
pytest
```

Também validar:

- CI;
- instalação em ambiente limpo;
- ausência de arquivos temporários;
- árvore Git limpa.

---

## DG-1002 — Revisão de segurança e segredos

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ⏳ PENDENTE

### Critérios de aceite

- nenhuma chave versionada;
- `.env` ignorado;
- exemplo de configuração seguro;
- credenciais opcionais;
- documentação sem dados sensíveis.

---

## DG-1003 — Revisão de documentação

**Prioridade:** P0
**Complexidade:** BAIXA
**Status:** ⏳ PENDENTE

### Critérios de aceite

- README compatível com implementação;
- documentação em PT-BR;
- instruções reproduzíveis;
- diagramas coerentes;
- avaliação atualizada;
- limitações documentadas;
- links válidos;
- índice documental atualizado.

---

## DG-1004 — Code freeze

**Prioridade:** P0
**Complexidade:** NÃO APLICÁVEL
**Status:** ⏳ PENDENTE

### Data-alvo

**06/11/2026**

Após o code freeze:

- nenhuma funcionalidade desnecessária;
- somente correções bloqueadoras;
- validação final;
- ensaio da demonstração;
- preparação da submissão.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="itens-adiados"></a>

# 🧊 Itens adiados / Pós-Challenge

Os seguintes itens permanecem fora do escopo do MVP, salvo mudança explícita nos requisitos:

- Kubernetes;
- arquitetura multi-agent;
- Redis;
- Qdrant;
- integração runtime com Airflow;
- integração runtime com Spark;
- React;
- Next.js;
- autenticação complexa;
- IAM corporativo;
- implantação obrigatória em cloud;
- remediação autônoma;
- escalabilidade de produção;
- infraestrutura distribuída desnecessária.

Esses itens podem ser revisitados posteriormente, caso exista benefício concreto.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)

---

<a id="regra-backlog"></a>

# 🧭 Regra de controle do backlog

Uma nova tarefa deve entrar no backlog anterior à entrega somente quando melhorar materialmente pelo menos um dos seguintes aspectos:

- aderência ao Challenge;
- confiabilidade;
- explicabilidade;
- governança;
- rastreabilidade;
- segurança;
- avaliação;
- qualidade da demonstração;
- qualidade profissional do portfólio.

Caso contrário, a tarefa deve ser adiada.

---

## ✅ Definition of Done geral

Uma tarefa de implementação só deve ser considerada concluída quando, quando aplicável:

- requisitos atendidos;
- critérios de aceite satisfeitos;
- testes implementados;
- testes aprovados;
- Ruff aprovado;
- dependências válidas;
- documentação atualizada;
- comportamento reproduzível;
- nenhuma regressão conhecida introduzida.

---

## 🔄 Fluxo de execução

```text
Planejamento
     ↓
Contrato / critérios de aceite
     ↓
Implementação com escopo controlado
     ↓
Testes
     ↓
Quality gates
     ↓
Revisão
     ↓
Versionamento
     ↓
Próxima tarefa
```

---

> 📋 O backlog do **AI Data Governance Agent** prioriza entregas pequenas, testáveis, rastreáveis e alinhadas ao objetivo de produzir uma solução profissional de Engenharia de Dados, Inteligência Artificial e Governança.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](README.md)
