# DG-903 — Runbook da demonstração ao vivo

## Objetivo

Definir uma sequência reproduzível para demonstrar o AI Data Governance Agent
durante o Challenge, reduzindo improvisação e risco operacional.

Este runbook separa explicitamente:

- a interface web;
- a API FastAPI;
- o workflow LangGraph;
- as ferramentas determinísticas;
- o provider determinístico utilizado na demonstração;
- a avaliação automatizada.

## Transparência sobre o provider

A demonstração controlada utiliza respostas determinísticas baseadas nos
cenários versionados DE-101 e DE-102.

Esse modo existe para manter a apresentação reproduzível e não depender de
rede, credenciais ou disponibilidade de um LLM externo.

Ele não deve ser apresentado como execução de um modelo real em produção.

A parte efetivamente executada pelo sistema continua incluindo:

- validação do incidente;
- coleta e organização de evidências;
- análise de Data Quality;
- análise de impacto de negócio;
- recuperação de controles de governança;
- guardrails;
- regras de revisão humana;
- construção do `AgentResponse`.

---

## 1. Duração sugerida

Meta para a demonstração principal:

| Etapa | Tempo |
| --- | ---: |
| Contexto do problema | 45 s |
| DE-101 | 90 s |
| DE-102 | 120 s |
| Avaliação mensurável | 45 s |
| Encerramento | 30 s |
| Total aproximado | 5 a 6 min |

Se houver menos tempo, priorizar o DE-102 e os resultados mensuráveis.

---

## 2. Preparação antes da apresentação

Executar a partir da raiz do repositório.

Confirmar branch e estado:

```bash
git status
git log -1 --oneline
```

Ativar o ambiente virtual:

```bash
source .venv/bin/activate
```

Validar rapidamente a avaliação:

```bash
python -m ai_data_governance_agent.evaluation
```

O resultado esperado é:

```text
Scenarios: 7
Scenario results: 7/7 passed
```

Validar a interface:

```bash
cd web
npm test
cd ..
```

O resultado esperado no estado da DG-903 é:

```text
18 tests
18 pass
0 fail
```

---

## 3. Backend determinístico da demonstração

A aplicação FastAPI padrão não configura automaticamente um provider.

Para uma demonstração controlada dos cenários DE-101 e DE-102, criar um
adaptador temporário fora do repositório.

O arquivo abaixo não faz parte do produto e não deve ser commitado.

Criar:

```bash
cat > /tmp/ai_data_governance_demo_api.py <<'PY'
import json

from pydantic import BaseModel

from ai_data_governance_agent.api import create_app
from ai_data_governance_agent.evaluation import load_evaluation_dataset
from ai_data_governance_agent.providers import ProviderError
from ai_data_governance_agent.workflow import (
    HypothesisGenerationResult,
    RecommendationGenerationResult,
)


SCENARIOS = {
    scenario.incident.incident_id: scenario
    for scenario in load_evaluation_dataset()
    if scenario.incident.incident_id
    in {
        "EVAL-DE-101",
        "EVAL-DE-102",
    }
}


class DemoScenarioProvider:
    @property
    def provider_name(self) -> str:
        return "deterministic-demo"

    def generate_structured[T: BaseModel](
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        del system_prompt

        payload = json.loads(user_prompt)
        incident_id = payload["incident"]["incident_id"]

        scenario = SCENARIOS.get(incident_id)

        if scenario is None:
            raise ProviderError(
                f"demo scenario not configured: {incident_id}"
            )

        if response_model is HypothesisGenerationResult:
            configured = scenario.hypothesis_response
        elif response_model is RecommendationGenerationResult:
            configured = scenario.recommendation_response
        else:
            raise ProviderError(
                f"unsupported demo response model: {response_model.__name__}"
            )

        if configured is None:
            raise ProviderError(
                f"demo response not configured: {response_model.__name__}"
            )

        return response_model.model_validate(
            configured.model_dump()
        )


app = create_app(
    provider=DemoScenarioProvider()
)
PY
```

Importante: esse adaptador usa o provider determinístico apenas para as etapas
que dependem de geração estruturada. O restante do workflow continua sendo
executado pela aplicação.

---

## 4. Iniciar os serviços

Usar dois terminais.

### Terminal A — FastAPI

Na raiz do projeto e com `.venv` ativa:

```bash
PYTHONPATH=/tmp uvicorn \
  ai_data_governance_demo_api:app \
  --host 127.0.0.1 \
  --port 8000
```

Validar em outro terminal:

```bash
curl -s http://127.0.0.1:8000/health
```

Esperado:

```json
{"status":"ok","service":"ai-data-governance-agent","version":"0.1.0"}
```

### Terminal B — Interface web

```bash
cd web
npm start
```

Validar:

```bash
curl -s http://127.0.0.1:3000/health
```

Esperado:

```json
{"status":"ok","service":"ai-data-governance-agent-web"}
```

Abrir no navegador:

```text
http://localhost:3000
```

Não deixar outras abas, terminais ou notificações desnecessárias visíveis.

---

## 5. Abertura da demonstração

Mensagem a transmitir:

> Incidentes de dados normalmente chegam com evidências fragmentadas. O
> objetivo deste agente é organizar essas evidências, separar fato de
> hipótese, avaliar impacto e governança e indicar quando uma pessoa precisa
> assumir a decisão.

