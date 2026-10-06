# 🏷️ Contrato de Enums de Domínio

Este documento define os **valores enumerados normalizados** utilizados pelos modelos de domínio do **AI Data Governance Agent**.

Os enums funcionam como contratos estáveis entre as diferentes camadas da solução, reduzindo ambiguidades e impedindo que valores equivalentes sejam representados de maneiras diferentes.

---

<a id="sumario"></a>

## 📑 Sumário

- [Objetivo](#objetivo)
- [Princípios gerais](#principios-gerais)
- [Severity](#severity)
- [IncidentClassification](#incident-classification)
- [EvidenceType](#evidence-type)
- [EvidenceReliability](#evidence-reliability)
- [BusinessImpactStatus](#business-impact-status)
- [ActionPriority](#action-priority)
- [Regras de validação](#validacao)
- [Regras de serialização](#serializacao)
- [Local de implementação](#implementacao)
- [Testes obrigatórios](#testes)
- [Critérios de aceite](#criterios-aceite)
- [Valores de domínio adiados](#valores-adiados)

---

<a id="objetivo"></a>

## 🎯 Objetivo

Os enums definidos neste contrato serão utilizados em:

- modelos Pydantic;
- ferramentas determinísticas;
- estado do LangGraph;
- requests e responses da API;
- fixtures de avaliação;
- testes automatizados;
- interface web de demonstração.

A implementação correspondente está planejada na tarefa:

```text
DG-101 — Enums de severidade e classificação
```

O principal objetivo é garantir que valores de domínio sejam:

- explícitos;
- previsíveis;
- validados;
- serializáveis;
- consistentes entre diferentes componentes.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="principios-gerais"></a>

## 📐 Princípios gerais

Todos os enums definidos pela `DG-101` devem seguir as mesmas regras.

### Nomenclatura Python

As classes devem utilizar **PascalCase**.

Exemplo:

```python
class Severity(StrEnum): ...
```

Os membros das classes devem utilizar nomes em letras maiúsculas.

Exemplo:

```python
Severity.HIGH
```

---

### Valores serializados

Os valores serializados devem utilizar:

```text
lowercase_snake_case
```

Exemplos:

```text
high
data_quality
pipeline_failure
reconciliation_result
```

---

### Case sensitivity

Os valores são **case-sensitive**.

Portanto:

```text
high
```

é válido.

Enquanto:

```text
HIGH
High
```

são inválidos como valores serializados.

---

### Aliases

Aliases não documentados não devem ser aceitos.

Exemplo:

```text
med
```

não deve ser interpretado automaticamente como:

```text
medium
```

Da mesma forma:

```text
dq
```

não deve ser convertido para:

```text
data_quality
```

---

### Normalização automática

A implementação não deve corrigir silenciosamente entradas inválidas.

Exemplo:

```text
data-quality
```

não deve ser automaticamente convertido para:

```text
data_quality
```

O valor inválido deve ser rejeitado.

---

### Estabilidade

Depois que um valor for exposto por um contrato público da aplicação, sua representação serializada deverá permanecer estável.

Isso evita divergências entre:

```text
Backend
   ↕
API
   ↕
Interface
   ↕
Testes
   ↕
Avaliação
```

---

## 🐍 Implementação Python

A implementação planejada deve utilizar `StrEnum`, disponível no Python 3.12.

Exemplo:

```python
from enum import StrEnum


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

A representação:

```python
Severity.HIGH
```

deve ser serializada como:

```json
"high"
```

e nunca como:

```text
Severity.HIGH
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="severity"></a>

## 🚦 Severity

### Classe Python

```text
Severity
```

### Objetivo

Representar a severidade normalizada atribuída a um incidente.

### Valores

| Membro Python | Valor serializado |
|---|---|
| `LOW` | `low` |
| `MEDIUM` | `medium` |
| `HIGH` | `high` |
| `CRITICAL` | `critical` |

### Hierarquia conceitual

Da menor para a maior severidade:

```text
low
 ↓
medium
 ↓
high
 ↓
critical
```

Ou, conceitualmente:

```text
low < medium < high < critical
```

A interpretação detalhada dos níveis está definida em:

➡️ [`SEVERITY_AND_HUMAN_REVIEW.md`](SEVERITY_AND_HUMAN_REVIEW.md)

### Limites da DG-101

A `DG-101` não deverá implementar:

- comparação automática entre enums;
- escalonamento automático;
- regras de revisão humana;
- cálculo de severidade.

Esses comportamentos pertencem a etapas posteriores.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="incident-classification"></a>

## 🧭 IncidentClassification

### Classe Python

```text
IncidentClassification
```

### Objetivo

Representar a classificação principal de um incidente.

### Valores

| Membro Python | Valor serializado |
|---|---|
| `DATA_QUALITY` | `data_quality` |
| `SCHEMA` | `schema` |
| `INTEGRITY` | `integrity` |
| `RECONCILIATION` | `reconciliation` |
| `FRESHNESS` | `freshness` |
| `PIPELINE_FAILURE` | `pipeline_failure` |
| `GOVERNANCE` | `governance` |
| `UNKNOWN` | `unknown` |

---

### `data_quality`

Problema relacionado à qualidade dos dados.

Exemplos conceituais:

- valores inválidos;
- campos ausentes;
- falhas em regras de qualidade.

---

### `schema`

Problema relacionado à estrutura ou ao schema dos dados.

Exemplos:

- coluna ausente;
- tipo incompatível;
- alteração inesperada de schema.

---

### `integrity`

Problema relacionado à integridade dos dados.

Exemplos:

- chave inválida;
- relacionamento quebrado;
- referência inexistente.

---

### `reconciliation`

Problema identificado por divergência entre valores, volumes ou fontes que deveriam reconciliar.

Exemplo:

```text
RAW = 400 registros
SILVER = 388 registros
```

---

### `freshness`

Problema relacionado ao atraso ou desatualização dos dados.

Exemplos:

- dataset não atualizado;
- atraso na ingestão;
- SLA de atualização não atendido.

---

### `pipeline_failure`

Falha diretamente relacionada à execução de um pipeline ou processo.

---

### `governance`

Problema relacionado a políticas, controles ou requisitos de governança.

---

### `unknown`

Valor explícito utilizado quando as evidências disponíveis não permitem uma classificação mais específica.

`UNKNOWN` é um valor válido do domínio.

Entretanto, ele **não deve ser utilizado como fallback silencioso para entradas inválidas**.

Exemplo:

```text
security_problem
```

não deve ser automaticamente convertido em:

```text
unknown
```

Nesse caso, a entrada deve ser rejeitada.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidence-type"></a>

## 🧾 EvidenceType

### Classe Python

```text
EvidenceType
```

### Objetivo

Representar o tipo de uma evidência associada a um incidente.

### Valores

| Membro Python | Valor serializado |
|---|---|
| `DATA_QUALITY_CHECK` | `data_quality_check` |
| `PIPELINE_REPORT` | `pipeline_report` |
| `VALIDATION_RESULT` | `validation_result` |
| `RECONCILIATION_RESULT` | `reconciliation_result` |
| `LOG` | `log` |
| `BUSINESS_RULE` | `business_rule` |
| `GOVERNANCE_POLICY` | `governance_policy` |
| `ANALYST_OBSERVATION` | `analyst_observation` |
| `METRIC` | `metric` |
| `DATASET_SAMPLE` | `dataset_sample` |

---

### `data_quality_check`

Resultado de uma verificação de Data Quality.

Exemplos:

- null check;
- uniqueness check;
- range validation;
- relationship validation.

---

### `pipeline_report`

Relatório ou artefato produzido por um pipeline.

---

### `validation_result`

Resultado de uma validação técnica ou funcional.

---

### `reconciliation_result`

Resultado da comparação entre valores ou contagens que deveriam reconciliar.

---

### `log`

Registro técnico de execução.

---

### `business_rule`

Regra de negócio relevante para interpretar o incidente.

---

### `governance_policy`

Política ou controle de governança aplicável.

---

### `analyst_observation`

Observação realizada por uma pessoa durante investigação ou análise.

---

### `metric`

Valor quantitativo utilizado como evidência.

---

### `dataset_sample`

Amostra de registros utilizada como evidência.

---

## Regra de extensão

Novos tipos de evidência não devem ser adicionados sem uma necessidade concreta do projeto.

Valores não suportados devem ser rejeitados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidence-reliability"></a>

## 📊 EvidenceReliability

### Classe Python

```text
EvidenceReliability
```

### Objetivo

Representar a confiabilidade atribuída a uma evidência.

### Valores

| Membro Python | Valor serializado |
|---|---|
| `LOW` | `low` |
| `MEDIUM` | `medium` |
| `HIGH` | `high` |

---

### `low`

A evidência possui limitações significativas ou baixa confiabilidade.

---

### `medium`

A evidência possui confiabilidade intermediária.

---

### `high`

A evidência é considerada altamente confiável dentro do contexto analisado.

---

## Ausência de confiabilidade

O enum não possui um membro:

```text
UNKNOWN
```

Essa decisão é intencional.

Quando a confiabilidade não estiver disponível, o futuro modelo `Evidence` deverá representar esse estado como:

```text
None
```

ou ausência do campo, conforme o contrato.

Essa separação evita confundir:

```text
confiabilidade não informada
```

com:

```text
classificação explícita de confiabilidade
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="business-impact-status"></a>

## 💼 BusinessImpactStatus

### Classe Python

```text
BusinessImpactStatus
```

### Objetivo

Distinguir se um impacto de negócio é:

- confirmado;
- potencial;
- desconhecido.

### Valores

| Membro Python | Valor serializado |
|---|---|
| `CONFIRMED` | `confirmed` |
| `POTENTIAL` | `potential` |
| `UNKNOWN` | `unknown` |

---

### `confirmed`

As evidências disponíveis sustentam que a consequência de negócio ocorreu.

Fluxo conceitual:

```text
Evidência
   ↓
Impacto observado
   ↓
confirmed
```

---

### `potential`

Existe risco ou consequência plausível sustentada pelas evidências, mas o impacto ainda não foi confirmado.

```text
Evidência
   ↓
Risco plausível
   ↓
potential
```

---

### `unknown`

As evidências são insuficientes para determinar o impacto de negócio.

```text
Evidência insuficiente
        ↓
      unknown
```

---

## Regra

A implementação deve preservar claramente a distinção entre:

```text
confirmed
potential
unknown
```

Esses estados não são intercambiáveis.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="action-priority"></a>

## ⚡ ActionPriority

### Classe Python

```text
ActionPriority
```

### Objetivo

Representar a prioridade de uma ação recomendada pelo sistema.

### Valores

| Membro Python | Valor serializado |
|---|---|
| `LOW` | `low` |
| `MEDIUM` | `medium` |
| `HIGH` | `high` |
| `URGENT` | `urgent` |

---

### Hierarquia conceitual

```text
low
 ↓
medium
 ↓
high
 ↓
urgent
```

### Importante

Prioridade não representa autorização.

Uma ação classificada como:

```text
urgent
```

continua sendo uma **recomendação consultiva**.

Ela não autoriza execução automática.

A aprovação humana continua necessária quando exigida pelas regras de governança.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="validacao"></a>

## ✅ Regras de validação

Os valores devem ser aceitos exatamente conforme definidos neste contrato.

### Exemplos válidos

```text
high
data_quality
reconciliation_result
potential
urgent
```

### Exemplos inválidos

```text
HIGH
Data_Quality
data-quality
very_high
critical_incident
trusted
```

Valores inválidos devem ser rejeitados.

O sistema não deve corrigi-los silenciosamente.

---

## Aliases não suportados

Exemplos:

```text
med
sev1
dq
pipeline
reconcile
```

Esses valores não devem ser traduzidos automaticamente para enums válidos.

### Exemplo

Entrada:

```text
sev1
```

não deve ser convertida para:

```text
critical
```

O comportamento correto é rejeitar a entrada.

---

## Casing

Entrada válida:

```text
high
```

Entradas inválidas:

```text
HIGH
High
hIGH
```

Essa regra mantém os contratos previsíveis.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="serializacao"></a>

## 📤 Regras de serialização

Os enums devem ser serializados utilizando seus valores de string.

Exemplo esperado:

```json
{
  "severity": "high",
  "classification": "data_quality",
  "business_impact_status": "potential",
  "action_priority": "urgent"
}
```

Consumidores da API não devem receber representações internas do Python como:

```text
Severity.HIGH
IncidentClassification.DATA_QUALITY
ActionPriority.URGENT
```

---

## Fluxo de representação

```text
Python
Severity.HIGH
     │
     ▼
Serialização
     │
     ▼
"high"
```

O formato serializado deve permanecer estável entre:

- API;
- testes;
- fixtures;
- relatórios;
- interface web.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="implementacao"></a>

## 📁 Local de implementação

Estrutura planejada:

```text
src/
└── ai_data_governance_agent/
    └── domain/
        ├── __init__.py
        └── enums.py
```

Estrutura planejada para testes:

```text
tests/
└── domain/
    └── test_enums.py
```

---

## 🔒 Limites da implementação DG-101

A `DG-101` deve permanecer pequena e focada exclusivamente nos enums.

Ela **não deve implementar**:

- modelos Pydantic de `IncidentInput`;
- modelo `Evidence`;
- modelos de `AgentResponse`;
- regras de revisão humana;
- ferramentas analíticas;
- FastAPI;
- LangGraph;
- providers de modelos;
- lógica de negócio de severidade.

Essas responsabilidades pertencem a tarefas posteriores.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="testes"></a>

## 🧪 Testes obrigatórios

Os testes da `DG-101` devem verificar, no mínimo:

1. todos os membros documentados existem;
2. cada membro possui exatamente o valor esperado;
3. strings válidas constroem corretamente seus enums;
4. valores não suportados são rejeitados;
5. casing incorreto é rejeitado;
6. aliases não documentados não são aceitos.

---

## Exemplos válidos

```python
Severity("high") == Severity.HIGH

IncidentClassification("data_quality") == IncidentClassification.DATA_QUALITY

EvidenceType("reconciliation_result") == EvidenceType.RECONCILIATION_RESULT

EvidenceReliability("high") == EvidenceReliability.HIGH

BusinessImpactStatus("potential") == BusinessImpactStatus.POTENTIAL

ActionPriority("urgent") == ActionPriority.URGENT
```

---

## Entradas inválidas representativas

Os testes devem incluir valores como:

```text
HIGH
very_high
Data_Quality
data-quality
trusted
immediate
```

Todos devem ser rejeitados.

---

## 🔁 Cobertura dos seis enums

Os testes devem abranger:

```text
Severity
IncidentClassification
EvidenceType
EvidenceReliability
BusinessImpactStatus
ActionPriority
```

Nenhum enum documentado deve permanecer sem teste.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="criterios-aceite"></a>

## ✅ Critérios de aceite

A `DG-101` será considerada concluída quando:

- os seis enums estiverem implementados;
- os valores corresponderem exatamente a este contrato;
- valores inválidos forem rejeitados;
- casing inválido for rejeitado;
- aliases não documentados forem rejeitados;
- valores válidos forem serializados de forma previsível;
- testes válidos e inválidos estiverem implementados;
- nenhum modelo de domínio não relacionado for introduzido;
- todas as verificações de qualidade forem aprovadas.

### Quality gates

```bash
python -m pip check
ruff check .
ruff format --check .
pytest
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="valores-adiados"></a>

## ⏳ Valores de domínio adiados

O contrato de resposta do agente também prevê estados relacionados às hipóteses.

Os valores planejados são:

```text
suspected
probable
confirmed
rejected
```

Esses valores **não fazem parte da DG-101**.

Eles permanecem deliberadamente adiados para:

```text
DG-104 — Modelos AgentResponse
```

Essa separação evita ampliar desnecessariamente o escopo da implementação inicial.

---

## 🧭 Visão consolidada

Os seis enums definidos neste contrato são:

| Enum | Quantidade de valores |
|---|---:|
| `Severity` | 4 |
| `IncidentClassification` | 8 |
| `EvidenceType` | 10 |
| `EvidenceReliability` | 3 |
| `BusinessImpactStatus` | 3 |
| `ActionPriority` | 4 |

Total:

```text
32 valores normalizados
```

---

## 🔗 Relação com outros contratos

```text
DOMAIN_ENUMS
     │
     ├── Severity
     │      └── SEVERITY_AND_HUMAN_REVIEW
     │
     ├── EvidenceType
     │      └── EVIDENCE_MODEL
     │
     ├── EvidenceReliability
     │      └── EVIDENCE_MODEL
     │
     ├── IncidentClassification
     │      └── AgentResponse
     │
     ├── BusinessImpactStatus
     │      └── BusinessImpact
     │
     └── ActionPriority
            └── RecommendedAction
```

Os enums constituem uma das camadas mais básicas do domínio e devem permanecer independentes das regras de negócio que os utilizam.

---

> 🏷️ Este contrato garante que valores fundamentais do **AI Data Governance Agent** sejam representados de maneira consistente, previsível e validável em todas as camadas da solução.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)
