# DG-1103 — Pacote de submissão

## Objetivo

Centralizar o material final necessário para apresentar e submeter o **AI Data Governance Agent** de forma consistente, curta e verificável.

Este documento funciona como fonte única para descrição do projeto, links públicos, evidências, screenshots e texto de apresentação.

---

## Identidade do projeto

**Nome:** AI Data Governance Agent

**Repositório público:** https://github.com/brodyandre/ai-data-governance-agent

**Autor:** Luiz André de Souza

**Contexto:** projeto de portfólio desenvolvido no contexto da Imersão de Agentes de IA para Negócios — Alura + Oracle Next Education (ONE).

---

## Descrição curta

Agente de IA para investigação estruturada de incidentes de dados, combinando Data Quality, impacto de negócio, governança, rastreabilidade de evidências, guardrails e human-in-the-loop.

---

## Descrição intermediária

O AI Data Governance Agent organiza evidências técnicas e de negócio para apoiar a investigação de incidentes de dados. O workflow utiliza LangGraph, FastAPI, Pydantic e ferramentas determinísticas para analisar Data Quality, impacto de negócio e controles de governança, produzindo hipóteses e recomendações rastreáveis. Guardrails impedem que conclusões sem suporte sejam tratadas como fatos, e decisões críticas permanecem sob revisão humana.

---

## Descrição completa para submissão

O **AI Data Governance Agent** foi criado para apoiar investigações de incidentes de dados em cenários nos quais informações técnicas, regras de negócio e controles de governança estão distribuídos em diferentes fontes.

A solução recebe um incidente estruturado, organiza as evidências, executa análises determinísticas de Data Quality e impacto de negócio, recupera controles de governança e utiliza um workflow com LangGraph para produzir hipóteses, recomendações, nível de confiança e necessidade de revisão humana.

Um princípio central do projeto é separar claramente evidência observada, resultado determinístico, hipótese e recomendação. Claims sem suporte são rejeitados ou qualificados por guardrails, e o agente não executa automaticamente remediações críticas.

A aplicação possui backend em Python com FastAPI e Pydantic, workflow com LangGraph, interface web em Node.js, Express, EJS e JavaScript, testes automatizados e CI com GitHub Actions.

A demonstração utiliza dois cenários canônicos. No DE-101, uma diferença entre Silver e Gold é reconciliada pelas regras de elegibilidade, evitando classificar rejeições esperadas como perda de dados. No DE-102, Gold e Analytics reconciliam tecnicamente o mesmo valor, mas a investigação identifica uma lacuna de governança na definição semântica da métrica de receita.

O projeto foi validado com 576 testes Python, 19 testes web e 7 de 7 cenários determinísticos de avaliação aprovados. As métricas funcionais desse dataset controlado ficaram em 100%. Esses resultados medem o comportamento do workflow, ferramentas e guardrails no conjunto versionado e não representam uma taxa universal de acerto de um LLM em produção.

O objetivo do agente não é substituir engenheiros, analistas ou responsáveis pelo negócio. O valor está em tornar a investigação mais consistente, auditável, rastreável e segura, indicando explicitamente quando uma decisão precisa permanecer sob responsabilidade humana.

---

## Problema de negócio

Investigações de incidentes de dados frequentemente dependem de informações fragmentadas:

- resultados de Data Quality;
- diferenças entre camadas;
- reconciliações;
- regras de negócio;
- logs;
- políticas de governança;
- observações de analistas.

Sem organização e rastreabilidade, uma diferença técnica pode ser interpretada incorretamente como erro, uma hipótese pode ser promovida a fato e uma remediação pode ser executada antes da validação do negócio.

---

## Solução

O workflow implementado:

1. recebe e valida o incidente;
2. organiza as evidências;
3. analisa Data Quality;
4. avalia impacto de negócio;
5. recupera controles de governança;
6. produz hipóteses e recomendações;
7. valida rastreabilidade e claims;
8. calcula confiança;
9. determina necessidade de revisão humana;
10. retorna uma resposta estruturada.

---

## Diferenciais

