# DG-903 — Narrativa da demonstração

## Objetivo

Definir a narrativa oficial de demonstração do AI Data Governance Agent para
o Challenge da Imersão de Agentes de IA para Negócios — Alura + Oracle Next
Education (ONE).

A demonstração deve mostrar valor técnico e de negócio sem atribuir ao agente
capacidades que não foram implementadas ou avaliadas.

A mensagem central é:

> O agente organiza evidências, aplica controles de governança, produz uma
> análise rastreável e ajuda uma pessoa a tomar uma decisão mais informada,
> sem transformar hipóteses em fatos nem executar automaticamente mudanças
> críticas.

## Princípio da demonstração

A apresentação deve diferenciar claramente:

- evidência observada;
- resultado de ferramenta determinística;
- hipótese;
- recomendação;
- decisão que exige supervisão humana.

Os cenários DE-101 e DE-102 são utilizados em conjunto para demonstrar que o
agente não depende de um único tipo de incidente.

---

## 1. Problema de negócio

Incidentes de dados normalmente são investigados a partir de informações
fragmentadas, como contagens entre camadas, resultados de Data Quality,
reconciliações, regras de negócio, observações de analistas e políticas de
governança.

O desafio não é apenas encontrar uma diferença técnica. Também é necessário
entender se ela representa erro, qual pode ser o impacto, quais evidências
sustentam a conclusão e quando a decisão precisa permanecer com uma pessoa.

O AI Data Governance Agent organiza essas informações em uma resposta
estruturada, rastreável e sujeita a controles de governança.

---

## 2. Incidente recebido

### DE-101 — Elegibilidade entre Silver e Gold

A Silver contém 1000 `order_items`, enquanto a `gold.fct_sales` contém 937
registros.

Uma leitura superficial poderia interpretar os 63 registros de diferença como
perda de dados. A investigação, porém, estabelece que:

- 30 itens possuem quantidade inválida;
- 33 itens pertencem a 12 pedidos com status inválido;
- não existe perda entre Raw, Bronze e Silver;
- não existem perdas adicionais nos JOINs com clientes ou produtos.

O desafio do agente é distinguir uma diferença explicada pelas regras atuais
de elegibilidade de uma perda inesperada.

### DE-102 — Semântica da métrica de receita

Gold e Analytics publicam exatamente `R$ 1.416.127,23`, portanto não existe
divergência matemática entre essas camadas.

A investigação identifica uma lacuna de governança: não existe contrato
semântico formal definindo quais status de pedido devem compor uma métrica
denominada `revenue`.

Como cenário investigativo, `paid + shipped` resulta em `R$ 548.323,22`.
A diferença para a receita atualmente publicada é `R$ 867.804,01`, ou cerca
de `61,28%`.

Esse número não representa perda financeira comprovada nem erro técnico
comprovado.

---

## 3. Evidências disponíveis

No DE-101, as evidências permitem reconciliar:

```text
Silver order_items: 1000
- quantidade inválida: 30
= itens válidos: 970
- itens ligados a pedidos inválidos: 33
= Gold fct_sales: 937
```

No DE-102, as evidências mostram:

```text
Gold fct_sales: R$ 1.416.127,23
Analytics:      R$ 1.416.127,23
Resultado: reconciliação técnica correta
```

Ao mesmo tempo, não existe uma regra formal determinando quais status devem
representar receita reconhecida. A ausência dessa regra também é informação
relevante para a análise.

---

## 4. Ferramentas utilizadas

O workflow utiliza quatro ferramentas determinísticas principais:

| Ferramenta | Responsabilidade |
| --- | --- |
| `evidence_collector` | Organizar e preservar evidências |
| `quality_analyzer` | Avaliar sinais de Data Quality |
| `business_impact_analyzer` | Avaliar impacto potencial de negócio |
| `policy_retriever` | Recuperar controles de governança aplicáveis |

O LangGraph orquestra as etapas e a resposta segue contratos estruturados
validados por Pydantic.

A separação entre ferramentas determinísticas e camada de modelo mantém partes
críticas do comportamento testáveis e reproduzíveis.

