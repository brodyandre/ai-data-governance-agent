# Avaliação determinística

A avaliação do AI Data Governance Agent utiliza os cenários versionados da
DG-701 e o `FakeProvider`.

O objetivo é medir o comportamento do workflow de forma reproduzível e sem
dependência de APIs externas, credenciais ou disponibilidade de um modelo real.

## Execução

A avaliação completa pode ser executada com:

```bash
python -m ai_data_governance_agent.evaluation
```

O formato padrão é um resumo legível para uso durante desenvolvimento,
demonstrações e revisão do projeto.

A saída JSON continua disponível com:

```bash
python -m ai_data_governance_agent.evaluation --format json
```

Um relatório Markdown reutilizável no README ou na apresentação pode ser
gerado com:

```bash
python -m ai_data_governance_agent.evaluation --format markdown --output reports/evaluation/latest.md
```

## Métricas

### `schema_valid_rate`

Proporção de cenários que produzem uma resposta final válida segundo o contrato
`AgentResponse`.

`respostas válidas / total de cenários`

### `severity_accuracy`

Proporção de cenários em que a severidade final produzida pelo workflow
corresponde à severidade esperada no dataset.

`severidades corretas / total de cenários`

### `evidence_traceability_rate`

Proporção agregada de claims que exigem suporte e que referenciam evidências
válidas existentes no incidente.

`claims rastreáveis / claims que exigem suporte`

Claims que não exigem evidência pelas regras de governança não entram no
denominador. Quando nenhum claim exige suporte, a rastreabilidade é considerada
`1.0`.

### `unsupported_rejection_rate`

Proporção dos cenários adversariais marcados com
`unsupported_claim_rejection_expected=true` em que o workflow impede que a
afirmação não suportada preserve um nível de certeza indevido.

`rejeições corretas / cenários adversariais aplicáveis`

### `human_review_accuracy`

Proporção de cenários em que a decisão final `human_review_required`
corresponde à decisão esperada.

`decisões corretas / total de cenários`

### `tool_execution_success_rate`

Proporção das etapas determinísticas de ferramenta concluídas com sucesso.

As etapas medidas são:

- `evidence_collected`;
- `quality_analyzed`;
- `business_impact_analyzed`;
- `policies_retrieved`.

`execuções de ferramenta concluídas / execuções esperadas`

### `response_latency`

Tempo médio, em milissegundos, para executar um cenário completo no ambiente
local.

A metodologia é reproduzível, mas o valor não é determinístico porque depende
de máquina, sistema operacional, carga e demais condições de execução.

Essa métrica não participa do critério funcional de aprovação do cenário.

### `test_pass_rate`

Proporção dos cenários que satisfazem todos os checks funcionais aplicáveis.

Um cenário é considerado aprovado quando:

- produz `AgentResponse` válido;
- mantém a classificação esperada;
- mantém a severidade esperada;
- produz a decisão esperada de revisão humana;
- mantém rastreabilidade integral dos claims que exigem suporte;
- executa todas as etapas determinísticas de ferramenta;
- rejeita corretamente claims sem suporte quando aplicável.

`cenários aprovados / total de cenários`

## Classificação

A correspondência de classificação é registrada em cada
`ScenarioEvaluationResult` como `classification_match`.

O backlog da DG-702 não define `classification_accuracy` como métrica agregada.
Por isso, a classificação participa do `test_pass_rate`, mas não cria uma nona
métrica agregada.

## Interpretação

Todas as taxas são normalizadas no intervalo de `0.0` a `1.0`.

- `1.0` = 100%
- `0.95` = 95%
- `0.80` = 80%

Para o dataset determinístico versionado, uma regressão funcional deve ser
visível tanto no resultado individual quanto nas métricas agregadas.

## Escopo

A avaliação determinística mede o comportamento do workflow, dos guardrails e
das ferramentas usando `FakeProvider`.

Avaliações de qualidade de um provider real, custo de tokens, latência de rede
ou variabilidade de LLM permanecem fora do escopo desta etapa.
