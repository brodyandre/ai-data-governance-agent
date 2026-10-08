# DG-903 — Roteiro de apresentação

## Objetivo

Fornecer uma fala principal de aproximadamente cinco a seis minutos para a
demonstração do AI Data Governance Agent no Challenge da Imersão de Agentes de
IA para Negócios — Alura + Oracle Next Education (ONE).

O roteiro deve ser usado como guia de apresentação, não como texto que precise
ser lido mecanicamente.

---

## 1. Abertura e problema de negócio

Olá. Este projeto é o AI Data Governance Agent.

Ele foi criado para apoiar a investigação de incidentes de dados em um ponto
em que Engenharia de Dados, Data Quality, negócio e governança se encontram.

Em uma investigação real, normalmente não recebemos uma resposta pronta.
Recebemos informações fragmentadas: contagens entre camadas, resultados de
qualidade, regras de negócio, evidências de reconciliação e observações de
analistas.

O problema não é apenas descobrir que dois números são diferentes.

Também precisamos entender se a diferença representa um erro, qual pode ser o
impacto de negócio, quais evidências sustentam a conclusão e se uma decisão
pode ser automatizada ou precisa de revisão humana.

A proposta do agente é organizar essa investigação em uma resposta estruturada,
rastreável e conservadora.

---

## 2. Incidente recebido

Para demonstrar isso, eu preparei dois cenários baseados em investigações de um
projeto Lakehouse do meu portfólio.

O primeiro é o DE-101.

Na Silver existem 1000 itens de pedido e, na Gold, a `fct_sales` possui 937
registros.

Olhando apenas para os números, alguém poderia concluir que 63 registros foram
perdidos.

Mas a investigação mostra que 30 itens possuem quantidade inválida e outros 33
itens estão associados a 12 pedidos com status inválido.

Ou seja, a diferença de 1000 para 937 é explicada pelas regras atuais de
elegibilidade.

O segundo cenário é o DE-102.

Nesse caso, Gold e Analytics reconciliam exatamente em R$ 1.416.127,23.

O problema não é uma divergência técnica. O problema é que não existe uma
definição formal de quais status de pedido devem compor uma métrica chamada
receita.

---

## 3. Evidências e análise

Na interface eu consigo carregar os cenários já estruturados e inspecionar as
evidências utilizadas pelo agente.

No DE-101, a análise preserva a sequência quantitativa:

1000 itens na Silver, menos 30 itens com quantidade inválida, menos 33 itens
ligados a pedidos inválidos, resultando em 937 registros elegíveis na Gold.

O ponto importante é que o agente não chama isso automaticamente de perda de
dados.

No DE-102, a evidência mostra que Gold e Analytics possuem o mesmo valor:
R$ 1.416.127,23.

Como exercício investigativo, considerando somente `paid` e `shipped`, o valor
seria R$ 548.323,22.

A diferença é R$ 867.804,01, aproximadamente 61,28%.

Mas o agente não pode transformar esse número em uma afirmação de perda
financeira, porque não existe uma regra de negócio formal dizendo que somente
esses dois status representam receita.

---

## 4. Ferramentas e arquitetura

O workflow é orquestrado com LangGraph e utiliza quatro ferramentas
determinísticas principais.

O `evidence_collector` organiza e preserva as evidências.

O `quality_analyzer` avalia sinais de Data Quality.

O `business_impact_analyzer` relaciona o incidente a possíveis impactos de
negócio.

E o `policy_retriever` recupera controles de governança aplicáveis.

A API foi construída com FastAPI e os contratos de entrada e saída são
validados com Pydantic.

Na demonstração controlada, as etapas que dependem de provider utilizam
respostas determinísticas versionadas. Isso torna a execução reproduzível e
permite avaliar o comportamento do workflow sem depender de uma API externa.

---

## 5. Limites do raciocínio baseado em IA

Um princípio central do projeto é que uma hipótese não deve ser promovida a
fato sem evidência suficiente.

No DE-101, o sistema não deve afirmar que houve perda entre Raw e Silver,
porque essa afirmação seria falsa em relação às evidências.

No DE-102, ele também não deve afirmar que 61,28% da receita está errada ou que
R$ 867.804,01 representam perda financeira.

Esses valores fazem parte de um cenário investigativo, não de uma conclusão
contábil.

O objetivo aqui não é fazer a IA parecer mais confiante.

É fazer a solução reconhecer os limites do que realmente pode afirmar.

---

## 6. Controles de governança

Para isso, a solução utiliza contratos estruturados, rastreabilidade entre
claims e evidências, rejeição de afirmações sem suporte, classificação de
severidade, avaliação de impacto, controles de governança e regras explícitas
de revisão humana.

