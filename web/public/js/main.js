"use strict";

import {
  renderAnalysisResult,
  renderErrorState,
  renderLoadingState,
} from "./result-renderer.mjs";

const demoIncidents = {
  de101: {
    incident_id: "EVAL-DE-101",
    title:
      "Divergência de elegibilidade entre Silver e Gold no pipeline de vendas",
    description:
      "A camada Silver preserva 1000 itens de pedido, enquanto 937 registros elegíveis compõem a fct_sales após aplicação das regras de qualidade e elegibilidade.",
    source_system:
      "aws-lakehouse-engineering-lab",
    detected_at:
      "2026-10-06T12:00:00.000Z",
    affected_datasets: [
      "orders",
      "order_items",
      "fct_sales",
    ],
    business_context:
      "As análises de vendas consomem a fct_sales e precisam distinguir rejeições esperadas por regra de negócio de perdas inesperadas de dados.",
    initial_severity: "medium",
    tags: [
      "de-101",
      "data-quality",
      "reconciliation",
      "silver-gold",
    ],
    evidence: [
      {
        evidence_id:
          "EV-DE101-LAYERS",
        evidence_type:
          "reconciliation_result",
        source:
          "layer-reconciliation",
        description:
          "As contagens de order_items entre Raw e Silver permanecem em 1000 registros, sem perda nessa transição.",
        value: {
          raw_count: 1000,
          silver_count: 1000,
        },
        reliability: "high",
      },
      {
        evidence_id:
          "EV-DE101-QUALITY",
        evidence_type:
          "data_quality_check",
        source:
          "silver-quality-analysis",
        description:
          "A Silver preserva os registros inválidos: 30 itens apresentam quantidade inválida e 12 pedidos possuem status inválido, impactando 33 itens.",
        value: {
          invalid_rows: 30,
          invalid_orders: 12,
          impacted_order_items: 33,
        },
        reliability: "high",
      },
      {
        evidence_id:
          "EV-DE101-RECON",
        evidence_type:
          "reconciliation_result",
        source:
          "silver-to-gold-reconciliation",
        description:
          "A fct_sales contém 937 registros elegíveis após aplicação das regras de publicação da camada Gold.",
        value: {
          source_count: 1000,
          target_count: 937,
          rejected_invalid_quantity: 30,
          rejected_invalid_order_status: 33,
        },
        reliability: "high",
      },
      {
        evidence_id:
          "EV-DE101-IMPACT",
        evidence_type:
          "analyst_observation",
        source:
          "incident-analysis",
        description:
          "As exclusões esperadas na Gold podem ser interpretadas como perda de dados quando as regras de elegibilidade não estão explícitas para os consumidores analíticos.",
        value: {
          business_impact: {
            status: "potential",
            description:
              "Consumidores analíticos podem interpretar exclusões esperadas da Gold como perda inesperada de dados.",
            affected_processes: [
              "análises de vendas",
            ],
            affected_consumers: [
              "usuários de analytics",
            ],
            materiality: "medium",
          },
        },
        reliability: "high",
      },
    ],
  },
  de102: {
    incident_id: "EVAL-DE-102",
    title:
      "Ambiguidade semântica na métrica de receita",
    description:
      "Gold e Analytics reconciliam corretamente, mas não existe definição formal de quais status de pedido são elegíveis para métricas denominadas receita.",
    source_system:
      "aws-lakehouse-engineering-lab",
    detected_at:
      "2026-10-06T12:00:00.000Z",
    affected_datasets: [
      "gold.fct_sales",
      "analytics.revenue_by_month",
      "analytics.revenue_by_category",
      "analytics.top_customers",
      "analytics.campaign_performance",
    ],
    business_context:
      "Métricas financeiras precisam de um contrato semântico explícito para diferenciar validade técnica de reconhecimento de receita.",
    initial_severity: "high",
    tags: [
      "de-102",
      "governance",
      "semantic-contract",
      "revenue",
    ],
    evidence: [
      {
        evidence_id:
          "EV-DE102-METRIC",
        evidence_type:
          "metric",
        source:
          "de-102-investigation",
        description:
          "Gold e Analytics reconciliam em R$ 1.416.127,23. Um cenário investigativo com paid e shipped resulta em R$ 548.323,22.",
        value: {
          analytics_revenue: 1416127.23,
          gold_revenue: 1416127.23,
          paid_shipped_revenue: 548323.22,
          investigative_difference: 867804.01,
          investigative_difference_percentage:
            61.28,
        },
        reliability: "high",
      },
      {
        evidence_id:
          "EV-DE102-STATUS",
        evidence_type:
          "metric",
        source:
          "de-102-status-analysis",
        description:
          "Todos os status tecnicamente válidos possuem valores positivos de net_amount na fct_sales.",
        value: {
          cancelled: {
            sales_rows: 222,
            distinct_orders: 94,
            net_revenue: 328252.48,
          },
          created: {
            sales_rows: 175,
            distinct_orders: 69,
            net_revenue: 279216.30,
          },
          shipped: {
            sales_rows: 183,
            distinct_orders: 77,
            net_revenue: 275168.43,
          },
          paid: {
            sales_rows: 178,
            distinct_orders: 76,
            net_revenue: 273154.79,
          },
          refunded: {
            sales_rows: 179,
            distinct_orders: 68,
            net_revenue: 260335.23,
          },
        },
        reliability: "high",
      },
      {
        evidence_id:
          "EV-DE102-RULE",
        evidence_type:
          "business_rule",
        source:
          "de-102-investigation",
        description:
          "Não existe contrato de negócio explícito definindo quais status são elegíveis para receita.",
        value: {
          semantic_contract_defined: false,
          eligible_statuses_defined: false,
          technical_defect_confirmed: false,
          gold_analytics_reconciled: true,
          business_impact: {
            status: "potential",
            description:
              "Métricas financeiras podem ser interpretadas de maneiras diferentes enquanto a semântica de receita não estiver formalizada.",
            affected_processes: [
              "análises financeiras",
            ],
            affected_consumers: [
              "stakeholders de negócio",
              "usuários de analytics",
            ],
            materiality: "high",
          },
        },
        reliability: "high",
      },
    ],
  },
};

