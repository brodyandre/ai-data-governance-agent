const test = require("node:test");
const assert = require("node:assert/strict");

const request = require("supertest");

const { createApp } = require("../src/app");

test("GET / renders the web bootstrap", async () => {
  const app = createApp({
    apiBaseUrl: "http://api.example.test",
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
});

test("GET /health returns web service health", async () => {
  const app = createApp();

  const response = await request(app)
    .get("/health")
    .expect("Content-Type", /json/)
    .expect(200);

  assert.deepEqual(response.body, {
    status: "ok",
    service: "ai-data-governance-agent-web",
  });
});

test("default backend configuration targets local API", async () => {
  const app = createApp();

  const response = await request(app)
    .get("/")
    .expect(200);

  assert.match(
    response.text,
    /http:\/\/127\.0\.0\.1:8000/
  );
});