A pergunta que eu quero conseguir responder não é apenas "qual foi a resposta
do agente?".

Eu também quero conseguir responder "qual evidência sustenta essa resposta?".

Esse requisito torna a análise mais auditável e reduz o risco de conclusões
plausíveis, mas não sustentadas.

---

## 7. Supervisão humana

O agente é consultivo.

Ele não executa automaticamente mudanças críticas.

No DE-101, se o negócio decidir que a regra de elegibilidade da Gold deve ser
alterada, essa decisão precisa ser validada pelos responsáveis.

No DE-102, a situação é ainda mais clara: uma mudança na definição de receita
não pode ser decidida pelo modelo.

Primeiro o negócio precisa formalizar o significado da métrica e aprovar a
regra. Só depois uma mudança no SQL pode ser implementada.

Quanto maior o risco, maior a necessidade de supervisão humana.

---

## 8. Resultados mensuráveis

Além da demonstração visual, o projeto possui uma avaliação determinística com
sete cenários versionados.

No gate utilizado para esta demonstração, os sete cenários foram aprovados.

As métricas de validade de schema, severidade, rastreabilidade de evidências,
rejeição de claims sem suporte, revisão humana, execução das ferramentas e
aprovação dos cenários ficaram em 100% dentro desse dataset controlado.

A suíte de engenharia também possui 576 testes Python e 18 testes da interface
web aprovados, além dos quality gates de lint, formatação e integração contínua.

É importante deixar claro que esses 100% não representam uma taxa universal de
acerto em produção.

Eles representam o comportamento esperado sobre o conjunto determinístico e
versionado que foi utilizado para validar o projeto.

---

## 9. Valor de negócio e encerramento

O valor principal da solução não é substituir o engenheiro, o analista ou o
responsável pelo negócio.

É tornar a investigação mais consistente, rastreável e segura.

No DE-101, o agente ajuda a evitar uma correção precipitada em um pipeline
quando a diferença está explicada pelas regras atuais.

No DE-102, ele ajuda a evitar que uma hipótese investigativa seja transformada
em uma conclusão financeira ou em uma mudança prematura de SQL.

Então, em vez de simplesmente perguntar "qual é o erro?", o projeto procura
responder:

O que sabemos?

Quais evidências sustentam isso?

O que ainda é hipótese?

Qual pode ser o impacto?

Quais controles se aplicam?

E quem precisa tomar a decisão?

Essa combinação de Engenharia de Dados, Inteligência Artificial, Data Quality,
governança e human-in-the-loop é o valor central do AI Data Governance Agent.

---

## Versão curta de contingência — aproximadamente 90 segundos

Este projeto é o AI Data Governance Agent, criado para apoiar investigações de
incidentes de dados com rastreabilidade, governança e supervisão humana.

Eu demonstro dois cenários.

No DE-101, a Silver possui 1000 itens e a Gold possui 937. A diferença de 63
registros parece inicialmente uma perda, mas as evidências mostram 30 itens com
quantidade inválida e 33 itens associados a pedidos inválidos. O agente,
portanto, evita classificar automaticamente essa diferença como falha do
pipeline.

No DE-102, Gold e Analytics reconciliam em R$ 1.416.127,23. Um cenário
investigativo com `paid + shipped` resulta em R$ 548.323,22, uma diferença de
R$ 867.804,01 ou 61,28%. O agente não chama isso de perda financeira porque não
existe contrato semântico formal definindo quais status representam receita.

O workflow combina LangGraph, ferramentas determinísticas, FastAPI, Pydantic,
guardrails e regras de revisão humana.

A avaliação versionada possui sete cenários aprovados, com 576 testes Python e
18 testes web no gate atual.

O objetivo não é deixar a IA tomar a decisão final. É organizar evidências,
explicitar incertezas e indicar quando uma decisão precisa permanecer sob
responsabilidade humana.

---

## Frases de apoio para memorização

Problema: informações fragmentadas podem produzir investigações inconsistentes.

DE-101: diferença de registros não significa automaticamente perda de dados.

DE-102: consistência técnica não garante definição semântica de negócio.

IA: hipótese sem evidência não deve ser apresentada como fato.

Governança: uma conclusão precisa ser rastreável às evidências que a sustentam.

Supervisão: decisões críticas continuam sob responsabilidade humana.

Resultado: sete cenários determinísticos aprovados no gate da demonstração.

Valor: investigar com mais consistência sem automatizar decisões que exigem
contexto e responsabilidade humana.