const form =
  document.querySelector(
    "#incident-form"
  );

const demo101Button =
  document.querySelector(
    "#load-demo"
  );

const demo102Button =
  document.querySelector(
    "#load-demo-de102"
  );

const submitButton =
  document.querySelector(
    "#submit-button"
  );

const message =
  document.querySelector(
    "#form-message"
  );

const evidenceInput =
  document.querySelector(
    "#incident-evidence"
  );

const resultSection =
  document.querySelector(
    "#analysis-result"
  );

const resultContent =
  document.querySelector(
    "#analysis-result-content"
  );

function byId(id) {
  return document.getElementById(id);
}

function parseList(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function formatDatetimeLocal(value) {
  const date = new Date(value);

  const offset =
    date.getTimezoneOffset() * 60000;

  return new Date(
    date.getTime() - offset
  )
    .toISOString()
    .slice(0, 16);
}

function validateEvidence(value) {
  let evidence;

  try {
    evidence = JSON.parse(value);
  } catch {
    throw new Error(
      "Evidências devem conter JSON válido."
    );
  }

  if (!Array.isArray(evidence)) {
    throw new Error(
      "Evidências devem ser um array JSON."
    );
  }

  for (const item of evidence) {
    if (
      !item ||
      typeof item !== "object" ||
      !item.evidence_id ||
      !item.evidence_type ||
      !item.source
    ) {
      throw new Error(
        "Cada evidência precisa de evidence_id, evidence_type e source."
      );
    }
  }

  return evidence;
}

function buildPayload() {
  const evidence =
    validateEvidence(
      evidenceInput.value
    );

  const payload = {
    incident_id:
      byId("incident-id").value.trim(),
    title:
      byId("incident-title").value.trim(),
    description:
      byId(
        "incident-description"
      ).value.trim(),
    source_system:
      byId("source-system").value.trim(),
    detected_at: new Date(
      byId("detected-at").value
    ).toISOString(),
    evidence,
    affected_datasets:
      parseList(
        byId(
          "affected-datasets"
        ).value
      ),
    tags:
      parseList(
        byId("incident-tags").value
      ),
  };

  const businessContext =
    byId(
      "business-context"
    ).value.trim();

  const initialSeverity =
    byId(
      "initial-severity"
    ).value;

  if (businessContext) {
    payload.business_context =
      businessContext;
  }

  if (initialSeverity) {
    payload.initial_severity =
      initialSeverity;
  }

  return payload;
}

function setMessage(type, text) {
  message.className =
    `form-message ${type}`;
  message.textContent = text;
}

function resolveAnalysisError(responseBody) {
  const messages = {
    provider_not_configured:
      "O provedor de modelo não está configurado.",
    api_unavailable:
      "A API de análise está indisponível.",
  };

  return (
    messages[responseBody.code] ||
    responseBody.message ||
    "A análise não pôde ser concluída."
  );
}

function clearResult() {
  resultContent.innerHTML = "";
  resultSection.hidden = true;
  resultSection.removeAttribute("aria-busy");
}

function showLoadingState() {
  resultContent.innerHTML =
    renderLoadingState();

  resultSection.hidden = false;
  resultSection.setAttribute(
    "aria-busy",
    "true"
  );

  resultSection.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function showErrorState(errorMessage) {
  resultContent.innerHTML =
    renderErrorState(errorMessage);

  resultSection.hidden = false;
  resultSection.setAttribute(
    "aria-busy",
    "false"
  );

  resultSection.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function showResult(result) {
  resultContent.innerHTML =
    renderAnalysisResult(result);

  resultSection.hidden = false;
  resultSection.setAttribute(
    "aria-busy",
    "false"
  );

  resultSection.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function loadDemoIncident(incident, label) {
  byId("incident-id").value =
    incident.incident_id;

  byId("incident-title").value =
    incident.title;

  byId(
    "incident-description"
  ).value =
    incident.description;

  byId("source-system").value =
    incident.source_system;

  byId("detected-at").value =
    formatDatetimeLocal(
      incident.detected_at
    );

  byId(
    "affected-datasets"
  ).value =
    incident
      .affected_datasets
      .join(", ");

  byId(
    "business-context"
  ).value =
    incident.business_context;

  byId(
    "initial-severity"
  ).value =
    incident.initial_severity;

  byId("incident-tags").value =
    incident.tags.join(", ");

  evidenceInput.value =
    JSON.stringify(
      incident.evidence,
      null,
      2
    );

  evidenceInput.setCustomValidity("");

  clearResult();

  setMessage(
    "info",
    `Cenário ${label} carregado. Revise os dados e envie para análise.`
  );
}

async function submitIncident(event) {
  event.preventDefault();

  setMessage("", "");
  clearResult();

  evidenceInput.setCustomValidity("");

  if (!form.reportValidity()) {
    return;
  }

  let payload;

  try {
    payload = buildPayload();
  } catch (error) {
    evidenceInput.setCustomValidity(
      error.message
    );

    evidenceInput.reportValidity();

    setMessage(
      "error",
      error.message
    );

    return;
  }

  evidenceInput.setCustomValidity("");

  submitButton.disabled = true;
  submitButton.textContent =
    "Analisando...";

  setMessage(
    "info",
    "Incidente enviado. Aguardando resposta do agente..."
  );

  showLoadingState();

  try {
    const response = await fetch(
      "/api/analyze",
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json",
        },
        body: JSON.stringify(
          payload
        ),
      }
    );

    const responseText =
      await response.text();

    let responseBody = {};

    if (responseText) {
      try {
        responseBody =
          JSON.parse(responseText);
      } catch {
        responseBody = {};
      }
    }

    if (!response.ok) {
      throw new Error(
        resolveAnalysisError(responseBody)
      );
    }

    showResult(responseBody);

    setMessage(
      "success",
      `Incidente ${payload.incident_id} analisado com sucesso.`
    );
  } catch (error) {
    const errorMessage =
      error.message ||
      "Não foi possível comunicar com a API de análise.";

    setMessage(
      "error",
      "Falha na análise. Consulte os detalhes abaixo."
    );

    showErrorState(errorMessage);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent =
      "Enviar para análise";
  }
}

demo101Button.addEventListener(
  "click",
  () => {
    loadDemoIncident(
      demoIncidents.de101,
      "DE-101"
    );
  }
);

demo102Button.addEventListener(
  "click",
  () => {
    loadDemoIncident(
      demoIncidents.de102,
      "DE-102"
    );
  }
);

evidenceInput.addEventListener(
  "input",
  () => {
    evidenceInput.setCustomValidity("");
  }
);

form.addEventListener(
  "reset",
  () => {
    evidenceInput.setCustomValidity("");

    setTimeout(() => {
      setMessage("", "");
      clearResult();
    }, 0);
  }
);

form.addEventListener(
  "submit",
  submitIncident
);
