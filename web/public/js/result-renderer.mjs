function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

const translations = {
  data_quality: "Qualidade de dados",
  schema: "Esquema",
  integrity: "Integridade",
  reconciliation: "Reconciliação",
  freshness: "Atualidade dos dados",
  pipeline_failure: "Falha de pipeline",
  governance: "Governança",
  "governance-policy": "Política de governança",
  unknown: "Desconhecido",
  low: "Baixa",
  medium: "Média",
  high: "Alta",
  critical: "Crítica",
  confirmed: "Confirmado",
  potential: "Potencial",
  suspected: "Suspeita",
  probable: "Provável",
  rejected: "Rejeitada",
  data_quality_check: "Verificação de qualidade",
  pipeline_report: "Relatório de pipeline",
  validation_result: "Resultado de validação",
  reconciliation_result: "Resultado de reconciliação",
  log: "Log",
  business_rule: "Regra de negócio",
  governance_policy: "Política de governança",
  analyst_observation: "Observação do analista",
  metric: "Métrica",
  dataset_sample: "Amostra de dataset",
};

function translateValue(value) {
  const key = String(value ?? "").toLowerCase();

  return translations[key] ?? value ?? "—";
}

function classToken(value) {
  return String(value ?? "")
    .toLowerCase()
    .replace(/[^a-z0-9_-]/g, "");
}

function displayValue(value, fallback = "—") {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return fallback;
  }

  return escapeHtml(value);
}

function formatPercentage(value) {
  const numericValue = Number(value);

  if (!Number.isFinite(numericValue)) {
    return "—";
  }

  return `${(numericValue * 100).toFixed(0)}%`;
}

function renderStringList(
  values,
  emptyMessage = "Nenhum item informado."
) {
  if (!Array.isArray(values) || values.length === 0) {
    return `
      <p class="empty-state">
        ${escapeHtml(emptyMessage)}
      </p>
    `;
  }

  return `
    <ul class="compact-list">
      ${values
        .map(
          (value) => `
            <li>${escapeHtml(value)}</li>
          `
        )
        .join("")}
    </ul>
  `;
}

function renderEvidence(evidence) {
  if (!Array.isArray(evidence) || evidence.length === 0) {
    return `
      <p class="empty-state">
        Nenhuma evidência retornada.
      </p>
    `;
  }

  return evidence
    .map((item) => {
      const serializedValue =
        item.value === undefined ||
        item.value === null
          ? "—"
          : JSON.stringify(
              item.value,
              null,
              2
            );

      return `
        <article class="result-card">
          <div class="card-heading">
            <strong>
              ${displayValue(item.evidence_id)}
            </strong>

            <span class="chip">
              ${displayValue(translateValue(item.evidence_type))}
            </span>
          </div>

          <dl class="detail-list">
            <div>
              <dt>Fonte</dt>
              <dd>${displayValue(item.source)}</dd>
            </div>

            <div>
              <dt>Confiabilidade</dt>
              <dd>${displayValue(translateValue(item.reliability))}</dd>
            </div>
          </dl>

          ${
            item.description
              ? `
                <p>
                  ${escapeHtml(item.description)}
                </p>
              `
              : ""
          }

          <pre class="evidence-value">${escapeHtml(
            serializedValue
          )}</pre>
        </article>
      `;
    })
    .join("");
}

function renderBusinessImpact(impact = {}) {
  return `
    <article class="result-card">
      <div class="card-heading">
        <strong>Impacto identificado</strong>

        <span class="chip">
          ${displayValue(translateValue(impact.status))}
        </span>
      </div>

      <p>
        ${displayValue(
          impact.description,
          "Impacto não descrito."
        )}
      </p>

      <dl class="detail-list">
        <div>
          <dt>Materialidade</dt>
          <dd>${displayValue(translateValue(impact.materiality))}</dd>
        </div>
      </dl>

      <div class="nested-section">
        <h4>Processos afetados</h4>
        ${renderStringList(
          impact.affected_processes
        )}
      </div>

      <div class="nested-section">
        <h4>Consumidores afetados</h4>
        ${renderStringList(
          impact.affected_consumers
        )}
      </div>

      <div class="nested-section">
        <h4>Evidências de suporte</h4>
        ${renderStringList(
          impact.supporting_evidence
        )}
      </div>
    </article>
  `;
}

function renderHypotheses(hypotheses) {
  if (
    !Array.isArray(hypotheses) ||
    hypotheses.length === 0
  ) {
    return `
      <p class="empty-state">
        Nenhuma hipótese de causa raiz foi produzida.
      </p>
    `;
  }

  return hypotheses
    .map(
      (hypothesis) => `
        <article class="result-card">
          <div class="card-heading">
            <span class="chip">
              ${displayValue(translateValue(hypothesis.status))}
            </span>

            <strong>
              Confiança:
              ${formatPercentage(
                hypothesis.confidence
              )}
            </strong>
          </div>

          <p>
            ${displayValue(
              hypothesis.description
            )}
          </p>

          <div class="nested-section">
            <h4>Evidências de suporte</h4>
            ${renderStringList(
              hypothesis.supporting_evidence
            )}
          </div>
        </article>
      `
    )
    .join("");
}

