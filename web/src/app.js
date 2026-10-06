const path = require("node:path");

const express = require("express");

function createApp(options = {}) {
  const app = express();

  const apiBaseUrl =
    options.apiBaseUrl ||
    process.env.API_BASE_URL ||
    "http://127.0.0.1:8000";

  app.set("view engine", "ejs");
  app.set("views", path.join(__dirname, "..", "views"));

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

  return app;
}

module.exports = {
  createApp,
};