Na tela, apontar brevemente:

- formulário do incidente;
- botões DE-101 e DE-102;
- evidências estruturadas;
- botão de análise.

Não explicar ainda todos os campos.

---

## 6. Demonstrar o DE-101

Clicar:

`Carregar cenário DE-101`

Destacar:

- 1000 registros em Silver;
- 937 registros em Gold;
- 30 itens com quantidade inválida;
- 33 itens relacionados a 12 pedidos com status inválido;
- nenhuma perda entre Raw e Silver.

Mensagem principal:

> Uma diferença de contagem não significa automaticamente perda de dados.

Clicar:

`Analisar incidente`

Na resposta, destacar:

- classificação de reconciliação;
- severidade média;
- causa suportada pelas evidências;
- impacto potencial;
- recomendação consultiva;
- revisão humana obrigatória para mudança da regra.

Não dizer que o pipeline está defeituoso.

---

## 7. Demonstrar o DE-102

Clicar:

`Carregar cenário DE-102`

Destacar inicialmente:

- Gold: R$ 1.416.127,23;
- Analytics: R$ 1.416.127,23;
- as duas camadas reconciliam matematicamente.

Depois mostrar o cenário investigativo:

- `paid + shipped`: R$ 548.323,22;
- diferença investigativa: R$ 867.804,01;
- aproximadamente 61,28%.

Mensagem obrigatória:

> Esses 61,28% não são uma perda financeira comprovada. O número é um cenário
> investigativo. O problema confirmado é a ausência de um contrato semântico
> que defina quais status devem representar receita.

Clicar:

`Analisar incidente`

Na resposta, destacar:

- classificação de governança;
- severidade alta;
- ausência de defeito técnico comprovado;
- impacto potencial;
- necessidade de definição do negócio;
- revisão humana antes de alteração de SQL.

Esse é o ponto principal da demonstração de guardrails.

---

## 8. Mostrar resultados mensuráveis

Depois da interface, abrir um terminal já preparado e executar:

```bash
python -m ai_data_governance_agent.evaluation
```

Mostrar apenas os pontos principais:

```text
Scenarios: 7
Scenario results: 7/7 passed

Schema valid rate: 100.0%
Severity accuracy: 100.0%
Evidence traceability rate: 100.0%
Unsupported rejection rate: 100.0%
Human review accuracy: 100.0%
Tool execution success rate: 100.0%
Test pass rate: 100.0%
```

Explicar:

> Esses resultados pertencem ao dataset determinístico versionado. Não são
> uma alegação de 100% de acerto para qualquer incidente do mundo real.

Não utilizar `response_latency` como promessa de desempenho.

---

## 9. Encerramento

Mensagem final:

> O valor da solução não é automatizar cegamente uma correção. É organizar a
> investigação, tornar as conclusões rastreáveis, explicitar incerteza e
> encaminhar decisões críticas para supervisão humana.

Encerrar mostrando a área de revisão humana ou o resultado do DE-102.

---

## 10. Plano de contingência

### API não inicia

Executar:

```bash
python -m ai_data_governance_agent.evaluation
```

Usar o runner como prova de execução reproduzível do workflow e mostrar a
interface apenas para carregamento dos cenários.

Não fingir que a análise web foi executada.

### Interface não inicia

Mostrar:

- `docs/scenarios/DE-101.md`;
- `docs/scenarios/DE-102.md`;
- saída do evaluation runner.

### Erro durante submissão

Não depurar ao vivo por vários minutos.

Explicar que a interface propaga falhas da API de forma segura e seguir para o
runner determinístico.

### Falha de internet

A demonstração principal não depende de serviço externo quando o modo
determinístico está preparado localmente.

---

## 11. Frases que não devem ser usadas

Evitar afirmar:

- "o agente provou que houve perda financeira";
- "61,28% da receita está errada";
- "a IA corrige automaticamente o pipeline";
- "o modelo sempre encontra a causa raiz";
- "os testes provam 100% de acerto em produção";
- "o FakeProvider é um modelo de IA real";
- "somente paid e shipped são receita";
- "há perda de dados entre Raw e Silver no DE-101".

---

## 12. Checklist de 15 minutos antes

Confirmar:

- `.venv` ativa;
- portas 8000 e 3000 livres;
- API respondendo `/health`;
- web respondendo `/health`;
- DE-101 carrega;
- DE-101 analisa;
- DE-102 carrega;
- DE-102 analisa;
- evaluation runner retorna 7/7;
- navegador em zoom legível;
- notificações do sistema desabilitadas;
- terminal limpo;
- repositório sem alterações acidentais.

Comandos úteis:

```bash
git status --short
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:3000/health
python -m ai_data_governance_agent.evaluation
```

---

## 13. Encerrar os serviços

Nos terminais da API e da interface:

```text
Ctrl+C
```

Remover o adaptador temporário:

```bash
rm -f /tmp/ai_data_governance_demo_api.py
```

Confirmar que ele nunca entrou no repositório:

```bash
git status --short
```

---

## Regra de ouro

Se houver conflito entre uma apresentação mais impressionante e uma
apresentação tecnicamente fiel ao que o projeto implementa, escolher a
fidelidade técnica.

A demonstração deve ser reproduzível, auditável e transparente sobre os
limites do sistema.