- evidência, hipótese e recomendação são tratadas como conceitos distintos;
- conclusões relevantes preservam rastreabilidade;
- ferramentas determinísticas executam tarefas verificáveis fora da camada de geração;
- guardrails rejeitam claims sem suporte;
- human-in-the-loop é parte explícita do contrato;
- o provider da demonstração é determinístico para garantir reprodutibilidade;
- a arquitetura mantém provider, workflow, ferramentas, API e interface desacoplados;
- testes e avaliação não dependem de credenciais externas.

---

## Stack principal

- Python 3.12;
- FastAPI;
- Pydantic;
- LangGraph;
- Node.js;
- Express;
- EJS;
- Vanilla JavaScript;
- pytest;
- Ruff;
- GitHub Actions.

---

## Cenários oficiais de demonstração

### DE-101 — Elegibilidade Silver → Gold

Fatos principais:

- Silver: 1000 itens;
- 30 itens com quantidade inválida;
- 970 itens válidos;
- 33 itens associados a 12 pedidos inválidos;
- Gold `fct_sales`: 937 registros;
- diferença explicada pelas regras atuais de elegibilidade;
- classificação da demonstração: reconciliação;
- severidade: média;
- confiança: 98%;
- revisão humana necessária.

Mensagem principal:

> Diferença de registros não significa automaticamente perda de dados.

### DE-102 — Governança da semântica de receita

Fatos principais:

- Gold e Analytics: R$ 1.416.127,23;
- reconciliação técnica correta;
- `paid + shipped` como cenário investigativo: R$ 548.323,22;
- diferença investigativa: R$ 867.804,01;
- aproximadamente 61,28%;
- não representa perda financeira comprovada;
- ausência de contrato semântico formal para receita;
- classificação da demonstração: governança;
- severidade: alta;
- confiança: 88%;
- revisão humana necessária.

Mensagem principal:

> Consistência técnica não garante definição semântica de negócio.

---

## Evidências técnicas validadas

- 576 testes Python aprovados;
- 19 testes da interface web aprovados;
- 7 de 7 cenários determinísticos aprovados;
- métricas funcionais em 100% para o dataset versionado;
- lint aprovado;
- formatação aprovada;
- CI aprovado;
- DE-101 validado end-to-end;
- DE-102 validado end-to-end;
- interface de demonstração validada em PT-BR;
- revisão humana e rastreabilidade verificadas visualmente.

Os resultados de 100% são restritos ao dataset determinístico controlado e não devem ser apresentados como desempenho universal de um modelo em produção.

---

## Screenshots selecionados

Manter um conjunto pequeno e objetivo de evidências.

### 1. DE-101 — Visão geral

Deve mostrar:

- `EVAL-DE-101`;
- classificação Reconciliação;
- severidade Média;
- confiança 98%;
- revisão humana necessária;
- resumo executivo.

Nome sugerido:

`01-de101-overview.png`

### 2. DE-101 — Hipótese, recomendação e controles

Deve mostrar:

- hipótese confirmada;
- confiança da hipótese;
- recomendação;
- aprovação humana;
- evidências de suporte;
- controles DQ-001 e DQ-002.

Nome sugerido:

`02-de101-hypothesis-recommendation.png`

### 3. DE-102 — Visão geral

Deve mostrar:

- `EVAL-DE-102`;
- classificação Governança;
- severidade Alta;
- confiança 88%;
- revisão humana necessária;
- resumo executivo.

Nome sugerido:

`03-de102-overview.png`

### 4. DE-102 — Hipótese e recomendação

Deve mostrar:

- hipótese confirmada;
- confiança 96%;
- recomendação de alta prioridade;
- aprovação humana;
- evidências `EV-DE102-METRIC` e `EV-DE102-RULE`;
- ausência de controle inventado.

Nome sugerido:

`04-de102-hypothesis-recommendation.png`

Para uma submissão que aceite poucas imagens, priorizar as imagens 2 e 4 porque concentram hipótese, recomendação, evidência e human-in-the-loop.

---

## Texto curto para apresentação

> O AI Data Governance Agent apoia investigações de incidentes de dados organizando evidências, analisando Data Quality e impacto de negócio, recuperando controles de governança e produzindo hipóteses e recomendações rastreáveis. A solução utiliza guardrails para evitar conclusões sem suporte e mantém decisões críticas sob revisão humana.

