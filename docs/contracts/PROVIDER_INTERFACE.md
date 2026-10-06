# 🔌 Contrato de Interface de Provider

Este documento define a abstração utilizada pelo **AI Data Governance Agent** para interação com modelos de linguagem sem acoplar a lógica central a um fornecedor específico.

## Objetivo

A lógica central deve depender do contrato `ModelProvider`, e não de SDKs ou implementações específicas de fornecedores.

## Arquitetura

```text
Lógica do agente
      │
      ▼
ModelProvider
      │
      ├── FakeProvider
      └── Provider real opcional
```

## ModelProvider

O contrato define duas responsabilidades principais:

- expor um identificador estável por meio de `provider_name`;
- gerar respostas Pydantic estruturadas por meio de `generate_structured()`.

A assinatura conceitual é:

```python
def generate_structured[T: BaseModel](
    *,
    system_prompt: str,
    user_prompt: str,
    response_model: type[T],
) -> T: ...
```

O retorno deve ser uma instância validada do modelo Pydantic recebido em `response_model`.

## ProviderError

`ProviderError` representa a raiz das falhas relacionadas a providers. Implementações futuras poderão especializar erros de configuração, autenticação, indisponibilidade, timeout ou resposta inválida quando houver necessidade concreta.

## Independência de fornecedor

A DG-301 não adiciona dependências específicas de OpenAI, Oracle, Anthropic, Google ou qualquer outro fornecedor.

Isso preserva:

- baixo acoplamento;
- testes offline;
- CI independente de credenciais;
- substituição futura do provider;
- comportamento testável.

## Sincronicidade

A interface inicial é síncrona. Streaming e execução assíncrona permanecem fora do escopo até existir necessidade comprovada.

## Testabilidade

`ModelProvider` utiliza `Protocol`, portanto implementações compatíveis não precisam herdar diretamente da interface.

Isso permite implementar um `FakeProvider` determinístico na DG-302.

## Limites da DG-301

Inclui:

- `ModelProvider`;
- `ProviderError`;
- contrato documental;
- testes da abstração.

Não inclui:

- provider real;
- credenciais;
- requisições HTTP;
- LangGraph;
- retries;
- streaming;
- tool calling;
- fallback entre fornecedores.

## Critérios de aceite

A DG-301 deve garantir:

- lógica central independente de fornecedor;
- suporte a saída Pydantic estruturada;
- contrato documentado;
- comportamento testável offline;
- CI independente de credenciais externas.
