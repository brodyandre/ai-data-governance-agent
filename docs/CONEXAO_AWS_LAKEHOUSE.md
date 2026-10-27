# Como o AI Data Governance Agent se relaciona com o AWS Lakehouse

> **Resumo:** são dois projetos independentes de portfólio. A conexão entre eles, hoje, é **documental e baseada em cenários de investigação versionados**. Não existe comunicação automática, pipeline entre repositórios ou acesso contínuo ao ambiente do Lakehouse.

## A história completa em quatro etapas

| Etapa | Onde ocorre | Evidência verificável |
| --- | --- | --- |
| **1. Produção e tratamento de dados** | [AWS Lakehouse Engineering Lab](https://github.com/brodyandre/aws-lakehouse-engineering-lab) | Jobs PySpark, camadas Raw/Bronze/Silver/Gold, Airflow, SQL e Data Quality |
| **2. Investigação técnica de comportamentos do pipeline** | [Relatórios de incidentes do Lakehouse](https://github.com/brodyandre/aws-lakehouse-engineering-lab/tree/main/docs/incidents) | Contagens, reconciliação, regras de elegibilidade e questionamentos sobre métricas |
| **3. Adaptação dessas investigações para demonstrações reproduzíveis** | [Cenários deste agente](scenarios/) e [dataset de avaliação](../src/ai_data_governance_agent/evaluation/dataset.py) | Entradas estruturadas e evidências de DE-101 e DE-102, explicitamente associadas às fontes originais |
| **4. Análise assistida e resposta estruturada** | Este projeto: [workflow LangGraph](../src/ai_data_governance_agent/workflow/graph.py) e [contrato da resposta](contracts/AGENT_RESPONSE.md) | Classificação, severidade, hipóteses, recomendações, rastreabilidade e sinalização de revisão humana |

## De onde vêm os casos

| Caso | Relatório original do AWS Lakehouse | Cenário do agente | Mensagem correta |
| --- | --- | --- | --- |
| **DE-101** | [Investigação da divergência Raw/Silver/Gold](https://github.com/brodyandre/aws-lakehouse-engineering-lab/blob/main/docs/incidents/de-101-raw-silver-divergence.md) | [DE-101](scenarios/DE-101.md) | Dos **1.000** itens na Silver, **937** chegam à Gold após regras de elegibilidade. A diferença de **63** itens é explicada por **30** quantidades inválidas e **33** itens associados a pedidos inválidos; isso não comprova perda acidental de dados. |
| **DE-102** | [Investigação da semântica de receita](https://github.com/brodyandre/aws-lakehouse-engineering-lab/blob/main/docs/incidents/de-102-analytics-revenue-status.md) | [DE-102](scenarios/DE-102.md) | Gold e Analytics reconciliam **R$ 1.416.127,23**. O problema investigado é a ausência de uma definição formal de quais status integram a métrica de receita. Uma comparação alternativa é **hipotética**, não uma perda financeira comprovada. |

As investigações de origem ocorreram em um **laboratório com dados sintéticos**, não em produção empresarial. As entradas de demonstração são adaptações explícitas e versionadas; o agente não fez sozinho a descoberta ou a extração dessas investigações do GitHub.

## Existem duas conexões diferentes

### Conexão entre projetos: documental

```text
AWS Lakehouse (processamento de dados sintéticos)
    ↓
Relatórios de investigações DE-101 e DE-102
    ↓  adaptação em cenários/fixtures versionados; NÃO há API entre repositórios
AI Data Governance Agent (entrada IncidentInput)
    ↓
Análise, evidências, hipóteses, recomendações e revisão humana
```

**O que existe:** referências aos relatórios originais, cenários de demonstração, evidências estruturadas e casos do dataset determinístico.

**O que não existe:** leitura automática de bases, consultas ao Trino ou MinIO do Lakehouse, publicação de eventos, sincronização contínua, mudança remota de SQL ou correção automática do pipeline.

### Conexão dentro do agente: integração de software real

```text
Navegador → Interface Node/Express → POST /api/analyze
                                         ↓
                         POST /api/v1/incidents/analyze (FastAPI)
                                         ↓
                         Workflow LangGraph e ferramentas
                                         ↓
                         AgentResponse estruturada
                                         ↓
                         Interface e decisão com supervisão humana
```

A rota Express encaminha a requisição à API conforme [`web/src/app.js`](../web/src/app.js). A API invoca o workflow somente quando um provider é fornecido; na [configuração padrão](../src/ai_data_governance_agent/api/app.py), retorna **503 / `provider_not_configured`** caso contrário.

Para os cenários DE-101 e DE-102, o [runbook de demonstração](demo/LIVE_DEMO_RUNBOOK.md) prepara **um provider determinístico**, que fornece respostas controladas às etapas de geração de hipóteses e recomendações. As demais etapas — validações, ferramentas determinísticas e guardrails — são executadas pelo workflow. Isso **não equivale** a usar um LLM externo real nem demonstra uma integração produtiva com o AWS Lakehouse.

## O que é demonstrado para o negócio

- **Evidência antes da hipótese:** permite conferir quais fatos sustentam a análise.
- **Impacto potencial, não prejuízo inventado:** especialmente relevante no caso DE-102.
- **Controles e limites de confiança:** evita elevar conclusões sem suporte a fatos.
- **Decisão responsável:** recomendações críticas indicam necessidade de aprovação humana; o sistema não executa mudanças críticas automaticamente.

## Como verificar

1. Leia as investigações originais nos links da tabela de casos.
2. Compare-as com os cenários [DE-101](scenarios/DE-101.md) e [DE-102](scenarios/DE-102.md).
3. Consulte as [capturas no README](../README.md#cenarios), que mostram saídas demonstrativas, e o [runbook reproduzível](demo/LIVE_DEMO_RUNBOOK.md).
4. Consulte [testes e avaliação](EVALUATION.md) para entender o comportamento reproduzível e seus limites.

O objetivo dessa conexão é demonstrar **continuidade entre Engenharia de Dados e Governança de IA**, sem alegar que dois projetos independentes já constituem um produto integrado em produção.
