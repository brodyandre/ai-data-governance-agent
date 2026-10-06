# 🧾 Contrato do Modelo de Evidência — Evidence

Este documento define o contrato técnico do modelo de domínio `Evidence` utilizado pelo **AI Data Governance Agent**.

A implementação correspondente está planejada na tarefa:

```text
DG-102 — Modelo Evidence
```

O modelo será posteriormente implementado utilizando **Pydantic 2**.

Este contrato refina a definição conceitual inicialmente apresentada em:

➡️ [`INCIDENT_INPUT.md`](INCIDENT_INPUT.md)

e depende dos enums definidos em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

---

<a id="sumario"></a>

## 📑 Sumário

- [Objetivo](#objetivo)
- [Nome do modelo](#nome-modelo)
- [Estrutura](#estrutura)
- [Campos](#campos)
- [evidence_id](#evidence-id)
- [evidence_type](#evidence-type)
- [source](#source)
- [description](#description)
- [value](#value)
- [collected_at](#collected-at)
- [reliability](#reliability)
- [metadata](#metadata)
- [Evidência mínima válida](#minima-valida)
- [Exemplo completo](#exemplo-completo)
- [Campos extras](#campos-extras)
- [Normalização de strings](#normalizacao)
- [Validação de enums](#validacao-enums)
- [Serialização](#serializacao)
- [IDs duplicados](#ids-duplicados)
- [Falhas de validação](#falhas-validacao)
- [Testes obrigatórios](#testes)
- [Limites de escopo](#limites)
- [Dependências](#dependencias)
- [Critérios de aceite](#criterios)
- [Responsabilidades adiadas](#adiadas)

---

<a id="objetivo"></a>

## 🎯 Objetivo

O modelo `Evidence` representa uma unidade individual e rastreável de informação técnica, analítica, de negócio ou de governança associada a um incidente.

Exemplos de evidências:

- resultado de validação de Data Quality;
- relatório de pipeline;
- resultado de reconciliação;
- log;
- regra de negócio;
- política de governança;
- observação de analista;
- métrica;
- amostra de dataset.

A evidência é um dos elementos centrais de rastreabilidade do projeto.

Componentes posteriores deverão ser capazes de referenciar uma evidência por meio de um identificador estável:

```text
evidence_id
```

### Princípio

```text
Evidência
   │
   ├── possui origem
   ├── possui tipo
   ├── pode possuir valor
   ├── pode possuir confiabilidade
   └── pode ser referenciada por outras estruturas
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="nome-modelo"></a>

## 🐍 Nome do modelo

Classe Python planejada:

```text
Evidence
```

Estrutura prevista:

```text
src/
└── ai_data_governance_agent/
    └── domain/
        ├── __init__.py
        ├── enums.py
        └── evidence.py
```

Testes previstos:

```text
tests/
└── domain/
    ├── test_enums.py
    └── test_evidence.py
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="estrutura"></a>

## 🏗️ Estrutura

Visão conceitual:

```text
Evidence
   │
   ├── evidence_id
   ├── evidence_type
   ├── source
   ├── description
   ├── value
   ├── collected_at
   ├── reliability
   └── metadata
```

O modelo deve validar apenas uma evidência por vez.

Responsabilidades que dependem de uma coleção de evidências pertencem a camadas posteriores.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="campos"></a>

## 📦 Campos

O modelo deverá suportar os seguintes campos:

| Campo | Tipo | Obrigatório |
|---|---|---|
| `evidence_id` | `str` | Sim |
| `evidence_type` | `EvidenceType` | Sim |
| `source` | `str` | Sim |
| `description` | `str \| None` | Não |
| `value` | valor JSON-compatible ou `None` | Não |
| `collected_at` | `datetime \| None` | Não |
| `reliability` | `EvidenceReliability \| None` | Não |
| `metadata` | objeto JSON-compatible | Não |

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidence-id"></a>

## 🆔 `evidence_id`

### Tipo

```text
str
```

### Obrigatório

**Sim**

### Objetivo

Fornecer um identificador estável que permita que outros objetos do domínio façam referência a essa evidência.

Exemplo:

```text
EV-001
```

### Regras

O campo:

- deve estar presente;
- deve conter texto diferente de espaços em branco;
- deve ter espaços iniciais removidos;
- deve ter espaços finais removidos;
- é case-sensitive;
- não deve ser reescrito automaticamente;
- não precisa ser único no nível de uma instância individual de `Evidence`.

### Exemplos válidos

```text
EV-001
DQ-CHECK-17
PIPELINE-REPORT-2026-10-06
```

### Exemplos inválidos

```text
""
"   "
null
```

### Normalização permitida

Entrada:

```text
"  EV-001  "
```

Resultado:

```text
"EV-001"
```

### Normalização proibida

Entrada:

```text
"ev-001"
```

não deve ser automaticamente convertida para:

```text
"EV-001"
```

O conteúdo semântico do identificador deve ser preservado.

### Unicidade

O modelo `Evidence` não deve detectar sozinho IDs duplicados.

Esse tipo de validação exige acesso a uma coleção.

Exemplo:

```text
Evidence A → EV-001
Evidence B → EV-001
```

A duplicidade deverá ser tratada no nível de:

- `IncidentInput`;
- coleção de evidências;
- ou ferramenta responsável pela organização das evidências.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidence-type"></a>

## 🏷️ `evidence_type`

### Tipo

```text
EvidenceType
```

### Obrigatório

**Sim**

### Objetivo

Representar o tipo semântico da evidência.

Os valores permitidos são definidos em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

### Valores atuais

```text
data_quality_check
pipeline_report
validation_result
reconciliation_result
log
business_rule
governance_policy
analyst_observation
metric
dataset_sample
```

### Exemplos válidos

```text
reconciliation_result
pipeline_report
metric
```

### Exemplos inválidos

```text
reconciliation
report
DataQuality
unknown_type
```

Valores não suportados devem ser rejeitados.

O sistema não deve converter silenciosamente uma entrada inválida para outro tipo.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="source"></a>

## 🔗 `source`

### Tipo

```text
str
```

### Obrigatório

**Sim**

### Objetivo

Identificar a origem da evidência.

A origem pode representar:

- sistema;
- pipeline;
- documento;
- relatório;
- usuário;
- componente;
- processo automatizado;
- catálogo;
- mecanismo de validação.

### Exemplos

```text
pipeline-report
great-expectations
sales-reconciliation-job
governance-policy-catalog
data-engineer-observation
```

### Regras

O campo:

- deve estar presente;
- deve conter texto diferente de espaços em branco;
- deve ter espaços iniciais removidos;
- deve ter espaços finais removidos;
- deve preservar seu valor semântico original.

### Exemplos inválidos

```text
""
"   "
null
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="description"></a>

## 📝 `description`

### Tipo

```text
str | None
```

### Obrigatório

**Não**

### Objetivo

Fornecer uma explicação curta e legível sobre o que a evidência representa.

Exemplo:

```text
Raw and silver record counts differ.
```

### Regras

Quando presente:

- remover espaços iniciais;
- remover espaços finais;
- rejeitar conteúdo composto apenas por espaços.

Exemplo inválido:

```text
"   "
```

O campo pode ser omitido quando:

- o valor for autoexplicativo;
- a origem não fornecer descrição;
- não houver conteúdo adicional relevante.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="value"></a>

## 📊 `value`

### Tipo

Valor JSON-compatible ou:

```text
None
```

### Obrigatório

**Não**

### Objetivo

Armazenar o valor efetivo ou resumido associado à evidência.

O contrato conceitual original utilizava a ideia:

```text
value or content
```

Para o MVP, o campo canônico será exclusivamente:

```text
value
```

Não será introduzido um campo separado chamado:

```text
content
```

Essa decisão evita duas propriedades diferentes representando o mesmo conceito.

---

## Tipos suportados

O valor pode conter dados compatíveis com JSON:

- string;
- inteiro;
- ponto flutuante;
- boolean;
- lista;
- objeto;
- null.

### String

```json
"orders RAW=400 SILVER=388"
```

### Inteiro

```json
30
```

### Float

```json
0.075
```

### Boolean

```json
true
```

### Objeto

```json
{
  "raw_count": 400,
  "silver_count": 388,
  "difference": 12
}
```

### Lista

```json
[
  "ORD-000038",
  "ORD-000144",
  "ORD-000148"
]
```

### Regra

O modelo `Evidence` não deve interpretar o significado do campo `value`.

Exemplo:

```text
Evidence
   │
   └── value
          │
          └── apenas armazena
```

A interpretação pertence a:

- ferramentas determinísticas;
- regras de domínio;
- etapas posteriores do workflow.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="collected-at"></a>

## 🕒 `collected_at`

### Tipo

```text
datetime | None
```

### Obrigatório

**Não**

### Objetivo

Representar o momento em que a evidência foi coletada ou gerada.

### Exemplo serializado

```text
2026-10-05T20:00:00Z
```

A implementação com Pydantic poderá aceitar uma string ISO 8601 válida e convertê-la para `datetime`.

### Exemplos válidos

```text
2026-10-05T20:00:00Z
2026-10-05T17:00:00-03:00
```

### Exemplo inválido

```text
yesterday evening
```

Valores temporais malformados devem ser rejeitados.

### Timezone

A `DG-102` não introduzirá regras adicionais de timezone.

Políticas específicas de timezone só deverão ser criadas posteriormente se houver necessidade concreta.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="reliability"></a>

## 📈 `reliability`

### Tipo

```text
EvidenceReliability | None
```

### Obrigatório

**Não**

### Objetivo

Representar a confiabilidade atribuída à evidência ou à sua fonte.

### Valores permitidos

```text
low
medium
high
```

Os valores são definidos em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

### Ausência de avaliação

Não existe um valor:

```text
unknown
```

para `EvidenceReliability`.

Quando a confiabilidade não tiver sido avaliada, o campo deve permanecer:

```text
None
```

ou ausente.

### Princípio

```text
Reliability informada
        ≠
Reliability não avaliada
```

Essa distinção deve ser preservada.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="metadata"></a>

## 🗂️ `metadata`

### Tipo

Objeto JSON-compatible.

### Obrigatório

**Não**

### Valor padrão

Objeto vazio:

```json
{}
```

### Objetivo

Armazenar atributos contextuais específicos da evidência que não justificam campos próprios no nível superior do modelo.

### Exemplo

```json
{
  "pipeline_run_id": "run-20261005-001",
  "dataset": "orders",
  "layer": "silver"
}
```

Outro exemplo:

```json
{
  "rule_id": "DQ-QUANTITY-001",
  "failed_records": 30
}
```

### Regra

O modelo `Evidence` não deve interpretar semanticamente os dados contidos em `metadata`.

### Segurança do valor padrão

O objeto padrão deve ser criado de forma segura.

A implementação não deve compartilhar a mesma instância mutável entre objetos diferentes.

Exemplo de comportamento esperado:

```text
Evidence A.metadata
        ≠
mesma instância mutável
        ≠
Evidence B.metadata
```

Uma alteração em `Evidence A.metadata` não deve modificar `Evidence B.metadata`.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="minima-valida"></a>

## ✅ Evidência mínima válida

Uma evidência estruturalmente válida exige apenas:

- `evidence_id`;
- `evidence_type`;
- `source`.

Exemplo:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "pipeline_report",
  "source": "sales-pipeline"
}
```

Esse comportamento é intencional.

### Princípio

```text
Estrutura válida
      ≠
Evidência suficiente
```

Uma evidência pode ser válida segundo o schema, mas insuficiente para sustentar uma conclusão.

A avaliação de suficiência pertence a etapas posteriores.

A `DG-102` não deve calcular suficiência de evidência.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="exemplo-completo"></a>

## 🧪 Exemplo completo

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "reconciliation_result",
  "source": "pipeline-report",
  "description": "Raw and silver record counts differ.",
  "value": {
    "raw_count": 400,
    "silver_count": 388,
    "difference": 12
  },
  "collected_at": "2026-10-05T20:00:00Z",
  "reliability": "high",
  "metadata": {
    "dataset": "orders",
    "layer": "silver"
  }
}
```

### Interpretação estrutural

O exemplo representa:

```text
Evidence EV-001
     │
     ├── tipo: reconciliation_result
     ├── origem: pipeline-report
     ├── diferença: 12
     ├── reliability: high
     └── dataset: orders
```

O modelo apenas valida e representa esses dados.

Ele não conclui automaticamente:

- causa raiz;
- impacto;
- severidade;
- recomendação.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="campos-extras"></a>

## 🚫 Campos extras

O modelo deverá rejeitar campos top-level que não estejam definidos neste contrato.

A configuração planejada em Pydantic deve possuir comportamento equivalente a:

```text
extra = "forbid"
```

### Exemplo inválido

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "unsupported_field": "value"
}
```

O campo:

```text
unsupported_field
```

não pertence ao contrato e deverá gerar erro de validação.

### Justificativa

Essa abordagem ajuda a detectar:

- payloads malformados;
- erros de integração;
- campos incorretos;
- alterações de contrato não documentadas.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="normalizacao"></a>

## ✂️ Normalização de strings

Os seguintes campos textuais top-level devem remover espaços no início e no final:

- `evidence_id`;
- `source`;
- `description`.

### Exemplo

Entrada:

```text
"  EV-001  "
```

Resultado:

```text
"EV-001"
```

### Regra

Somente whitespace externo deve ser removido.

O sistema não deve executar reescrita semântica.

Entrada:

```text
"ev-001"
```

não deve se transformar em:

```text
"EV-001"
```

Da mesma forma:

```text
"Pipeline Report"
```

não deve ser reescrito automaticamente como:

```text
"pipeline-report"
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="validacao-enums"></a>

## 🏷️ Validação de enums

O modelo deve utilizar os enums definidos pela `DG-101`.

Exemplo válido:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "reconciliation_result",
  "source": "pipeline-report",
  "reliability": "high"
}
```

Exemplo inválido:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "RECONCILIATION_RESULT",
  "source": "pipeline-report"
}
```

A validação deve permanecer case-sensitive.

### Fluxo

```text
Entrada
   │
   ▼
Valor existe no enum?
   │
 ┌─┴─┐
 │   │
Sim Não
 │   │
 ▼   ▼
Aceita Rejeita
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="serializacao"></a>

## 📤 Serialização

O modelo deve possuir serialização determinística.

Em modo JSON:

- enums devem utilizar seus valores string;
- datetimes devem utilizar representação compatível com ISO;
- dicionários devem permanecer objetos;
- listas devem permanecer listas;
- nomes de campos devem permanecer estáveis.

### Exemplo conceitual

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "reconciliation_result",
  "source": "pipeline-report",
  "description": "Raw and silver record counts differ.",
  "value": "orders RAW=400 SILVER=388",
  "collected_at": "2026-10-05T20:00:00Z",
  "reliability": "high",
  "metadata": {}
}
```

A `DG-102` não precisa adicionar encoders customizados se o comportamento padrão do Pydantic já satisfizer o contrato.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="ids-duplicados"></a>

## 🔁 IDs duplicados

A `DG-102` valida apenas uma instância de `Evidence`.

Por esse motivo, a tarefa não deve implementar detecção de identificadores duplicados.

Exemplo:

```text
Evidence A → evidence_id = EV-001

Evidence B → evidence_id = EV-001
```

Detectar esse problema exige conhecimento da coleção.

### Responsabilidade

```text
Evidence individual
        │
        └── não conhece outros objetos

Coleção de Evidence
        │
        └── pode detectar duplicidade
```

A implementação não deve utilizar:

- estado global;
- registro global de IDs;
- cache externo;
- banco de dados;

para tentar resolver duplicidade no modelo individual.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="falhas-validacao"></a>

## ❌ Falhas de validação

Os casos inválidos representativos devem incluir os seguintes cenários.

---

### `evidence_id` ausente

```json
{
  "evidence_type": "metric",
  "source": "monitoring"
}
```

Resultado esperado:

```text
REJEITADO
```

---

### `evidence_id` vazio

```json
{
  "evidence_id": "   ",
  "evidence_type": "metric",
  "source": "monitoring"
}
```

Resultado esperado:

```text
REJEITADO
```

---

### `evidence_type` inválido

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "report",
  "source": "monitoring"
}
```

Resultado esperado:

```text
REJEITADO
```

---

### `source` ausente

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric"
}
```

Resultado esperado:

```text
REJEITADO
```

---

### `source` vazio

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "   "
}
```

Resultado esperado:

```text
REJEITADO
```

---

### `reliability` inválida

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "reliability": "trusted"
}
```

Resultado esperado:

```text
REJEITADO
```

---

### `collected_at` malformado

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "collected_at": "yesterday"
}
```

Resultado esperado:

```text
REJEITADO
```

---

### Campo extra não suportado

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "confidence": 0.95
}
```

Resultado esperado:

```text
REJEITADO
```

O campo `confidence` não pertence ao modelo `Evidence`.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="testes"></a>

## 🧪 Testes obrigatórios

Os testes da `DG-102` devem verificar, no mínimo, os seguintes cenários.

### 1. Evidência mínima válida

Uma `Evidence` contendo apenas:

- `evidence_id`;
- `evidence_type`;
- `source`;

deve ser aceita.

---

### 2. Evidência completa válida

Todos os campos documentados devem poder ser utilizados simultaneamente.

---

### 3. `evidence_id` obrigatório

Ausência do campo deve falhar.

---

### 4. `evidence_id` vazio

Valor composto apenas por whitespace deve falhar.

---

### 5. `source` obrigatório

Ausência do campo deve falhar.

---

### 6. `source` vazio

Whitespace-only deve falhar.

---

### 7. `EvidenceType` válido

Valores documentados devem ser aceitos.

---

### 8. `EvidenceType` inválido

Valores não suportados devem ser rejeitados.

---

### 9. `EvidenceReliability` válida

Valores:

```text
low
medium
high
```

devem ser aceitos.

---

### 10. Reliability inválida

Exemplo:

```text
trusted
```

deve ser rejeitado.

---

### 11. Reliability omitida

O campo poderá ser omitido.

---

### 12. Description omitida

O campo poderá ser omitido.

---

### 13. Valores JSON-compatible

O campo `value` deverá aceitar exemplos representativos de:

- string;
- integer;
- float;
- boolean;
- list;
- object;
- null.

---

### 14. Datetime válido

Strings ISO 8601 válidas devem ser interpretadas corretamente.

---

### 15. Datetime inválido

Valores malformados devem ser rejeitados.

---

### 16. Metadata padrão

Quando omitida:

```text
metadata
```

deve resultar em objeto vazio.

---

### 17. Metadata não compartilhada

Objetos `Evidence` diferentes não devem compartilhar a mesma instância mutável de metadata.

---

### 18. Campos extras

Campos top-level não documentados devem ser rejeitados.

---

### 19. Serialização dos enums

Enums devem ser serializados utilizando seus valores string.

Exemplo:

```text
EvidenceType.RECONCILIATION_RESULT
```

deve gerar:

```text
reconciliation_result
```

---

### 20. Serialização previsível

A saída deve produzir estruturas compatíveis com JSON e comportamento determinístico.

---

## Requisitos dos testes

Os testes devem permanecer:

- determinísticos;
- offline;
- independentes de credenciais externas;
- independentes de rede;
- independentes de modelos de linguagem.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="limites"></a>

## 🚧 Limites de escopo

A `DG-102` deve permanecer uma tarefa pequena e focada.

Ela **não deve implementar**:

- coleta de múltiplas evidências;
- detecção de `evidence_id` duplicado;
- cálculo de suficiência de evidência;
- detecção de evidências conflitantes;
- score de evidência;
- inferência automática de reliability;
- análise de Data Quality;
- análise de impacto de negócio;
- `IncidentInput`;
- `AgentResponse`;
- regras de revisão humana;
- FastAPI;
- LangGraph;
- providers de modelos;
- armazenamento externo;
- banco de dados;
- busca vetorial.

Essas capacidades pertencem a tarefas posteriores.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="dependencias"></a>

## 🔗 Dependências

A implementação da `DG-102` depende da `DG-101`.

Isso ocorre porque o modelo `Evidence` utiliza:

```text
EvidenceType
EvidenceReliability
```

Fluxo de dependência:

```text
DG-101
DOMAIN_ENUMS
    │
    ├── EvidenceType
    └── EvidenceReliability
             │
             ▼
          DG-102
          Evidence
```

Portanto, a implementação do modelo `Evidence` deve começar somente depois que os enums necessários estiverem disponíveis no código.

A documentação pode ser preparada antecipadamente.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="criterios"></a>

## ✅ Critérios de aceite

A `DG-102` será considerada concluída quando:

- o modelo Pydantic `Evidence` existir;
- `evidence_id` for obrigatório;
- `evidence_id` for validado;
- `evidence_type` utilizar `EvidenceType`;
- `source` for obrigatório;
- `source` for validado;
- campos opcionais forem suportados;
- `reliability` utilizar `EvidenceReliability`;
- valores JSON-compatible forem suportados;
- datetime for validado;
- campos extras forem rejeitados;
- serialização for previsível;
- detecção de ID duplicado permanecer fora desse modelo;
- testes válidos e inválidos estiverem implementados;
- testes existentes continuarem aprovados.

### Quality gates

```bash
python -m pip check
ruff check .
ruff format --check .
pytest
```

Todos devem ser aprovados.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="adiadas"></a>

## ⏳ Responsabilidades adiadas

Algumas responsabilidades relacionadas a evidências são deliberadamente atribuídas a etapas posteriores.

---

### DG-103 — `IncidentInput`

Responsabilidades:

- coleção de objetos `Evidence`;
- validação no nível do incidente;
- detecção de identificadores de evidência duplicados.

Fluxo:

```text
Evidence
    │
    ▼
IncidentInput
    │
    └── valida coleção
```

---

### DG-201 — `evidence_collector`

Responsabilidades:

- normalização de evidências no contexto do incidente;
- organização das evidências;
- tratamento de duplicidades quando aplicável;
- tratamento de estruturas não suportadas;
- processamento de rastreabilidade.

---

### DG-501 a DG-503 — Guardrails

Responsabilidades:

- tratamento de conclusões sem suporte;
- comportamento com evidência insuficiente;
- validação de rastreabilidade.

---

## 🧭 Separação de responsabilidades

```text
Evidence
   │
   └── valida uma evidência
          │
          ▼
IncidentInput
   │
   └── valida coleção
          │
          ▼
evidence_collector
   │
   └── organiza e processa
          │
          ▼
Guardrails
   │
   └── validam uso das evidências
```

Essa separação reduz acoplamento e mantém cada componente com responsabilidade clara.

---

## 📌 Resumo do contrato

| Propriedade | Decisão |
|---|---|
| Modelo | `Evidence` |
| Framework | Pydantic 2 |
| ID obrigatório | Sim |
| Tipo obrigatório | Sim |
| Origem obrigatória | Sim |
| Description | Opcional |
| Value | Opcional |
| Datetime | Opcional |
| Reliability | Opcional |
| Metadata | Opcional |
| Campos extras | Rejeitados |
| Case-sensitive | Sim |
| IDs duplicados | Validados fora de `Evidence` |
| Análise de suficiência | Fora da DG-102 |
| Lógica analítica | Fora da DG-102 |

---

> 🧾 O modelo `Evidence` representa a unidade fundamental de rastreabilidade do **AI Data Governance Agent**, garantindo que informações utilizadas nas análises possuam identidade, origem e estrutura explícitas sem misturar validação de dados com interpretação analítica.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)