function renderRecommendations(actions) {
  if (!Array.isArray(actions) || actions.length === 0) {
    return `
      <p class="empty-state">
        Nenhuma recomendação foi produzida.
      </p>
    `;
  }

  return actions
    .map(
      (action) => `
        <article class="result-card">
          <div class="card-heading">
            <span
              class="chip priority-${classToken(
                action.priority
              )}"
            >
              ${displayValue(translateValue(action.priority))}
            </span>

            <span class="approval-state">
              ${
                action.requires_human_approval
                  ? "Requer aprovação humana"
                  : "Não requer aprovação humana"
              }
            </span>
          </div>

          <p>
            <strong>
              ${displayValue(action.description)}
            </strong>
          </p>

          <p class="muted">
            ${displayValue(action.rationale)}
          </p>

          <div class="nested-section">
            <h4>Evidências de suporte</h4>
            ${renderStringList(
              action.supporting_evidence
            )}
          </div>
        </article>
      `
    )
    .join("");
}

function renderGovernanceControls(controls) {
  if (
    !Array.isArray(controls) ||
    controls.length === 0
  ) {
    return `
      <p class="empty-state">
        Nenhum controle de governança aplicável foi retornado.
      </p>
    `;
  }

  return controls
    .map(
      (control) => `
        <article class="result-card">
          <div class="card-heading">
            <strong>
              ${displayValue(control.control_id)}
            </strong>

            <span class="chip">
              Governança
            </span>
          </div>

          <h4>
            ${displayValue(control.title)}
          </h4>

          <p>
            ${displayValue(control.description)}
          </p>

          <dl class="detail-list">
            <div>
              <dt>Fonte</dt>
              <dd>${displayValue(translateValue(control.source))}</dd>
            </div>

            <div>
              <dt>Relevância</dt>
              <dd>${displayValue(control.relevance)}</dd>
            </div>
          </dl>

          <div class="nested-section">
            <h4>Evidências de suporte</h4>
            ${renderStringList(
              control.supporting_evidence
            )}
          </div>
        </article>
      `
    )
    .join("");
}

function renderHumanReview(result) {
  const required =
    result.human_review_required === true;

  return `
    <article
      class="review-card ${
        required
          ? "review-required"
          : "review-not-required"
      }"
    >
      <div>
        <p class="section-label">
          Supervisão humana
        </p>

        <h3>
          ${
            required
              ? "Revisão humana necessária"
              : "Revisão humana não obrigatória"
          }
        </h3>
      </div>

      ${
        required
          ? renderStringList(
              result.human_review_reasons,
              "Motivo não informado."
            )
          : `
            <p>
              O resultado não acionou os critérios
              determinísticos de revisão obrigatória.
            </p>
          `
      }
    </article>
  `;
}

function renderLoadingState() {
  return `
    <article
      class="state-card loading-state"
      role="status"
    >
      <span
        class="loading-spinner"
        aria-hidden="true"
      ></span>

      <div>
        <p class="section-label">
          Análise em andamento
        </p>

        <h3>Processando incidente</h3>

        <p>
          O agente está avaliando evidências,
          impacto, hipóteses e controles de
          governança.
        </p>
      </div>
    </article>
  `;
}

function renderErrorState(message) {
  const detail =
    message ||
    "A análise não pôde ser concluída.";

  return `
    <article
      class="state-card error-state"
      role="alert"
    >
      <div>
        <p class="section-label">
          Falha na análise
        </p>

        <h3>
          Não foi possível concluir a análise
        </h3>

        <p>
          ${escapeHtml(detail)}
        </p>

        <p class="state-hint">
          Revise os dados do incidente e tente
          novamente.
        </p>
      </div>
    </article>
  `;
}

function renderAnalysisResult(result) {
  if (!result || typeof result !== "object") {
    throw new TypeError(
      "O resultado da análise deve ser um objeto."
    );
  }

  return `
    <div class="result-overview">
      <div>
        <p class="result-label">Incidente</p>
        <strong>
          ${displayValue(result.incident_id)}
        </strong>
      </div>

      <div>
        <p class="result-label">Classificação</p>
        <span class="chip">
          ${displayValue(translateValue(result.classification))}
        </span>
      </div>

      <div>
        <p class="result-label">Severidade</p>
        <span
          class="severity severity-${classToken(
            result.severity
          )}"
        >
          ${displayValue(translateValue(result.severity))}
        </span>
      </div>

      <div>
        <p class="result-label">Confiança</p>
        <strong class="confidence-value">
          ${formatPercentage(result.confidence)}
        </strong>
      </div>
    </div>

    ${renderHumanReview(result)}

    <section class="result-block">
      <p class="section-label">
        Resumo executivo
      </p>
      <h3>Resumo executivo</h3>

      <p class="executive-summary">
        ${displayValue(result.executive_summary)}
      </p>
    </section>

    <section class="result-block">
      <p class="section-label">
        Evidências
      </p>
      <h3>Evidências</h3>

      <div class="result-grid">
        ${renderEvidence(result.evidence)}
      </div>
    </section>

    <section class="result-block">
      <p class="section-label">
        Impacto de negócio
      </p>
      <h3>Impacto de negócio</h3>

      ${renderBusinessImpact(
        result.business_impact
      )}
    </section>

    <section class="result-block">
      <p class="section-label">
        Causa raiz
      </p>
      <h3>Hipóteses</h3>

      <div class="result-grid">
        ${renderHypotheses(
          result.root_cause_hypotheses
        )}
      </div>
    </section>

    <section class="result-block">
      <p class="section-label">
        Ações recomendadas
      </p>
      <h3>Recomendações</h3>

      <div class="result-grid">
        ${renderRecommendations(
          result.recommended_actions
        )}
      </div>
    </section>

    <section class="result-block">
      <p class="section-label">
        Governança
      </p>
      <h3>Controles de governança</h3>

      <div class="result-grid">
        ${renderGovernanceControls(
          result.governance_controls
        )}
      </div>
    </section>
  `;
}

export {
  escapeHtml,
  formatPercentage,
  renderAnalysisResult,
  renderErrorState,
  renderLoadingState,
};
