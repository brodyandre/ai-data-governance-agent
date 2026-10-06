const path = require("node:path");

const express = require("express");

const ANALYZE_PATH = "/api/v1/incidents/analyze";

function createApp(options = {}) {
  const app = express();

  const apiBaseUrl =
    options.apiBaseUrl ||
    process.env.API_BASE_URL ||
    "http://127.0.0.1:8000";

  const fetchImpl =
    options.fetchImpl ||
    global.fetch;

  app.set("view engine", "ejs");
  app.set("views", path.join(__dirname, "..", "views"));

  app.use(express.json());

  app.use(
    express.static(
      path.join(__dirname, "..", "public")
    )
  );

  app.get("/", (request, response) => {
    response.render("index", {
      apiBaseUrl,
    });
  });

  app.get("/health", (request, response) => {
    response.status(200).json({
      status: "ok",
      service: "ai-data-governance-agent-web",
    });
  });

  app.post(
    "/api/analyze",
    async (request, response) => {
      try {
        const upstreamResponse =
          await fetchImpl(
            `${apiBaseUrl}${ANALYZE_PATH}`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(request.body),
            }
          );

        const responseBody =
          await upstreamResponse.text();

        const contentType =
          upstreamResponse.headers.get(
            "content-type"
          );

        if (contentType) {
          response.type(contentType);
        }

        response
          .status(upstreamResponse.status)
          .send(responseBody);
      } catch {
        response.status(502).json({
          code: "api_unavailable",
          message:
            "analysis API is unavailable",
          details: [],
        });
      }
    }
  );

  return app;
}

module.exports = {
  ANALYZE_PATH,
  createApp,
};