---

## Pitch de aproximadamente 60 segundos

O AI Data Governance Agent foi criado para tornar investigações de incidentes de dados mais consistentes e auditáveis.

Em vez de entregar apenas uma resposta, ele organiza as evidências, executa análises de Data Quality e impacto de negócio, recupera controles de governança e produz hipóteses e recomendações com rastreabilidade.

Eu demonstro dois cenários. No DE-101, uma diferença entre Silver e Gold é explicada pelas regras de elegibilidade, evitando uma conclusão incorreta de perda de dados. No DE-102, Gold e Analytics reconciliam tecnicamente, mas falta uma definição formal para a semântica da receita.

O ponto central é que o agente não promove hipótese a fato sem evidência e não automatiza decisões críticas. Quanto maior o risco, maior a necessidade de supervisão humana.

---

## Links finais

- Repositório: https://github.com/brodyandre/ai-data-governance-agent
- README principal: https://github.com/brodyandre/ai-data-governance-agent#readme
- Cenário DE-101: https://github.com/brodyandre/ai-data-governance-agent/blob/main/docs/scenarios/DE-101.md
- Cenário DE-102: https://github.com/brodyandre/ai-data-governance-agent/blob/main/docs/scenarios/DE-102.md
- Avaliação: https://github.com/brodyandre/ai-data-governance-agent/blob/main/docs/EVALUATION.md
- Runbook: https://github.com/brodyandre/ai-data-governance-agent/blob/main/docs/demo/LIVE_DEMO_RUNBOOK.md
- Roteiro de apresentação: https://github.com/brodyandre/ai-data-governance-agent/blob/main/docs/demo/PRESENTATION_SCRIPT.md

---

## Transparência sobre IA e provider

A demonstração controlada utiliza um provider determinístico nas etapas dependentes de geração.

Isso é intencional:

- mantém a execução reproduzível;
- evita dependência de credenciais externas;
- permite validar workflow, ferramentas e guardrails;
- evita apresentar resultados de um LLM real sem avaliação específica.

A integração com provider real permanece uma evolução opcional e não é requisito para demonstrar o comportamento implementado.

---

## Materiais de apoio

- narrativa: [DEMO_NARRATIVE.md](../demo/DEMO_NARRATIVE.md);
- roteiro: [PRESENTATION_SCRIPT.md](../demo/PRESENTATION_SCRIPT.md);
- execução: [LIVE_DEMO_RUNBOOK.md](../demo/LIVE_DEMO_RUNBOOK.md);
- validação da demonstração: [DG-1102-DEMO-EVIDENCE-VALIDATION.md](DG-1102-DEMO-EVIDENCE-VALIDATION.md).

---

## Checklist da submissão

- [x] descrição curta preparada;
- [x] descrição completa preparada;
- [x] problema e solução descritos;
- [x] stack documentada;
- [x] diferenciais documentados;
- [x] URL pública do repositório validada;
- [x] links técnicos principais selecionados;
- [x] screenshots de DE-101 e DE-102 selecionados;
- [x] texto curto de apresentação preparado;
- [x] pitch de contingência preparado;
- [x] transparência sobre provider determinístico registrada;
- [ ] confirmar os campos exatos exigidos pelo formulário oficial do Challenge;
- [ ] confirmar se o formulário exige upload de imagens, vídeo ou URL adicional;
- [ ] copiar o conteúdo final para o formulário oficial e revisar antes do envio.

---

## Pendência externa

Os campos exatos do formulário oficial de submissão não estão registrados no repositório.

Antes de marcar a DG-1103 como concluída, o formulário da plataforma deve ser conferido para confirmar:

- limites de caracteres;
- campos obrigatórios;
- quantidade de screenshots;
- necessidade de vídeo;
- necessidade de link adicional;
- formato de entrega.

Nenhuma exigência não verificada deve ser presumida.

---

## Estado

O pacote técnico e textual está preparado.

A conclusão da DG-1103 depende apenas da conferência dos requisitos exatos do formulário oficial e da associação dos materiais selecionados aos campos exigidos.
