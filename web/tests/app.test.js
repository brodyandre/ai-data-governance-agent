const test = require("node:test");
const assert = require("node:assert/strict");

const request = require("supertest");

const {
  ANALYZE_PATH,
  createApp,
} = require("../src/app");

function makeIncidentPayload() {
  return {
    incident_id: "INC-WEB-001",
    title: "Invalid records detected",
    description:
      "A data-quality validation identified invalid records.",
    source_system: "orders-lakehouse",
    detected_at:
      "2026-10-06T22:30:00.000Z",
    evidence: [
      {
        evidence_id: "EV-001",
        evidence_type:
          "data_quality_check",
        source: "quality-report",
        value: {
          invalid_rows: 30,
        },
      },
    ],
  };
}

test(
  "GET / renders the web bootstrap",
  async () => {
    const app = createApp({
      apiBaseUrl:
        "http://api.example.test",
    });

    const response = await request(app)
      .get("/")
      .expect(200);

    assert.match(
      response.text,
      /AI Data Governance Agent/
    );

    assert.match(
      response.text,
      /http:\/\/api\.example\.test/
    );
  }
);

test(
  "GET /health returns web service health",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/health")
      .expect("Content-Type", /json/)
      .expect(200);

    assert.deepEqual(response.body, {
      status: "ok",
      service:
        "ai-data-governance-agent-web",
    });
  }
);

test(
  "default backend configuration targets local API",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/")
      .expect(200);

    assert.match(
      response.text,
      /http:\/\/127\.0\.0\.1:8000/
    );
  }
);

test(
  "POST /api/analyze forwards incident to FastAPI",
  async () => {
    const payload = makeIncidentPayload();

    let receivedUrl;
    let receivedOptions;

    const fetchImpl = async (
      url,
      options
    ) => {
      receivedUrl = url;
      receivedOptions = options;

      return new Response(
        JSON.stringify({
          incident_id:
            payload.incident_id,
          classification:
            "data_quality",
          severity: "medium",
        }),
        {
          status: 200,
          headers: {
            "Content-Type":
              "application/json",
          },
        }
      );
    };

    const app = createApp({
      apiBaseUrl:
        "http://api.example.test",
      fetchImpl,
    });

    const response = await request(app)
      .post("/api/analyze")
      .send(payload)
      .expect(200);

    assert.equal(
      receivedUrl,
      `http://api.example.test${ANALYZE_PATH}`
    );

    assert.equal(
      receivedOptions.method,
      "POST"
    );

    assert.deepEqual(
      JSON.parse(receivedOptions.body),
      payload
    );

    assert.equal(
      response.body.incident_id,
      "INC-WEB-001"
    );
  }
);

test(
  "POST /api/analyze preserves FastAPI errors",
  async () => {
    const fetchImpl = async () =>
      new Response(
        JSON.stringify({
          code:
            "provider_not_configured",
          message:
            "model provider is not configured",
          details: [],
        }),
        {
          status: 503,
          headers: {
            "Content-Type":
              "application/json",
          },
        }
      );

    const app = createApp({
      fetchImpl,
    });

    const response = await request(app)
      .post("/api/analyze")
      .send(makeIncidentPayload())
      .expect(503);

    assert.equal(
      response.body.code,
      "provider_not_configured"
    );
  }
);

test(
  "POST /api/analyze reports unavailable API safely",
  async () => {
    const fetchImpl = async () => {
      throw new Error(
        "connection refused"
      );
    };

    const app = createApp({
      fetchImpl,
    });

    const response = await request(app)
      .post("/api/analyze")
      .send(makeIncidentPayload())
      .expect(502);

    assert.deepEqual(response.body, {
      code: "api_unavailable",
      message:
        "analysis API is unavailable",
      details: [],
    });
  }
);

test(
  "GET / renders incident input controls",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/")
      .expect(200);

    assert.match(
      response.text,
      /id="incident-form"/
    );

    assert.match(
      response.text,
      /id="incident-id"/
    );

    assert.match(
      response.text,
      /id="incident-evidence"/
    );

    assert.match(
      response.text,
      /id="submit-button"/
    );
  }
);

test(
  "GET / exposes DE-101 demo loader",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/")
      .expect(200);

    assert.match(
      response.text,
      /id="load-demo"/
    );

    assert.match(
      response.text,
      /Carregar cenário DE-101/
    );
  }
);

test(
  "GET / includes analysis result container",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/")
      .expect(200);

    assert.match(
      response.text,
      /id="analysis-result"/
    );

    assert.match(
      response.text,
      /id="analysis-result-content"/
    );

    assert.match(
      response.text,
      /type="module"/
    );
  }
);


test(
  "GET /js/main.js preserves canonical DE-101 facts",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/js/main.js")
      .expect(200);

    assert.match(
      response.text,
      /initial_severity:\s*"medium"/
    );

    assert.match(
      response.text,
      /raw_count:\s*1000/
    );

    assert.match(
      response.text,
      /silver_count:\s*1000/
    );

    assert.match(
      response.text,
      /source_count:\s*1000/
    );

    assert.match(
      response.text,
      /target_count:\s*937/
    );

    assert.match(
      response.text,
      /invalid_orders:\s*12/
    );

    assert.match(
      response.text,
      /impacted_order_items:\s*33/
    );

    assert.doesNotMatch(
      response.text,
      /missing_relationships/
    );

    assert.doesNotMatch(
      response.text,
      /silver_count:\s*970/
    );

    assert.doesNotMatch(
      response.text,
      /\bdemoIncident\b/
    );
  }
);

test(
  "GET / exposes DE-102 demo loader",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/")
      .expect(200);

    assert.match(
      response.text,
      /id="load-demo-de102"/
    );

    assert.match(
      response.text,
      /Carregar cenário DE-102/
    );
  }
);

test(
  "GET /js/main.js preserves canonical DE-102 facts",
  async () => {
    const app = createApp();

    const response = await request(app)
      .get("/js/main.js")
      .expect(200);

    assert.match(
      response.text,
      /incident_id:\s*"EVAL-DE-102"/
    );

    assert.match(
      response.text,
      /analytics_revenue:\s*1416127\.23/
    );

    assert.match(
      response.text,
      /gold_revenue:\s*1416127\.23/
    );

    assert.match(
      response.text,
      /paid_shipped_revenue:\s*548323\.22/
    );

    assert.match(
      response.text,
      /investigative_difference:\s*867804\.01/
    );

    assert.match(
      response.text,
      /61\.28/
    );

    assert.match(
      response.text,
      /semantic_contract_defined:\s*false/
    );

    assert.match(
      response.text,
      /technical_defect_confirmed:\s*false/
    );

    assert.match(
      response.text,
      /gold_analytics_reconciled:\s*true/
    );
  }
);
