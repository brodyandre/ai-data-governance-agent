# DG-1102 — Validação final da demonstração e evidências

## Objetivo

Registrar a validação final da demonstração end-to-end do AI Data Governance Agent e das evidências visuais utilizadas na preparação da entrega.

## Baseline

- branch: `docs/dg-1102-demo-evidence-validation`;
- commit-base: `a9ec8f8`;
- data da validação: 08/10/2026;
- modo de demonstração: provider determinístico controlado;
- interface: Node.js + Express + EJS + Vanilla JavaScript;
- backend: FastAPI + LangGraph.

## Fluxo validado

Os cenários foram enviados pela rota pública da interface web:

```text
Interface Web :3000
       ↓
Express /api/analyze
       ↓
FastAPI :8001
       ↓
Workflow LangGraph
       ↓
Ferramentas determinísticas + guardrails
       ↓
Provider determinístico da demonstração
       ↓
AgentResponse
```

O provider determinístico é utilizado apenas para manter a demonstração reproduzível e não é apresentado como um LLM real em produção.

## DE-101 — Resultado validado

- HTTP 200;
- classificação: `reconciliation`;
- severidade: `medium`;
- confiança: 98%;
- revisão humana obrigatória;
- 4 evidências retornadas;
- 1 ação recomendada;
- 2 controles de governança retornados.

### Validação visual

A interface apresentou em PT-BR:

- classificação Reconciliação;
- severidade Média;
- revisão humana necessária;
- resumo executivo;
- hipótese confirmada;
- recomendação consultiva;
- aprovação humana obrigatória;
- controles DQ-001 e DQ-002;
- rastreabilidade pelas evidências `EV-DE101-*`.

## DE-102 — Resultado validado

- HTTP 200;
- classificação: `governance`;
- severidade: `high`;
- confiança: 88%;
- revisão humana obrigatória;
- 2 evidências retornadas;
- 1 ação recomendada;
- nenhum controle local de governança retornado.

A ausência de controle local no DE-102 é esperada. O catálogo atual recupera DQ-001, DQ-002 e DQ-003 somente quando existem findings compatíveis de Data Quality, reconciliação ou integridade. O cenário DE-102 representa uma lacuna semântica de governança e o sistema não deve inventar um controle inexistente.

### Validação visual

A interface apresentou em PT-BR:

- classificação Governança;
- severidade Alta;
- revisão humana necessária;
- motivos de revisão humana traduzidos;
- resumo executivo;
- hipótese confirmada com 96% de confiança;
- recomendação de alta prioridade;
- aprovação humana obrigatória;
- rastreabilidade por `EV-DE102-METRIC` e `EV-DE102-RULE`.

Identificadores técnicos, nomes de campos, datasets e IDs permanecem em inglês por fazerem parte dos contratos técnicos da aplicação.

## Correção de apresentação realizada

Durante a validação foi identificado que textos produzidos pelo provider determinístico eram exibidos em inglês na interface.

A correção foi aplicada somente na camada de apresentação web, preservando o dataset de avaliação e os contratos internos.

Foi adicionada proteção automatizada para a localização PT-BR do resumo executivo, hipótese, recomendação, justificativa e motivos de revisão humana.

## Quality gates

- `ruff check .`: aprovado;
- `ruff format --check .`: aprovado, 83 arquivos conformes;
- `pytest`: 576 testes aprovados;
- testes web: 19 de 19 aprovados;
- avaliação determinística: 7 de 7 cenários aprovados;
- métricas funcionais da avaliação: 100% no dataset versionado;
- `git diff --check`: aprovado.

## Evidências visuais aprovadas

Foram validadas capturas em formato desktop contendo:

- DE-101 — resultado, classificação, severidade, confiança, revisão humana e resumo executivo;
- DE-101 — hipótese, recomendação e controles de governança;
- DE-102 — resultado, classificação, severidade, confiança, revisão humana e resumo executivo;
- DE-102 — hipótese e recomendação.

As imagens finais serão organizadas e selecionadas no pacote de submissão da DG-1103.

## Critérios de aceite

- DE-101 validado end-to-end: atendido;
- DE-102 validado end-to-end: atendido;
- execução reproduzível pelo runbook: atendido;
- transparência sobre provider determinístico: atendido;
- screenshots ou evidências de apresentação validadas: atendido;
- narrativa compatível com o comportamento observado: atendido.

## Conclusão

A demonstração final está funcional, reproduzível e compatível com a narrativa oficial do projeto. Os dois cenários canônicos estão prontos para utilização na apresentação e na submissão.
