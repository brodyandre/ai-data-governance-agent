# 🛡️ Regras de Severidade e Revisão Humana

Este documento define as regras conceituais iniciais utilizadas pelo **AI Data Governance Agent** para:

- classificar a severidade de um incidente;
- interpretar confiança;
- identificar situações de maior risco;
- determinar quando revisão humana responsável é obrigatória.

Essas regras deverão ser convertidas posteriormente em **lógica determinística e testes automatizados**.

---

<a id="sumario"></a>

## 📑 Sumário

- [Objetivo](#objetivo)
- [Níveis de severidade](#niveis-severidade)
- [LOW](#low)
- [MEDIUM](#medium)
- [HIGH](#high)
- [CRITICAL](#critical)
- [Princípios de avaliação](#avaliacao)
- [Escalonamento de severidade](#escalonamento)
- [Revisão humana](#revisao-humana)
- [Regras obrigatórias](#regras-obrigatorias)
- [Limite inicial de confidence](#confidence-threshold)
- [Interpretação de confidence](#confidence)
- [Evidência insuficiente](#evidencia-insuficiente)
- [Evidência conflitante](#evidencia-conflitante)
- [Impacto material de negócio](#impacto-material)
- [Exposição de governança](#governanca)
- [Ações destrutivas ou irreversíveis](#acoes-destrutivas)
- [Princípio conservador](#principio-conservador)
- [Governança determinística](#governanca-deterministica)
- [Casos de decisão](#casos)
- [Critérios previstos para implementação](#implementacao)

---

<a id="objetivo"></a>

## 🎯 Objetivo

A severidade e a revisão humana são controles centrais do projeto.

O sistema deve ser capaz de responder duas perguntas diferentes:

```text
Qual é a gravidade do incidente?
```

e:

```text
Uma pessoa responsável precisa revisar esta situação?
```

Essas perguntas estão relacionadas, mas não são equivalentes.

Um incidente pode possuir:

```text
severity = medium
```

e ainda exigir:

```text
human_review_required = true
```

por motivos como:

- baixa confiança;
- evidência insuficiente;
- evidência conflitante;
- recomendação destrutiva;
- risco de governança.

Da mesma forma, alta confiança não elimina a necessidade de revisão humana em situações críticas.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="niveis-severidade"></a>

## 🚦 Níveis de severidade

Os níveis normalizados são:

```text
low
medium
high
critical
```

A fonte canônica dos valores está definida em:

➡️ [`DOMAIN_ENUMS.md`](DOMAIN_ENUMS.md)

Ordem conceitual:

```text
LOW
 │
 ▼
MEDIUM
 │
 ▼
HIGH
 │
 ▼
CRITICAL
```

A classificação deve considerar impacto técnico, impacto de negócio, governança, incerteza e contexto operacional.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="low"></a>

## 🟢 LOW

### Características típicas

Um incidente `low` pode apresentar:

- impacto técnico limitado;
- ausência de impacto material de negócio conhecido;
- nenhum dataset crítico afetado;
- ausência de preocupação regulatória;
- ausência de exposição relevante de governança;
- remediação simples;
- evidências de boa qualidade;
- baixo risco operacional.

### Interpretação

Um incidente de baixa severidade normalmente pode ser tratado sem intervenção urgente.

Exemplo conceitual:

```text
Problema localizado
      +
Baixo impacto
      +
Evidência confiável
      +
Remediação simples
      ↓
LOW
```

### Revisão humana

Se nenhuma outra regra obrigatória for ativada, uma severidade `low` pode resultar em:

```text
human_review_required = false
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="medium"></a>

## 🟡 MEDIUM

### Características típicas

Um incidente `medium` pode apresentar:

- degradação mensurável de Data Quality;
- impacto downstream limitado;
- problema recuperável em pipeline ou dados;
- ausência de forte exposição regulatória;
- ausência de grande risco de governança;
- usuários ou processos ainda operacionais;
- remediação necessária, mas não urgente.

### Interpretação

A severidade `medium` indica que o incidente requer atenção, porém ainda não representa risco operacional material.

Fluxo conceitual:

```text
Problema relevante
      +
Impacto limitado
      +
Operação ainda funcional
      ↓
MEDIUM
```

### Revisão humana

Pode ou não ser necessária.

Exemplos que podem tornar a revisão obrigatória:

- `confidence < 0.70`;
- evidência insuficiente;
- evidências conflitantes;
- recomendação destrutiva;
- possível problema de governança.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="high"></a>

## 🟠 HIGH

### Características típicas

Um incidente `high` pode apresentar:

- impacto material downstream;
- dataset analítico ou operacional importante afetado;
- perda significativa de registros;
- corrupção de dados;
- inconsistências relevantes;
- múltiplos consumidores afetados;
- múltiplos sistemas afetados;
- métricas de negócio potencialmente incorretas;
- necessidade de remediação urgente;
- evidências incompletas ou conflitantes.

### Interpretação

```text
Problema significativo
      +
Impacto relevante
      +
Risco de decisão incorreta
      ↓
HIGH
```

### Revisão humana

Um incidente `high` deve normalmente receber supervisão humana.

A regra obrigatória inicial estabelece revisão humana quando:

```text
severity = high
```

e:

```text
business impact = material
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="critical"></a>

## 🔴 CRITICAL

### Características típicas

Um incidente `critical` pode apresentar:

- interrupção severa de negócio;
- falha grave de integridade;
- processo crítico de produção afetado;
- exposição regulatória;
- exposição de privacidade;
- exposição de compliance;
- falha grave de governança;
- risco de consequência irreversível;
- dados materialmente incorretos utilizados em decisões executivas;
- necessidade de intervenção humana imediata.

### Regra absoluta

Todo incidente crítico exige revisão humana.

```text
severity = critical
        ↓
human_review_required = true
```

Essa regra independe da confidence.

Exemplo:

```text
severity = critical
confidence = 0.99
```

continua resultando em:

```text
human_review_required = true
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="avaliacao"></a>

## 📊 Princípios de avaliação de severidade

A severidade não deve ser calculada a partir de um único sinal quando múltiplas evidências relevantes estiverem disponíveis.

A análise deve considerar, quando aplicável:

- impacto técnico;
- impacto de negócio;
- quantidade de datasets afetados;
- quantidade de consumidores afetados;
- duração;
- recuperabilidade;
- risco de integridade;
- risco de governança;
- risco regulatório;
- risco de privacidade;
- qualidade das evidências;
- nível de incerteza;
- criticidade do processo afetado.

### Princípio

```text
Severidade
   =
Contexto
   +
Impacto
   +
Risco
   +
Evidência
```

A severidade não deve ser confundida com confidence.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="escalonamento"></a>

## ⬆️ Escalonamento de severidade

Quando evidências confiáveis indicarem níveis diferentes de severidade, o sistema deverá considerar o nível mais elevado sustentado pelo conjunto de evidências.

### Exemplo 1

Impacto técnico:

```text
medium
```

Impacto de negócio:

```text
high
```

Resultado possível:

```text
severity = high
```

---

### Exemplo 2

Impacto técnico:

```text
high
```

Exposição de governança:

```text
critical
```

Resultado esperado:

```text
severity = critical
```

---

### Exemplo 3

A evidência disponível não permite distinguir com segurança entre:

```text
high
```

e:

```text
critical
```

Nesse caso:

```text
human_review_required = true
```

mesmo antes de uma classificação definitiva.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="revisao-humana"></a>

## 👤 Revisão humana

O campo:

```text
human_review_required
```

indica se uma pessoa responsável precisa revisar:

- a avaliação;
- as conclusões;
- as hipóteses;
- as recomendações;
- ou uma possível ação.

### Tipo

```text
bool
```

Valores:

```text
true
false
```

A revisão humana funciona como um **controle de governança**.

Ela não deve depender exclusivamente de comportamento arbitrário de um modelo.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="regras-obrigatorias"></a>

## 🚨 Regras obrigatórias de revisão humana

`human_review_required` deve ser:

```text
true
```

quando **uma ou mais** das condições abaixo forem atendidas.

### 1. Severidade crítica

```text
severity = critical
```

---

### 2. Severidade alta com impacto material de negócio

```text
severity = high
```

e:

```text
material business impact = true
```

---

### 3. Confidence abaixo do limite

```text
confidence < 0.70
```

---

### 4. Evidência insuficiente

O sistema não consegue sustentar conclusões importantes.

---

### 5. Evidências conflitantes

Fontes confiáveis sustentam conclusões incompatíveis.

---

### 6. Possível exposição regulatória

Existe risco relacionado a requisitos regulatórios.

---

### 7. Possível violação de governança

Existe possível descumprimento de controle, política ou processo de governança.

---

### 8. Possível impacto de privacidade

O incidente pode envolver:

- dados pessoais;
- dados sensíveis;
- acesso inadequado;
- tratamento incorreto;
- exposição indevida.

---

### 9. Recomendação destrutiva

Exemplo:

```text
delete production data
```

---

### 10. Recomendação irreversível

A ação proposta não pode ser facilmente desfeita.

---

### 11. Causa raiz altamente incerta

Não existe evidência suficiente para sustentar uma hipótese dominante.

---

### 12. O sistema não consegue determinar uma recomendação segura

Quando múltiplas opções possuem risco significativo ou a informação disponível é insuficiente.

---

### 13. Processo crítico de negócio afetado

Exemplos:

- faturamento;
- pagamentos;
- operação essencial;
- reporting regulatório;
- decisão executiva crítica.

---

## Relação lógica

```text
Regra de risco ativada
        │
        ▼
human_review_required = true
```

Uma única regra obrigatória é suficiente.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="confidence-threshold"></a>

## 📏 Limite inicial de confidence

O limite inicial planejado é:

```text
confidence < 0.70
```

Quando a confidence geral ficar abaixo de `0.70`, revisão humana deverá ser obrigatória.

Exemplos:

```text
confidence = 0.69
→ revisão humana
```

```text
confidence = 0.40
→ revisão humana
```

```text
confidence = 0.70
→ essa regra específica não é ativada
```

Importante: outras regras ainda poderão exigir revisão humana.

### Natureza do limite

O valor `0.70` é **provisório**.

Ele deverá ser validado durante a fase de avaliação.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="confidence"></a>

## 📊 Interpretação de confidence

Interpretação conceitual inicial:

| Intervalo | Interpretação |
|---|---|
| `0.90 – 1.00` | Confiança muito alta |
| `0.80 – 0.89` | Confiança alta |
| `0.70 – 0.79` | Confiança moderada |
| `0.50 – 0.69` | Confiança baixa |
| `< 0.50` | Confiança muito baixa |

### Princípio importante

Confidence não substitui severidade.

```text
confidence
    ≠
severity
```

Um incidente crítico com confidence alta continua crítico.

Exemplo:

```text
severity = critical
confidence = 0.97
```

Resultado:

```text
human_review_required = true
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidencia-insuficiente"></a>

## ⚠️ Evidência insuficiente

A evidência deve ser considerada insuficiente quando o sistema não conseguir sustentar uma conclusão importante utilizando as fontes disponíveis.

### Exemplos

- nenhuma evidência foi fornecida;
- evidências não possuem relação clara com o incidente;
- informações de reconciliação necessárias estão ausentes;
- impacto de negócio não pode ser avaliado;
- hipóteses não possuem supporting evidence;
- informações relevantes estão incompletas.

### Consequências esperadas

Evidência insuficiente deverá normalmente resultar em:

- redução de confidence;
- conclusões qualificadas;
- hipóteses menos assertivas;
- recomendação de investigação adicional;
- indicação explícita da limitação;
- `human_review_required = true`.

### Fluxo

```text
Evidência insuficiente
        │
        ▼
Menor confidence
        │
        ▼
Conclusões qualificadas
        │
        ▼
Investigação adicional
        │
        ▼
Revisão humana
```

O sistema não deve fabricar evidências ausentes.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="evidencia-conflitante"></a>

## ⚔️ Evidência conflitante

Evidências são consideradas conflitantes quando fontes confiáveis sustentam conclusões incompatíveis.

### Exemplo

Fonte A:

```text
Dataset reconciliado corretamente
```

Fonte B:

```text
Dataset apresenta divergência material
```

Se ambas forem consideradas confiáveis, existe conflito.

### Regra

O sistema não deve escolher silenciosamente uma versão.

Quando o conflito afetar materialmente a análise:

- confidence deve diminuir;
- o conflito deve ser explicitado;
- a conclusão deve ser qualificada;
- revisão humana deve ser obrigatória.

```text
Evidência conflitante
        ↓
Incerteza aumenta
        ↓
Confidence diminui
        ↓
human_review_required = true
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="impacto-material"></a>

## 💼 Impacto material de negócio

Impacto material pode incluir situações como:

- reporting financeiro incorreto;
- reporting de receita incorreto;
- impacto significativo em clientes;
- interrupção operacional;
- reporting executivo incorreto;
- risco em reporting regulatório;
- decisões materiais baseadas em dados incorretos;
- corrupção significativa de análises downstream.

### Exemplos

```text
Receita mensal reportada incorretamente
```

```text
Dashboard executivo utilizando dados incompletos
```

```text
Processo operacional crítico afetado
```

### Regra

Os critérios exatos de materialidade poderão evoluir durante a fase de avaliação.

O sistema deverá evitar classificar materialidade com excesso de assertividade quando as evidências forem insuficientes.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="governanca"></a>

## 🛡️ Exposição de governança

Exposição de governança pode incluir situações como:

- violação de controles de Data Quality;
- acesso não autorizado;
- transformação não aprovada;
- descumprimento de política;
- falha de lineage;
- falha de rastreabilidade;
- preocupação com dados sensíveis;
- ausência de aprovações obrigatórias.

### Exemplos

```text
Dataset publicado sem aprovação obrigatória
```

```text
Lineage necessário não pode ser reconstruído
```

```text
Controle de Data Quality obrigatório foi ignorado
```

### Regra

Possível exposição de governança aumenta a necessidade de supervisão humana.

Quando materialmente relevante:

```text
human_review_required = true
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="acoes-destrutivas"></a>

## ⛔ Ações destrutivas ou irreversíveis

O agente não deve executar autonomamente ações destrutivas ou irreversíveis.

### Exemplos

- excluir dados de produção;
- sobrescrever datasets de produção;
- modificar permissões de acesso;
- desabilitar controles de governança;
- alterar regras de retenção;
- ignorar processos de aprovação;
- forçar rollback de produção;
- aplicar remediação irreversível.

### Regra

O agente pode **recomendar** uma ação desse tipo.

Entretanto:

```text
requires_human_approval = true
```

e:

```text
human_review_required = true
```

devem ser considerados obrigatórios.

### Fluxo

```text
Ação destrutiva
      │
      ▼
Recomendação
      │
      ▼
Aprovação humana obrigatória
      │
      ▼
Execução por processo autorizado
```

O agente não realiza a execução.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="principio-conservador"></a>

## 🧭 Princípio conservador de decisão

Quando houver incerteza relevante entre:

```text
human_review_required = false
```

e:

```text
human_review_required = true
```

o MVP deverá preferir:

```text
human_review_required = true
```

### Justificativa

Esse comportamento prioriza:

- segurança;
- governança;
- explicabilidade;
- responsabilidade;
- auditabilidade.

### Regra conceitual

```text
Dúvida material?
     │
   ┌─┴─┐
   │   │
  Sim Não
   │   │
   ▼   ▼
 true regra normal
```

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="governanca-deterministica"></a>

## ⚙️ Princípio de governança determinística

Sempre que possível, decisões sobre revisão humana devem utilizar regras explícitas e determinísticas.

### Objetivo

Permitir que a decisão seja:

- auditável;
- reproduzível;
- testável;
- explicável.

### Separação de responsabilidades

```text
IA
 │
 ├── pode analisar contexto
 ├── pode gerar hipótese
 └── pode fornecer suporte
          │
          ▼
Regras determinísticas
          │
          └── decidem controles críticos
```

Um modelo pode contribuir com a análise, mas controles críticos de governança não devem depender exclusivamente de sua decisão.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="casos"></a>

## 🧪 Casos de decisão

Os casos abaixo representam comportamentos esperados.

---

### Caso 1 — Severidade baixa

#### Condições

```text
severity = low
confidence = 0.95
evidence = complete
material_business_impact = false
governance_exposure = false
```

#### Resultado esperado

```text
human_review_required = false
```

#### Justificativa

- baixo impacto técnico;
- nenhuma exposição material;
- alta confiança;
- evidência adequada.

---

### Caso 2 — Confidence baixa

#### Condições

```text
severity = medium
confidence = 0.60
evidence = incomplete
```

#### Resultado esperado

```text
human_review_required = true
```

#### Motivos

- confidence abaixo do limite;
- evidência insuficiente.

---

### Caso 3 — Alto impacto de negócio

#### Condições

```text
severity = high
material_business_impact = true
confidence = 0.88
```

#### Resultado esperado

```text
human_review_required = true
```

#### Motivo

Severidade alta associada a impacto material de negócio.

---

### Caso 4 — Incidente crítico

#### Condições

```text
severity = critical
confidence = 0.97
evidence = strong
```

#### Resultado esperado

```text
human_review_required = true
```

#### Motivo

Incidentes críticos sempre exigem revisão humana responsável.

---

### Caso 5 — Recomendação destrutiva

#### Condições

```text
severity = medium
confidence = 0.92
recommendation = delete production data
```

#### Resultado esperado

```text
human_review_required = true
```

e:

```text
requires_human_approval = true
```

#### Motivo

Ação destrutiva ou irreversível exige aprovação humana.

---

### Caso 6 — Evidências conflitantes

#### Condições

```text
severity = medium
confidence = 0.82
conflicting_evidence = true
```

#### Resultado esperado

```text
human_review_required = true
```

#### Motivo

Conflitos entre evidências relevantes precisam ser resolvidos por investigação responsável.

---

### Caso 7 — Exposição de governança

#### Condições

```text
severity = medium
confidence = 0.90
governance_exposure = true
```

#### Resultado esperado

```text
human_review_required = true
```

#### Motivo

Possível violação de governança exige supervisão humana.

---

### Caso 8 — Confiança moderada sem outras regras

#### Condições

```text
severity = medium
confidence = 0.75
evidence = sufficient
conflicting_evidence = false
governance_exposure = false
material_business_impact = false
destructive_action = false
```

#### Resultado conceitual

Essa condição isoladamente não ativa a regra:

```text
confidence < 0.70
```

Portanto, revisão humana poderá ser:

```text
false
```

caso nenhuma outra regra obrigatória esteja ativa.

---

## 🔍 Ordem conceitual de avaliação

Uma implementação determinística poderá seguir uma lógica semelhante a:

```text
Receber estado da análise
        │
        ▼
Severity é critical?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
High + impacto material?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Confidence < 0.70?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Evidência insuficiente?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Evidência conflitante?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Exposição regulatória?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Exposição de governança?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Impacto de privacidade?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Ação destrutiva?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Ação irreversível?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Causa altamente incerta?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
Processo crítico afetado?
        │
       Sim ─────────────► REVIEW
        │
       Não
        ▼
NO MANDATORY REVIEW
```

A implementação final poderá organizar as regras de maneira diferente, desde que o comportamento permaneça equivalente e testável.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)

---

<a id="implementacao"></a>

## 🧩 Critérios previstos para implementação

A implementação determinística dessas regras está planejada para:

```text
DG-105 — Regras determinísticas de revisão humana
```

### Responsabilidades

A implementação deverá avaliar, no mínimo:

- severity;
- business impact;
- confidence;
- evidence sufficiency;
- evidence conflict;
- regulatory exposure;
- governance exposure;
- privacy impact;
- destructive action;
- irreversible action;
- root-cause uncertainty;
- affected critical process.

---

## 🧪 Testes esperados

Devem existir testes para cenários como:

1. critical sempre exige revisão;
2. high + impacto material exige revisão;
3. confidence `0.69` exige revisão;
4. confidence `0.70` não ativa essa regra isoladamente;
5. evidência insuficiente exige revisão;
6. evidência conflitante exige revisão;
7. exposição regulatória exige revisão;
8. exposição de governança exige revisão;
9. impacto de privacidade exige revisão;
10. ação destrutiva exige revisão;
11. ação irreversível exige revisão;
12. causa raiz altamente incerta exige revisão;
13. processo crítico exige revisão;
14. cenário seguro e de baixo risco pode dispensar revisão.

---

## 📏 Regra do threshold

A comparação inicial deve respeitar exatamente:

```text
confidence < 0.70
```

Portanto:

```text
0.69 → revisão
0.699 → revisão
0.70 → não ativa essa regra
0.71 → não ativa essa regra
```

Outras regras podem ainda exigir revisão independentemente desse valor.

---

## 🔗 Relação com outros contratos

```text
DOMAIN_ENUMS
      │
      └── Severity
              │
              ▼
SEVERITY_AND_HUMAN_REVIEW
              │
              ▼
       human_review_required
              │
              ▼
         AgentResponse
```

Além disso:

```text
Evidence
   │
   ├── suficiência
   ├── conflito
   └── confiabilidade
           │
           ▼
Regras de revisão humana
```

---

## 📌 Resumo das regras obrigatórias

| Condição | Revisão humana |
|---|---|
| `severity = critical` | ✅ Obrigatória |
| `high` + impacto material | ✅ Obrigatória |
| `confidence < 0.70` | ✅ Obrigatória |
| Evidência insuficiente | ✅ Obrigatória |
| Evidência conflitante | ✅ Obrigatória |
| Exposição regulatória | ✅ Obrigatória |
| Exposição de governança | ✅ Obrigatória |
| Impacto de privacidade | ✅ Obrigatória |
| Ação destrutiva | ✅ Obrigatória |
| Ação irreversível | ✅ Obrigatória |
| Causa raiz altamente incerta | ✅ Obrigatória |
| Processo crítico afetado | ✅ Obrigatória |

---

## 🧭 Princípio final

O projeto adota a seguinte orientação:

```text
Quanto maior o risco,
maior deve ser a supervisão.
```

e:

```text
Na dúvida material,
prefira revisão humana.
```

---

> 🛡️ As regras de severidade e revisão humana do **AI Data Governance Agent** foram concebidas para manter decisões críticas auditáveis, reproduzíveis e subordinadas à supervisão humana responsável.

[⬆️ Voltar ao índice](#sumario) · [📚 Central de documentação](../README.md)
