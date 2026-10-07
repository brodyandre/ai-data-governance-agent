# 📥 Contrato de Entrada de Incidente — IncidentInput

Este documento define o contrato conceitual de entrada para incidentes submetidos ao **AI Data Governance Agent**.

O contrato será posteriormente implementado utilizando **Pydantic**, preservando os nomes técnicos definidos nesta especificação.

---

<a id="sumario"></a>

## 📑 Sumário

- [Objetivo](#objetivo)
- [Visão geral](#visao-geral)
- [Campos obrigatórios](#campos-obrigatorios)
- [Campos opcionais](#campos-opcionais)
- [Estrutura de evidência](#evidencia)
- [Tipos de evidência](#tipos-evidencia)
- [Princípios de validação](#validacao)
- [Evidência insuficiente](#evidencia-insuficiente)
- [Exemplo](#exemplo)
- [Responsabilidades futuras](#responsabilidades)

---

<a id="objetivo"></a>

## 🎯 Objetivo

O `IncidentInput` representa o ponto de entrada formal para um incidente de dados.

Sua função é fornecer uma estrutura previsível para que o restante do sistema possa:

- identificar o incidente;
- compreender o problema observado;
- localizar a origem;
- identificar datasets afetados;
- acessar evidências;
- compreender o contexto de negócio;
- avaliar severidade;
- executar análises posteriores.

O contrato deve permanecer explícito, validável e independente da camada de orquestração.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="visao-geral"></a>

## 🔎 Visão geral

Estrutura conceitual:

```text
IncidentInput
     │
     ├── Identificação
     │
     ├── Descrição do incidente
     │
     ├── Sistema de origem
     │
     ├── Momento da detecção
     │
     ├── Contexto de negócio
     │
     ├── Datasets afetados
     │
     ├── Severidade inicial
     │
     └── Evidências
```

Os campos obrigatórios permitem representar o incidente em seu nível mínimo necessário.

Os campos opcionais adicionam contexto quando essa informação estiver disponível.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="campos-obrigatorios"></a>

## 📌 Campos obrigatórios

### `incident_id`

Identificador único do incidente.

Exemplo:

```text
EX-001
```

O identificador deve permitir que o incidente seja referenciado de forma estável ao longo de todo o fluxo de análise.

---

### `title`

Descrição curta e legível do incidente.

Exemplo:

```text
Silver layer record divergence
```

O título deve resumir o problema sem substituir a descrição detalhada.

---

### `description`

Descrição detalhada do problema observado.

Deve fornecer contexto suficiente para que o incidente possa ser compreendido por uma pessoa ou pelo fluxo de análise.

Exemplo conceitual:

```text
Record counts between raw and silver layers do not reconcile.
```

---

### `source_system`

Sistema, pipeline, dataset, plataforma ou processo no qual o incidente foi identificado ou teve origem.

Exemplo:

```text
lakehouse-pipeline
```

---

### `detected_at`

Timestamp ou data em que o incidente foi detectado.

Exemplo:

```text
2026-10-05T20:00:00Z
```

A implementação deverá utilizar uma representação temporal validável.

Valores temporais malformados devem ser rejeitados.

---

### `evidence`

Coleção das evidências técnicas ou de negócio associadas ao incidente.

Sempre que possível, pelo menos uma evidência deve ser fornecida.

Cada item deverá seguir o contrato formal definido em:

➡️ [`EVIDENCE_MODEL.md`](EVIDENCE_MODEL.md)

Exemplo conceitual:

```text
IncidentInput
     │
     └── evidence
           ├── EV-001
           ├── EV-002
           └── EV-003
```

Um incidente poderá ser estruturalmente válido mesmo quando a quantidade de evidências for insuficiente para uma conclusão confiável.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="campos-opcionais"></a>

## 🧩 Campos opcionais

### `affected_datasets`

Datasets conhecidos ou suspeitos de terem sido afetados pelo incidente.

Exemplo:

```json
[
  "orders",
  "order_items"
]
```

A presença de um dataset nesta coleção não implica, por si só, confirmação definitiva de impacto.

---

### `reported_by`

Pessoa, função, sistema ou processo automatizado que reportou o incidente.

Exemplos:

```text
data-quality-monitor
```

```text
Data Engineer
```

```text
analytics-validation-job
```

---

### `business_context`

Processo de negócio ou contexto analítico relacionado ao incidente.

Exemplo:

```text
Sales analytics pipeline
```

Esse campo pode auxiliar etapas posteriores na avaliação de impacto.

---

### `expected_behavior`

Comportamento esperado dos dados, do pipeline ou do processo.

Exemplo:

```text
Valid raw records should be represented in the silver layer.
```

---

### `observed_behavior`

Comportamento efetivamente observado durante o incidente.

Exemplo:

```text
Some records were rejected during data quality validation.
```

A comparação entre `expected_behavior` e `observed_behavior` pode ajudar a identificar divergências relevantes.

---

### `initial_severity`

Severidade opcional atribuída inicialmente pelo sistema de origem ou por um analista.

Esse valor representa a avaliação inicial e não necessariamente a classificação final produzida pelo agente.

Os valores válidos são definidos em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

A implementação deverá rejeitar valores de severidade não suportados.

---

### `tags`

Tags opcionais utilizadas para classificação ou organização do incidente.

Exemplo:

```json
[
  "data-quality",
  "reconciliation",
  "silver-layer"
]
```

As tags adicionam contexto, mas não substituem classificações formais de domínio.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidencia"></a>

## 🧾 Estrutura de evidência

Cada item da coleção `evidence` deverá representar uma evidência individual.

O modelo conceitual inclui:

| Campo | Finalidade |
|---|---|
| `evidence_id` | Identificador da evidência |
| `evidence_type` | Tipo normalizado |
| `source` | Origem da informação |
| `description` | Descrição opcional |
| `value` | Valor associado |
| `collected_at` | Momento da coleta |
| `reliability` | Nível de confiabilidade |
| `metadata` | Metadados adicionais |

O contrato formal do modelo está documentado em:

➡️ [`EVIDENCE_MODEL.md`](EVIDENCE_MODEL.md)

### Rastreabilidade

Cada evidência deve possuir um identificador estável para permitir referências posteriores.

Exemplo:

```text
EV-001
   │
   ├── finding
   │
   ├── hypothesis
   │
   └── recommendation
```

A rastreabilidade deve permitir identificar quais evidências sustentaram determinada conclusão.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="tipos-evidencia"></a>

## 🏷️ Tipos de evidência

Os tipos normalizados iniciais incluem:

| Valor | Uso conceitual |
|---|---|
| `data_quality_check` | Resultado de verificação de qualidade |
| `pipeline_report` | Relatório produzido por pipeline |
| `validation_result` | Resultado de validação |
| `reconciliation_result` | Resultado de reconciliação |
| `log` | Registro técnico |
| `business_rule` | Regra de negócio |
| `governance_policy` | Política ou controle de governança |
| `analyst_observation` | Observação de analista |
| `metric` | Métrica |
| `dataset_sample` | Amostra de dados |

A fonte canônica desses valores é:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

Valores não documentados devem ser rejeitados pela implementação.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="validacao"></a>

## ✅ Princípios de validação

A implementação final deverá rejeitar ou tratar explicitamente entradas contendo problemas como:

- ausência de `incident_id`;
- ausência de `title`;
- ausência de `description`;
- ausência de `source_system`;
- ausência de `detected_at`;
- timestamp malformado;
- valor inválido de severidade;
- identificadores de evidência duplicados;
- estruturas de evidência não suportadas;
- tipos de evidência inválidos.

### Identificadores duplicados

Dentro de um mesmo incidente, dois itens de evidência não deverão compartilhar o mesmo `evidence_id`.

Exemplo inválido:

```text
IncidentInput
     │
     ├── EV-001
     ├── EV-002
     └── EV-001  ← duplicado
```

A validação de unicidade pertence ao nível de `IncidentInput`, pois um objeto `Evidence` individual não possui conhecimento da coleção em que está inserido.

---

## 🧱 Separação de responsabilidades

O modelo de entrada deve validar estrutura.

Ele não deve assumir responsabilidades de análise.

```text
IncidentInput
     │
     ├── valida estrutura
     ├── valida tipos
     ├── valida timestamps
     ├── valida evidências
     └── valida unicidade de IDs
             │
             ▼
       Fluxo de análise
```

O `IncidentInput` não deve:

- calcular causa raiz;
- inferir impacto de negócio;
- atribuir confiabilidade automaticamente;
- gerar recomendações;
- consultar políticas;
- executar ferramentas analíticas.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidencia-insuficiente"></a>

## ⚠️ Evidência insuficiente

Um incidente poderá ser aceito mesmo quando as evidências disponíveis forem incompletas.

Estrutura válida e suficiência analítica são conceitos diferentes.

```text
Estrutura válida
      ≠
Evidência suficiente
```

Quando houver evidência insuficiente, essa condição deverá influenciar etapas posteriores, incluindo:

- `confidence`;
- recomendações;
- hipóteses de causa raiz;
- `human_review_required`.

O sistema não deverá fabricar evidências ausentes.

### Comportamento esperado

```text
Pouca evidência
      ↓
Análise limitada
      ↓
Menor confidence
      ↓
Limitação explícita
      ↓
Revisão humana quando aplicável
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="exemplo"></a>

## 🧪 Exemplo

> Este é um exemplo sintético do contrato e não representa o cenário
> canônico DG-901 / DE-101. Para esse cenário, consulte
> `../scenarios/DE-101.md`.

Exemplo de incidente válido:

```json
{
  "incident_id": "EX-001",
  "title": "Silver layer record divergence",
  "description": "Record counts between raw and silver layers do not reconcile.",
  "source_system": "lakehouse-pipeline",
  "detected_at": "2026-10-05T20:00:00Z",
  "affected_datasets": [
    "orders",
    "order_items"
  ],
  "business_context": "Sales analytics pipeline",
  "expected_behavior": "Valid raw records should be represented in the silver layer.",
  "observed_behavior": "Some records were rejected during data quality validation.",
  "evidence": [
    {
      "evidence_id": "EV-001",
      "evidence_type": "reconciliation_result",
      "source": "pipeline-report",
      "description": "Raw and silver record counts differ.",
      "value": "orders SOURCE=400 TARGET=388",
      "reliability": "high"
    }
  ]
}
```

### Interpretação

O exemplo informa que:

- o incidente possui ID `EX-001`;
- existe divergência entre camadas;
- os datasets `orders` e `order_items` podem estar envolvidos;
- existe evidência de reconciliação;
- a evidência possui confiabilidade `high`.

O contrato de entrada apenas representa esses fatos.

A interpretação analítica deve ocorrer nas etapas posteriores do sistema.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="responsabilidades"></a>

## 🔄 Responsabilidades futuras

A implementação do `IncidentInput` deverá ocorrer na tarefa **DG-103**.

Ela depende dos modelos e valores definidos anteriormente.

### Dependências

```text
DOMAIN_ENUMS
     │
     ├── Severity
     └── EvidenceType
              │
              ▼
        EVIDENCE_MODEL
              │
              ▼
        IncidentInput
```

### DG-103 deverá implementar

- modelo Pydantic;
- campos obrigatórios;
- campos opcionais;
- coleção de `Evidence`;
- parsing de timestamps;
- validação de `initial_severity`;
- validação de IDs de evidência duplicados;
- rejeição de campos não suportados quando definido pelo contrato;
- serialização previsível;
- testes unitários.

---

## 🧭 Princípio do contrato

O `IncidentInput` deve permanecer:

- explícito;
- pequeno;
- previsível;
- validável;
- serializável;
- rastreável;
- independente da orquestração.

---

> 📥 O `IncidentInput` define a fronteira de entrada do **AI Data Governance Agent** e garante que os incidentes sejam representados de maneira estruturada antes de qualquer análise automatizada.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)