---

## 5. Limites do raciocínio baseado em IA

A demonstração não apresenta o modelo como fonte absoluta de verdade.

O agente deve permanecer dentro das evidências disponíveis e não elevar uma
hipótese a fato sem suporte suficiente.

No DE-101, não deve afirmar que houve perda entre Raw e Silver.

No DE-102, não deve afirmar que:

- `R$ 867.804,01` representam perda financeira;
- `61,28%` da receita está incorreta;
- somente `paid` e `shipped` constituem receita;
- existe defeito técnico comprovado.

A avaliação automatizada atual utiliza `FakeProvider` para garantir
reprodutibilidade. Isso valida contratos, workflow, ferramentas e guardrails,
mas não mede a qualidade de um LLM real em produção.

---

## 6. Controles de governança

A solução aplica controles destinados a reduzir conclusões não sustentadas:

- contratos estruturados de entrada e saída;
- rastreabilidade entre claims e evidências;
- rejeição de claims sem suporte;
- classificação explícita de severidade;
- avaliação de impacto de negócio;
- consulta a controles de governança;
- níveis de confiança;
- regras de revisão humana.

O objetivo não é apenas produzir uma resposta plausível, mas uma resposta que
possa ser inspecionada e questionada.

---

## 7. Supervisão humana

O agente possui caráter consultivo e não executa automaticamente ações críticas
de remediação.

No DE-101, uma eventual mudança nas regras de publicação da Gold exige
validação dos responsáveis pelo negócio.

No DE-102, alterar a semântica de uma métrica financeira exige definição e
aprovação humana antes de qualquer modificação no SQL.

Princípio:

```text
Maior risco
    ↓
Maior necessidade de supervisão humana
```

A IA ajuda a estruturar a decisão, mas não substitui a responsabilidade de quem
possui autoridade sobre a regra de negócio.

---

## 8. Resultados mensuráveis

No gate utilizado na preparação da demonstração:

- 7 de 7 cenários determinísticos foram aprovados;
- `schema_valid_rate`: 100%;
- `severity_accuracy`: 100%;
- `evidence_traceability_rate`: 100%;
- `unsupported_rejection_rate`: 100%;
- `human_review_accuracy`: 100%;
- `tool_execution_success_rate`: 100%;
- `test_pass_rate`: 100%;
- 576 testes Python foram aprovados;
- 19 testes da interface web foram aprovados;
- lint, formatação e CI foram aprovados.

Esses números medem o dataset determinístico versionado e a implementação
atual. Eles não representam taxa de acerto universal do agente em incidentes
reais.

`response_latency` é medida, mas depende do ambiente e não participa do
critério funcional de aprovação.

---

## 9. Valor de negócio

O valor principal da solução não está em automatizar uma decisão crítica, mas
em tornar a investigação mais consistente, auditável e segura.

No DE-101, o agente ajuda a evitar uma correção desnecessária quando a diferença
é explicada pelas regras atuais de elegibilidade.

No DE-102, ajuda a evitar que uma hipótese investigativa seja convertida
prematuramente em conclusão financeira ou alteração de SQL.

A solução demonstra potencial para:

- reduzir interpretações inconsistentes de incidentes;
- tornar evidências e conclusões rastreáveis;
- acelerar a organização inicial de uma investigação;
- explicitar incertezas;
- identificar decisões que dependem do negócio;
- reduzir risco de remediações precipitadas;
- apoiar colaboração entre Engenharia de Dados, Analytics e Governança.

---

## Mensagem final da demonstração

O AI Data Governance Agent não foi construído apenas para responder
"qual é o erro?".

Ele foi construído para ajudar a responder:

```text
O que sabemos?
Quais evidências sustentam isso?
O que ainda é hipótese?
Qual pode ser o impacto?
Quais controles se aplicam?
Quem precisa tomar a decisão?
```

Essa combinação de Engenharia de Dados, IA, rastreabilidade, governança e
supervisão humana é o valor central demonstrado pelo projeto.
