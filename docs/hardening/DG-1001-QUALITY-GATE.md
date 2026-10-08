# DG-1001 — Quality gate completo

## Objetivo

Registrar a validação técnica executada durante o hardening final do
AI Data Governance Agent antes do code freeze.

Este documento registra evidências do quality gate local e os critérios que
devem permanecer verdes no CI antes do merge da DG-1001.

## Baseline

- branch: `chore/dg-1001-quality-gate`;
- commit-base: `888955b`;
- Python: `3.12.14`;
- Node.js: `20.20.2`;
- npm: `10.8.2`.

## Quality gate local

| Verificação | Resultado |
|---|---|
| `python -m pip check` | aprovado, sem dependências quebradas |
| `ruff check .` | aprovado |
| `ruff format --check .` | aprovado, 78 arquivos conformes |
| `pytest` | 576 testes aprovados |
| `npm test` | 18 testes aprovados |
| evaluation runner | 7 de 7 cenários aprovados |
| `git diff --check` | aprovado |

## Avaliação determinística

O runner de avaliação aprovou os sete cenários versionados.

As métricas funcionais reportadas no gate foram:

- `schema_valid_rate`: 100%;
- `severity_accuracy`: 100%;
- `evidence_traceability_rate`: 100%;
- `unsupported_rejection_rate`: 100%;
- `human_review_accuracy`: 100%;
- `tool_execution_success_rate`: 100%;
- `test_pass_rate`: 100%.

Esses percentuais descrevem exclusivamente o dataset determinístico versionado.
Eles não representam desempenho universal de um LLM real em produção.

A latência permanece dependente do ambiente e não integra o critério funcional
de aprovação.

## Instalação em ambiente limpo

Foi criado um ambiente virtual temporário independente da `.venv` de
desenvolvimento.

Nesse ambiente foram executados:

```bash
python3.12 -m venv /tmp/ai-data-governance-dg1001-venv
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip check
pytest
```

Resultado:

- instalação editável concluída com sucesso;
- dependências consistentes;
- 576 testes aprovados no ambiente limpo.

O ambiente temporário foi removido após a validação.

## Resíduos e arquivos temporários

Foram auditados, fora de `.git`, `.venv` e `web/node_modules`:

- `__pycache__`;
- `.pytest_cache`;
- `.ruff_cache`;
- `*.egg-info`;
- `*.pyc`;
- `*.pyo`;
- `*.log`;
- `*.tmp`;
- `*.bak`;
- `.DS_Store`.

Os caches gerados durante os testes foram removidos.

A auditoria final não encontrou resíduos locais elegíveis e `git ls-files`
não encontrou artefatos temporários versionados.

## Estado da árvore Git

Ao término das validações locais, a árvore Git estava limpa antes da criação
deste registro de hardening.

## CI e critério de merge

A DG-1001 somente deve ser integrada à `main` se todos os quality gates do
GitHub Actions estiverem verdes no pull request.

O merge do PR com CI aprovado constitui a confirmação final do critério
de CI desta entrega.

## Conclusão

Os critérios locais da DG-1001 foram atendidos:

- qualidade e formatação aprovadas;
- testes Python e web aprovados;
- avaliação determinística aprovada;
- instalação limpa reproduzida;
- ausência de resíduos confirmada;
- árvore Git validada.

A integração permanece condicionada ao CI verde do pull request.
