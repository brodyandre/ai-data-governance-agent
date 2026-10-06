# 🏗️ ADR-001 — Escopo do Projeto e Stack Tecnológica

## 📌 Status

**Aceito**

## 📅 Data

**05/10/2026**

---

<a id="sumario"></a>

## 📑 Sumário

- [Contexto](#contexto)
- [Decisão](#decisao)
- [Stack tecnológica](#stack)
- [Ferramentas iniciais](#ferramentas)
- [Restrições arquiteturais](#restricoes)
- [Justificativa](#justificativa)
- [Consequências](#consequencias)
- [Trade-offs](#tradeoffs)
- [Condições para revisão](#revisao)

---

<a id="contexto"></a>

## 🔎 Contexto

O **AI Data Governance Agent** está sendo desenvolvido como projeto individual do Challenge da **Imersão de Agentes de IA para Negócios — Alura + Oracle Next Education (ONE)**.

O projeto possui prazo definido e precisa equilibrar:

- relevância de negócio;
- aplicação prática de Inteligência Artificial;
- aderência à Engenharia de Dados;
- Data Quality;
- Data Governance;
- segurança;
- rastreabilidade;
- testes automatizados;
- qualidade da demonstração;
- tempo limitado de desenvolvimento.

Adicionar tecnologias sem benefício direto aumentaria o risco de implementação e reduziria o tempo disponível para:

- testes;
- avaliação;
- documentação;
- refinamento;
- demonstração.

Portanto, a arquitetura inicial deve permanecer enxuta e orientada ao problema.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="decisao"></a>

## ✅ Decisão

O projeto adotará uma arquitetura de agente único, baseada em contratos estruturados e ferramentas com responsabilidades bem definidas.

O sistema será construído de forma incremental.

O fluxo conceitual será:

```text
IncidentInput
     │
     ▼
Validação
     │
     ▼
Coleta de evidências
     │
     ▼
Ferramentas determinísticas
     │
     ▼
Orquestração
     │
     ▼
Guardrails
     │
     ▼
Supervisão humana
     │
     ▼
AgentResponse
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="stack"></a>

## 🧰 Stack tecnológica

### Backend

| Tecnologia | Responsabilidade |
|---|---|
| Python 3.12 | Linguagem principal |
| FastAPI | Interface HTTP |
| Pydantic | Modelagem e validação de contratos |
| LangGraph | Orquestração do workflow |

### Qualidade de desenvolvimento

| Tecnologia | Responsabilidade |
|---|---|
| pytest | Testes automatizados |
| pytest-cov | Cobertura |
| Ruff | Lint e formatação |
| GitHub Actions | Integração contínua |

### Estratégia de providers de IA

A lógica de negócio não deverá depender diretamente de um fornecedor específico.

Será criada uma camada de abstração para providers.

A estratégia inicial contempla:

```text
Aplicação
    │
    ▼
Provider Interface
    │
    ├── Provider determinístico para testes
    │
    └── Provider real opcional
```

### Requisitos

A CI deverá funcionar:

- sem credenciais externas;
- sem chamadas de rede obrigatórias;
- com resultados reproduzíveis.

A integração com modelos reais será opcional e utilizada apenas quando necessária à demonstração ou avaliação.

### Interface web

Abordagem principal:

- Node.js;
- Express;
- EJS;
- Vanilla JavaScript.

Alternativa de contingência:

- Streamlit.

A interface deverá priorizar:

- simplicidade;
- clareza;
- boa demonstração;
- baixo custo de manutenção.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="ferramentas"></a>

## 🛠️ Ferramentas iniciais

O MVP terá quatro capacidades principais:

### `quality_analyzer`

Analisa sinais relacionados à qualidade dos dados.

### `business_impact_analyzer`

Traduz descobertas técnicas em possíveis impactos de negócio.

### `policy_retriever`

Identifica regras, políticas ou controles de governança relevantes.

### `evidence_collector`

Organiza e preserva a rastreabilidade das evidências.

Essas ferramentas devem possuir contratos claros e ser testáveis independentemente da camada de orquestração.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="restricoes"></a>

## 🚧 Restrições arquiteturais

Antes da entrega do Challenge, o projeto evitará deliberadamente:

- Kubernetes;
- arquitetura multi-agent;
- infraestrutura cloud obrigatória;
- bancos complexos;
- Qdrant;
- Redis;
- Airflow no runtime;
- Spark no runtime;
- React;
- Next.js;
- autenticação corporativa complexa;
- remediação crítica autônoma;
- execução automática de ações irreversíveis.

Essa restrição não significa que essas tecnologias não sejam úteis.

Ela significa apenas que **não são necessárias para demonstrar adequadamente o valor do MVP**.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="justificativa"></a>

## 💡 Justificativa

### Python

Python possui forte aderência às necessidades de:

- Inteligência Artificial;
- Engenharia de Dados;
- validação;
- avaliação;
- testes;
- automação.

### FastAPI

FastAPI oferece:

- contratos HTTP simples;
- integração natural com Pydantic;
- documentação OpenAPI;
- validação estruturada;
- baixo overhead arquitetural.

### Pydantic

Pydantic permite definir contratos explícitos para:

- entrada;
- evidências;
- resultados de ferramentas;
- saída final.

Isso reduz ambiguidades e melhora a previsibilidade do sistema.

### LangGraph

LangGraph permite representar o fluxo do agente de forma explícita.

A escolha favorece:

- estados bem definidos;
- nodes com responsabilidades claras;
- controle de execução;
- testabilidade;
- evolução futura.

A primeira versão permanecerá com **arquitetura de agente único**.

### Provider abstrato

Separar providers da lógica de negócio reduz acoplamento com:

- fornecedor;
- credenciais;
- disponibilidade externa;
- latência;
- custo;
- comportamento não determinístico.

Isso permite que testes e CI permaneçam previsíveis.

### Node.js + Express + EJS

Essa combinação oferece flexibilidade suficiente para construir uma interface profissional de demonstração sem o overhead de uma SPA completa.

O projeto prioriza experiência de demonstração e simplicidade de manutenção.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="consequencias"></a>

## 📈 Consequências

### Consequências positivas

A decisão arquitetural proporciona:

- menor risco de entrega;
- ambiente local mais simples;
- CI determinística;
- testes mais fáceis;
- contratos explícitos;
- baixo custo de infraestrutura;
- maior explicabilidade;
- rastreabilidade;
- melhor controle de escopo;
- forte aderência a Engenharia de Dados e Governança.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="tradeoffs"></a>

## ⚖️ Trade-offs

A arquitetura inicial não demonstrará:

- infraestrutura distribuída;
- Kubernetes;
- arquitetura multi-agent;
- frontend SPA moderno;
- escalabilidade corporativa;
- arquitetura cloud complexa;
- processamento distribuído em runtime.

Essas limitações são aceitas porque não reduzem materialmente o valor principal da demonstração.

O objetivo do Challenge é demonstrar uma solução coerente e funcional, e não reproduzir uma plataforma empresarial completa.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="revisao"></a>

## 🔄 Condições para revisão

Esta decisão deverá ser revisitada somente se:

- um requisito oficial exigir outra tecnologia;
- um componente selecionado apresentar incompatibilidade bloqueadora;
- uma alternativa mais simples melhorar significativamente a confiabilidade;
- uma capacidade essencial não puder ser demonstrada;
- requisitos futuros justificarem expansão arquitetural.

### Regra

```text
Nova tecnologia
      │
      ▼
Resolve problema real?
      │
 ┌────┴────┐
 │         │
Sim       Não
 │         │
 ▼         ▼
Avaliar   Adiar
```

Complexidade arquitetural por si só não constitui justificativa suficiente para alterar esta decisão.

---

## 🎯 Resultado esperado

A arquitetura deve permitir que o projeto permaneça:

- compreensível;
- testável;
- reproduzível;
- rastreável;
- seguro;
- demonstrável;
- evolutivo.

---

> 🏗️ Esta decisão arquitetural prioriza uma solução enxuta e profissional, capaz de demonstrar claramente a integração entre Engenharia de Dados, Inteligência Artificial, Data Quality e Governança.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)
