# 📤 Contrato de Resposta do Agente — AgentResponse

Este documento define o contrato conceitual da resposta estruturada produzida pelo **AI Data Governance Agent**.

A implementação final utilizará **Pydantic** para validar e garantir a consistência deste contrato.

O objetivo é assegurar que toda análise produzida pelo agente seja:

- estruturada;
- rastreável;
- explícita quanto à incerteza;
- adequada para consumo por API;
- adequada para interface web;
- compatível com supervisão humana.

---

<a id="sumario"></a>

## 📑 Sumário

- [Objetivo](#objetivo)
- [Visão geral](#visao-geral)
- [incident_id](#incident-id)
- [classification](#classification)
- [severity](#severity)
- [executive_summary](#executive-summary)
- [evidence](#evidence)
- [business_impact](#business-impact)
- [root_cause_hypotheses](#root-cause-hypotheses)
- [recommended_actions](#recommended-actions)
- [governance_controls](#governance-controls)
- [confidence](#confidence)
- [human_review_required](#human-review-required)
- [human_review_reasons](#human-review-reasons)
- [Princípios da resposta](#principios)
- [Rastreabilidade de evidências](#rastreabilidade)
- [Comportamento com evidência insuficiente](#evidencia-insuficiente)
- [Supervisão humana](#supervisao-humana)
- [Exemplo completo](#exemplo)
- [Responsabilidades futuras](#responsabilidades)

---

<a id="objetivo"></a>

## 🎯 Objetivo

O `AgentResponse` representa a saída formal da análise de um incidente.

Ele deve consolidar:

- identificação do incidente;
- classificação;
- severidade;
- resumo executivo;
- evidências;
- impacto de negócio;
- hipóteses de causa raiz;
- ações recomendadas;
- controles de governança;
- nível de confiança;
- necessidade de revisão humana.

O contrato deve permitir que uma pessoa ou sistema consumidor compreenda não apenas **o que o agente concluiu**, mas também **quais evidências sustentam essas conclusões**.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="visao-geral"></a>

## 🏗️ Visão geral

Estrutura conceitual:

```text
AgentResponse
     │
     ├── incident_id
     ├── classification
     ├── severity
     ├── executive_summary
     ├── evidence
     ├── business_impact
     ├── root_cause_hypotheses
     ├── recommended_actions
     ├── governance_controls
     ├── confidence
     ├── human_review_required
     └── human_review_reasons
```

A resposta deve permanecer consistente com os contratos de entrada e com as evidências efetivamente disponíveis.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="incident-id"></a>

## 🆔 `incident_id`

### Objetivo

Identificar o incidente analisado.

O valor deve corresponder ao mesmo identificador recebido no `IncidentInput`.

Exemplo:

```text
DE-101
```

### Regra

O sistema não deve criar um novo identificador para o incidente durante a análise.

Fluxo esperado:

```text
IncidentInput.incident_id
          │
          ▼
      AgentResponse
          │
          └── mesmo incident_id
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="classification"></a>

## 🧭 `classification`

### Objetivo

Representar a classificação principal atribuída ao incidente.

Os valores normalizados são definidos em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

Valores atuais:

```text
data_quality
schema
integrity
reconciliation
freshness
pipeline_failure
governance
unknown
```

### Princípio

A classificação deve ser sustentada pelas evidências disponíveis.

Quando não houver evidência suficiente para uma classificação específica, o domínio permite:

```text
unknown
```

Entretanto, `unknown` não deve ser utilizado para mascarar entradas inválidas ou falhas de validação.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="severity"></a>

## 🚦 `severity`

### Objetivo

Representar a severidade normalizada atribuída ao incidente após a análise.

Valores:

```text
low
medium
high
critical
```

As regras detalhadas de severidade estão definidas em:

➡️ [`SEVERITY_AND_HUMAN_REVIEW.md`](SEVERITY_AND_HUMAN_REVIEW.md)

### Princípio

A severidade deve considerar fatores como:

- impacto;
- amplitude;
- criticidade dos dados;
- risco de negócio;
- governança;
- urgência;
- evidências disponíveis.

A classificação final não deve depender exclusivamente de comportamento não determinístico do modelo.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="executive-summary"></a>

## 📝 `executive_summary`

### Objetivo

Fornecer um resumo curto e compreensível da situação.

O resumo deve comunicar, sempre que possível:

- o que aconteceu;
- por que isso importa;
- qual é o nível atual de risco;
- se existe impacto confirmado ou potencial;
- se revisão humana é necessária.

### Características esperadas

O resumo deve ser:

- conciso;
- objetivo;
- legível;
- baseado em evidências;
- livre de afirmações não sustentadas.

### Exemplo conceitual

```text
Data Quality validation removed records from the silver layer and may affect downstream sales analytics.
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidence"></a>

## 🧾 `evidence`

### Objetivo

Representar as evidências utilizadas para sustentar a análise.

As evidências devem utilizar os mesmos identificadores definidos no incidente recebido.

Exemplo:

```text
EV-001
EV-002
EV-003
```

O contrato detalhado de uma evidência está definido em:

➡️ [`EVIDENCE_MODEL.md`](EVIDENCE_MODEL.md)

### Princípio de rastreabilidade

Conclusões importantes devem, sempre que possível, referenciar explicitamente as evidências que as sustentam.

```text
Evidence EV-001
      │
      ├── BusinessImpact
      ├── RootCauseHypothesis
      └── RecommendedAction
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="business-impact"></a>

## 💼 `business_impact`

### Objetivo

Representar consequências confirmadas, potenciais ou ainda desconhecidas para o negócio.

O impacto deve distinguir claramente:

```text
confirmed
potential
unknown
```

Os estados são definidos em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

### Estrutura conceitual sugerida

```text
BusinessImpact
     │
     ├── status
     ├── description
     ├── affected_processes
     ├── affected_consumers
     ├── materiality
     └── supporting_evidence
```

---

### `status`

Representa se o impacto é:

- confirmado;
- potencial;
- desconhecido.

---

### `description`

Descrição do possível ou confirmado efeito de negócio.

---

### `affected_processes`

Processos de negócio possivelmente afetados.

Exemplo:

```json
[
  "sales analytics",
  "revenue reporting"
]
```

---

### `affected_consumers`

Consumidores, equipes ou sistemas downstream possivelmente afetados.

---

### `materiality`

Indicação conceitual da relevância ou materialidade do impacto.

A definição formal poderá ser refinada na implementação do modelo correspondente.

---

### `supporting_evidence`

Lista de IDs de evidências que sustentam a avaliação.

Exemplo:

```json
[
  "EV-001",
  "EV-004"
]
```

### Regra

Um impacto não deve ser marcado como `confirmed` sem evidências que sustentem essa classificação.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="root-cause-hypotheses"></a>

## 🧠 `root_cause_hypotheses`

### Objetivo

Representar explicações possíveis para o incidente.

Cada hipótese deve permanecer explicitamente identificada como hipótese enquanto não houver evidência suficiente para confirmação.

### Estrutura conceitual

```text
RootCauseHypothesis
     │
     ├── description
     ├── supporting_evidence
     ├── confidence
     └── status
```

### Estados iniciais planejados

```text
suspected
probable
confirmed
rejected
```

Esses estados serão formalizados durante a implementação da `DG-104`.

---

### `suspected`

Existe uma possibilidade razoável, mas o suporte ainda é limitado.

---

### `probable`

As evidências tornam a hipótese plausível e relativamente forte, sem confirmação definitiva.

---

### `confirmed`

A evidência disponível sustenta a causa de forma suficiente para tratá-la como confirmada.

---

### `rejected`

As evidências disponíveis contradizem ou descartam a hipótese.

---

## Regra fundamental

```text
Hipótese
   ≠
Fato confirmado
```

Uma hipótese só pode receber status:

```text
confirmed
```

quando houver evidência suficiente.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="recommended-actions"></a>

## 🛠️ `recommended_actions`

### Objetivo

Representar próximos passos sugeridos pelo sistema.

As recomendações possuem caráter **consultivo**.

### Estrutura conceitual

```text
RecommendedAction
     │
     ├── description
     ├── priority
     ├── rationale
     ├── requires_human_approval
     └── supporting_evidence
```

---

### `description`

Descrição objetiva da ação recomendada.

---

### `priority`

Valores previstos:

```text
low
medium
high
urgent
```

A fonte canônica está em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

---

### `rationale`

Explica por que a ação está sendo recomendada.

---

### `requires_human_approval`

Indica explicitamente se a ação necessita de aprovação humana antes de qualquer execução.

Valores:

```text
true
false
```

---

### `supporting_evidence`

Referências às evidências que sustentam a recomendação.

---

## Princípio de segurança

Prioridade não significa autorização.

```text
urgent
   │
   ▼
Alta prioridade
   │
   ✕
Não significa execução automática
```

Mesmo uma ação `urgent` pode exigir aprovação humana.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="governance-controls"></a>

## 🛡️ `governance_controls`

### Objetivo

Representar regras, políticas ou controles de governança relevantes para o incidente.

### Estrutura conceitual

```text
GovernanceControl
     │
     ├── control_id
     ├── title
     ├── description
     ├── source
     ├── relevance
     └── supporting_evidence
```

---

### `control_id`

Identificador estável do controle.

---

### `title`

Nome legível do controle ou política.

---

### `description`

Descrição do requisito ou regra.

---

### `source`

Origem da política ou controle.

---

### `relevance`

Explica por que o controle é relevante para o incidente.

---

### `supporting_evidence`

Evidências associadas ao vínculo entre o incidente e o controle.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="confidence"></a>

## 📊 `confidence`

### Objetivo

Representar o nível de confiança da avaliação geral.

A implementação inicial deverá utilizar valor numérico entre:

```text
0.0
```

e:

```text
1.0
```

### Interpretação

```text
0.0
│
│ nenhuma confiança significativa
│
├───────────────────────────────
│
│ confiança crescente
│
├───────────────────────────────
│
│ confiança máxima suportada
│
1.0
```

### Regra

O valor deve refletir:

- quantidade de evidências;
- qualidade das evidências;
- consistência;
- conflitos;
- lacunas de informação;
- força do suporte para as conclusões.

### Importante

Confidence não representa certeza absoluta.

Mesmo:

```text
1.0
```

significa apenas confiança máxima **dentro do conjunto de evidências disponível e das regras definidas pelo sistema**.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="human-review-required"></a>

## 👤 `human_review_required`

### Tipo conceitual

```text
bool
```

### Valores

```text
true
false
```

### Objetivo

Indicar se o incidente exige revisão por uma pessoa responsável.

A decisão deve seguir regras explícitas de governança.

Ela não deve depender de escolha arbitrária de um modelo.

As regras estão definidas em:

➡️ [`SEVERITY_AND_HUMAN_REVIEW.md`](SEVERITY_AND_HUMAN_REVIEW.md)

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="human-review-reasons"></a>

## 📋 `human_review_reasons`

### Objetivo

Explicar por que a revisão humana foi exigida.

Exemplos conceituais:

```text
high severity
critical severity
insufficient evidence
conflicting evidence
low confidence
possible governance exposure
material business impact
destructive recommendation
```

### Princípio

Sempre que:

```text
human_review_required = true
```

a resposta deve fornecer motivos compreensíveis e auditáveis.

Exemplo:

```json
{
  "human_review_required": true,
  "human_review_reasons": [
    "high severity",
    "potential material business impact"
  ]
}
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="principios"></a>

## ✅ Princípios da resposta

Uma resposta válida deve:

- respeitar o schema definido;
- preservar o `incident_id`;
- distinguir fatos de hipóteses;
- referenciar evidências;
- expor incerteza;
- evitar afirmações sem suporte;
- sinalizar evidência insuficiente;
- indicar revisão humana quando necessário;
- permanecer consultiva;
- ser serializável;
- possuir comportamento previsível.

---

## Separação conceitual

```text
Fato observado
      │
      ▼
Resultado determinístico
      │
      ▼
Hipótese
      │
      ▼
Recomendação
```

Cada nível deve permanecer semanticamente distinguível.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="rastreabilidade"></a>

## 🔗 Rastreabilidade de evidências

Conclusões importantes devem permitir responder:

- qual evidência sustenta esta conclusão?
- qual fonte produziu a evidência?
- a conclusão é observada, derivada ou hipotética?
- qual é o nível de confiança?
- existem evidências conflitantes?

### Exemplo

```text
EV-001
  │
  ▼
Finding
  │
  ▼
RootCauseHypothesis
  │
  ▼
RecommendedAction
```

Uma conclusão sem suporte suficiente deve ser:

- qualificada;
- rejeitada;
- ou marcada como incerta.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidencia-insuficiente"></a>

## ⚠️ Comportamento com evidência insuficiente

Quando as evidências disponíveis forem insuficientes, o agente não deve fabricar informação.

O comportamento esperado inclui:

- reduzir `confidence`;
- identificar informações ausentes;
- qualificar hipóteses;
- evitar conclusões não sustentadas;
- recomendar investigação adicional;
- exigir revisão humana quando aplicável.

### Fluxo conceitual

```text
Evidência insuficiente
        │
        ▼
Não fabricar informação
        │
        ▼
Reduzir confidence
        │
        ▼
Declarar limitações
        │
        ▼
Recomendar investigação adicional
        │
        ▼
Revisão humana quando necessária
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="supervisao-humana"></a>

## 👥 Supervisão humana

A resposta produzida pelo agente é **consultiva**.

O sistema não deve:

- declarar que uma recomendação já foi executada;
- sugerir que aprovação humana ocorreu quando não ocorreu;
- executar automaticamente ações críticas;
- executar automaticamente ações irreversíveis.

### Regra

Ações críticas ou irreversíveis exigem aprovação humana responsável.

```text
Recomendação crítica
        │
        ▼
requires_human_approval = true
        │
        ▼
Pessoa responsável
        │
        ▼
Decisão
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="exemplo"></a>

## 🧪 Exemplo completo

```json
{
  "incident_id": "DE-101",
  "classification": "data_quality",
  "severity": "high",
  "executive_summary": "Data Quality validation removed records from the silver layer and may affect downstream sales analytics.",
  "evidence": [
    {
      "evidence_id": "EV-001",
      "source": "pipeline-report"
    }
  ],
  "business_impact": {
    "status": "potential",
    "description": "Downstream sales metrics may be incomplete.",
    "affected_processes": [
      "sales analytics"
    ],
    "materiality": "medium",
    "supporting_evidence": [
      "EV-001"
    ]
  },
  "root_cause_hypotheses": [
    {
      "description": "Invalid item quantities caused records to fail validation.",
      "supporting_evidence": [
        "EV-001"
      ],
      "confidence": 0.95,
      "status": "probable"
    }
  ],
  "recommended_actions": [
    {
      "description": "Review rejected records and validate upstream quantity rules.",
      "priority": "high",
      "rationale": "Rejected records may be causing incomplete downstream analytics.",
      "requires_human_approval": false,
      "supporting_evidence": [
        "EV-001"
      ]
    }
  ],
  "governance_controls": [],
  "confidence": 0.90,
  "human_review_required": true,
  "human_review_reasons": [
    "high severity",
    "potential material business impact"
  ]
}
```

---

## 🔍 Leitura do exemplo

O exemplo indica que:

- o incidente analisado é `DE-101`;
- a classificação é `data_quality`;
- a severidade é `high`;
- existe evidência identificada como `EV-001`;
- o impacto de negócio é considerado `potential`;
- existe uma hipótese de causa raiz com status `probable`;
- existe recomendação de prioridade `high`;
- a confiança geral é `0.90`;
- revisão humana é obrigatória.

Importante: a hipótese não foi marcada como `confirmed`.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="responsabilidades"></a>

## 🔄 Responsabilidades futuras

A implementação formal dos modelos de resposta está planejada para:

```text
DG-104 — Modelos AgentResponse
```

A tarefa deverá contemplar estruturas como:

```text
BusinessImpact
RootCauseHypothesis
RecommendedAction
GovernanceControl
AgentResponse
```

### Dependências conceituais

```text
DOMAIN_ENUMS
      │
      ├── IncidentClassification
      ├── Severity
      ├── BusinessImpactStatus
      └── ActionPriority
                │
                ▼
        AgentResponse models
```

---

## 📌 Requisitos previstos para DG-104

A implementação deverá garantir:

- tipos explícitos;
- `confidence` limitada ao intervalo permitido;
- severity normalizada;
- classification normalizada;
- `human_review_required` booleano;
- `human_review_reasons` representável;
- evidências de suporte referenciáveis;
- hipóteses com status explícito;
- ações com prioridade explícita;
- serialização previsível;
- campos extras tratados de acordo com o contrato;
- testes válidos e inválidos.

---

## 🧭 Princípio central

A resposta final deve permitir que um avaliador compreenda:

```text
O que aconteceu?
      │
Por que importa?
      │
Quais evidências existem?
      │
O que é fato?
      │
O que é hipótese?
      │
Qual é a confiança?
      │
O que deve ser feito?
      │
Uma pessoa precisa revisar?
```

---

## 📌 Resumo do contrato

| Campo | Finalidade |
|---|---|
| `incident_id` | Identificar o incidente |
| `classification` | Classificar o tipo de incidente |
| `severity` | Representar severidade |
| `executive_summary` | Resumir a situação |
| `evidence` | Preservar evidências |
| `business_impact` | Representar impacto de negócio |
| `root_cause_hypotheses` | Representar hipóteses |
| `recommended_actions` | Recomendar próximos passos |
| `governance_controls` | Apresentar controles relevantes |
| `confidence` | Representar incerteza/confiança |
| `human_review_required` | Indicar revisão humana |
| `human_review_reasons` | Explicar a decisão de revisão |

---

> 📤 O `AgentResponse` é a fronteira de saída do **AI Data Governance Agent** e deve transformar a análise interna em uma resposta estruturada, rastreável, explicável e adequada à tomada de decisão responsável.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)
