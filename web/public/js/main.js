"use strict";

const apiConfiguration =
  document.querySelector("[data-api-base-url]");

if (apiConfiguration) {
  const apiBaseUrl =
    apiConfiguration.dataset.apiBaseUrl;

  console.info(
    `Configured API base URL: ${apiBaseUrl}`
  );
}
