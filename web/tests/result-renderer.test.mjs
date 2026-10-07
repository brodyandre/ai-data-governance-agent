import assert from "node:assert/strict";
import test from "node:test";

import {
  escapeHtml,
  formatPercentage,
  renderAnalysisResult,
  renderErrorState,
  renderLoadingState,
} from "../public/js/result-renderer.mjs";

function makeAgentResponse() {
  return {
    incident_id: "INC-803",
    classification: "data_quality",
    severity: "high",
    executive_summary:
      "Invalid records affected downstream analytics.",
    evidence: [
      {
        evidence_id: "EV-001",
        evidence_type:
          "data_quality_check",
        source: "quality-report",
        description:
          "Thirty invalid rows were detected.",
        value: {
          invalid_rows: 30,
        },
        reliability: "high",
      },
    ],
    business_impact: {
      status: "confirmed",
      description:
        "Sales analytics completeness is affected.",
      affected_processes: [
        "sales analytics",
      ],
      affected_consumers: [
        "analytics users",
      ],
      materiality: "high",
      supporting_evidence: [
        "EV-001",
      ],
    },
    root_cause_hypotheses: [
      {
        description:
          "Invalid source records caused the divergence.",
        supporting_evidence: [
          "EV-001",
        ],
        confidence: 0.9,
        status: "probable",
      },
    ],
    recommended_actions: [
      {
        description:
          "Review rejected records.",
        priority: "high",
        rationale:
          "The evidence identifies invalid rows.",
        requires_human_approval: false,
        supporting_evidence: [
          "EV-001",
        ],
      },
    ],
    governance_controls: [
      {
        control_id: "GOV-001",
        title:
          "Evidence traceability",
        description:
          "Claims must reference evidence.",
        source:
          "governance-policy",
        relevance:
          "Ensures auditable analysis.",
        supporting_evidence: [
          "EV-001",
        ],
      },
    ],
    confidence: 0.92,
    human_review_required: true,
    human_review_reasons: [
      "High-severity incident requires review.",
    ],
  };
}

test(
  "renderer includes all DG-803 result sections",
  () => {
    const html =
      renderAnalysisResult(
        makeAgentResponse()
      );

    assert.match(
      html,
      /Classificação/
    );

    assert.match(
      html,
      /Severidade/
    );

    assert.match(
      html,
      /Resumo executivo/
    );

    assert.match(
      html,
      /Evidências/
    );

    assert.match(
      html,
      /Impacto de negócio/
    );

    assert.match(
      html,
      /Hipóteses/
    );

    assert.match(
      html,
      /Recomendações/
    );

    assert.match(
      html,
      /Controles de governança/
    );

    assert.match(
      html,
      /Confiança/
    );

    assert.match(
      html,
      /Revisão humana necessária/
    );

    assert.match(
      html,
      /Política de governança/
    );
  }
);

test(
  "renderer formats confidence as percentage",
  () => {
    const html =
      renderAnalysisResult(
        makeAgentResponse()
      );

    assert.match(
      html,
      /92%/
    );

    assert.match(
      html,
      /90%/
    );

    assert.equal(
      formatPercentage(0.755),
      "76%"
    );
  }
);

test(
  "renderer escapes server-provided HTML",
  () => {
    const response =
      makeAgentResponse();

    response.executive_summary =
      '<script>alert("xss")</script>';

    const html =
      renderAnalysisResult(
        response
      );

    assert.doesNotMatch(
      html,
      /<script>/
    );

    assert.match(
      html,
      /&lt;script&gt;/
    );

    assert.equal(
      escapeHtml("<b>unsafe</b>"),
      "&lt;b&gt;unsafe&lt;/b&gt;"
    );
  }
);

test(
  "renderer handles empty result collections",
  () => {
    const response =
      makeAgentResponse();

    response.evidence = [];
    response.root_cause_hypotheses =
      [];
    response.recommended_actions =
      [];
    response.governance_controls =
      [];

    const html =
      renderAnalysisResult(
        response
      );

    assert.match(
      html,
      /Nenhuma evidência retornada/
    );

    assert.match(
      html,
      /Nenhuma hipótese de causa raiz/
    );

    assert.match(
      html,
      /Nenhuma recomendação/
    );

    assert.match(
      html,
      /Nenhum controle de governança/
    );
  }
);


test(
  "renderer exposes a dedicated loading state",
  () => {
    const html = renderLoadingState();

    assert.match(
      html,
      /Análise em andamento/
    );

    assert.match(
      html,
      /Processando incidente/
    );

    assert.match(
      html,
      /role="status"/
    );
  }
);

test(
  "renderer exposes a safe error state",
  () => {
    const html = renderErrorState(
      '<script>alert("xss")</script>'
    );

    assert.match(
      html,
      /Não foi possível concluir a análise/
    );

    assert.match(
      html,
      /role="alert"/
    );

    assert.doesNotMatch(
      html,
      /<script>/
    );

    assert.match(
      html,
      /&lt;script&gt;/
    );
  }
);
