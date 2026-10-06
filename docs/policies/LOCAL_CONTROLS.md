# Catálogo Local de Controles de Governança

Este catálogo faz parte do AI Data Governance Agent.

Os controles são exemplos internos para demonstração,
testes determinísticos e rastreabilidade.

Não representam políticas corporativas efetivamente
aprovadas nem obrigações legais verificadas.

---

<a id="dq-001"></a>

## DQ-001 — Validação de qualidade de registros

Objetivo: identificar e acompanhar registros inválidos
ou falhas em validações de qualidade.

Sinais associados:
- invalid_records
- validation_failures

Critério: o controle é recuperado quando há finding
estruturado compatível e evidência rastreável.

---

<a id="dq-002"></a>

## DQ-002 — Reconciliação de volumes

Objetivo: verificar divergências entre contagens
esperadas e observadas ou entre camadas de dados.

Sinais associados:
- reconciliation_divergence
- count_divergence

Critério: o controle é recuperado quando há
divergência de contagem comprovada por finding.

---

<a id="dq-003"></a>

## DQ-003 — Integridade e relacionamentos

Objetivo: acompanhar falhas de relacionamento e
violações de integridade nos dados.

Sinais associados:
- missing_relationships
- integrity_inconsistencies

Critério: o controle é recuperado quando existem
findings estruturados de integridade.

---

## Princípios

- Não inferir uma violação regulatória automaticamente.
- Não inventar controles inexistentes no catálogo.
- Preservar a origem documental de cada controle.
- Preservar os IDs das evidências que sustentam o vínculo.
- Não recuperar controles na ausência de findings compatíveis.
- Manter execução offline e determinística.
