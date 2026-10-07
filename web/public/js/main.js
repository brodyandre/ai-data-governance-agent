"use strict";

import {
  renderAnalysisResult,
} from "./result-renderer.mjs";

const demoIncident = {
  incident_id: "EVAL-DE-101",
  title:
    "Divergência entre as camadas raw e silver no pipeline de vendas",
  description:
    "Pedidos e itens de pedidos apresentam perdas de qualidade de dados entre as etapas de processamento raw, silver e gold.",
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
    "As análises de vendas dependem de registros que atendam às validações de qualidade e integridade dos relacionamentos.",
  initial_severity: "high",
  tags: [
    "de-101",
    "data-quality",
    "reconciliation",
  ],
  evidence: [
    {
      evidence_id:
        "EV-DE101-QUALITY",
      evidence_type:
        "data_quality_check",
      source:
        "bronze-to-silver-analysis",
      description:
        "Foram identificadas quantidades inválidas e relacionamentos ausentes nos itens de pedidos.",
      value: {
        invalid_rows: 30,
        missing_relationships: 33,
      },
      reliability: "high",
    },
    {
      evidence_id:
        "EV-DE101-RECON",
      evidence_type:
        "reconciliation_result",
      source:
        "pipeline-reconciliation",
      description:
        "A quantidade de itens de pedidos diverge entre as camadas raw e silver.",
      value: {
        raw_count: 1000,
        silver_count: 970,
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
        "O problema de qualidade afeta registros utilizados na construção da tabela fato de vendas.",
      value: {
        business_impact: {
          status: "confirmed",
          description:
            "Sales fact-table completeness is affected.",
          affected_processes: [
            "sales analytics",
          ],
          affected_consumers: [
            "analytics users",
          ],
          materiality: "high",
        },
      },
      reliability: "high",
    },
  ],
};

const form =
  document.querySelector(
    "#incident-form"
  );

const demoButton =
  document.querySelector(
    "#load-demo"
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

function clearResult() {
  resultContent.innerHTML = "";
  resultSection.hidden = true;
}

function showResult(result) {
  resultContent.innerHTML =
    renderAnalysisResult(result);

  resultSection.hidden = false;

  resultSection.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function loadDemoIncident() {
  byId("incident-id").value =
    demoIncident.incident_id;

  byId("incident-title").value =
    demoIncident.title;

  byId(
    "incident-description"
  ).value =
    demoIncident.description;

  byId("source-system").value =
    demoIncident.source_system;

  byId("detected-at").value =
    formatDatetimeLocal(
      demoIncident.detected_at
    );

  byId(
    "affected-datasets"
  ).value =
    demoIncident
      .affected_datasets
      .join(", ");

  byId(
    "business-context"
  ).value =
    demoIncident.business_context;

  byId(
    "initial-severity"
  ).value =
    demoIncident.initial_severity;

  byId("incident-tags").value =
    demoIncident.tags.join(", ");

  evidenceInput.value =
    JSON.stringify(
      demoIncident.evidence,
      null,
      2
    );

  evidenceInput.setCustomValidity("");

  clearResult();

  setMessage(
    "info",
    "Cenário DE-101 carregado. Revise os dados e envie para análise."
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
        responseBody.message ||
          "A análise não pôde ser concluída."
      );
    }

    showResult(responseBody);

    setMessage(
      "success",
      `Incidente ${payload.incident_id} analisado com sucesso.`
    );
  } catch (error) {
    setMessage(
      "error",
      error.message ||
        "Não foi possível comunicar com a API de análise."
    );
  } finally {
    submitButton.disabled = false;
    submitButton.textContent =
      "Enviar para análise";
  }
}

demoButton.addEventListener(
  "click",
  loadDemoIncident
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
