const samples = {
  crashloop:
    "CrashLoopBackOff in pod payment-api due to invalid startup command and repeated restarts.",
  oom:
    "OOMKilled container in Kubernetes deployment after memory usage exceeded the configured limit.",
  network:
    "Error connecting to redis-service: connection refused from checkout-api container in cluster.",
};

const logInput = document.getElementById("log-input");
const analyzeBtn = document.getElementById("analyze-btn");
const clearBtn = document.getElementById("clear-btn");
const copyBtn = document.getElementById("copy-btn");
const resultCard = document.getElementById("result-card");
const jsonOutput = document.getElementById("json-output");
const statusText = document.getElementById("status-text");
const severityPill = document.getElementById("severity-pill");

function renderResult(data) {
  resultCard.classList.remove("empty");
  resultCard.innerHTML = `
    <div class="result-grid">
      <div class="result-item">
        <h3>Issue</h3>
        <p>${data.issue}</p>
      </div>
      <div class="result-item">
        <h3>Cause</h3>
        <p>${data.cause}</p>
      </div>
      <div class="result-item">
        <h3>Fix</h3>
        <p>${data.fix}</p>
      </div>
    </div>
  `;

  jsonOutput.textContent = JSON.stringify(data, null, 2);
  severityPill.textContent = data.severity;
  severityPill.className = `pill ${data.severity.toLowerCase()}`;
}

function renderEmptyState(message) {
  resultCard.className = "result-card empty";
  resultCard.innerHTML = `
    <div class="result-empty">
      <p class="result-empty-title">No result yet</p>
      <p class="result-empty-text">${message}</p>
    </div>
  `;
  severityPill.textContent = "Waiting";
  severityPill.className = "pill neutral";
  jsonOutput.textContent = `{
  "issue": "...",
  "cause": "...",
  "fix": "...",
  "severity": "..."
}`;
}

async function analyzeLog() {
  const log = logInput.value.trim();

  if (!log) {
    statusText.textContent = "Paste a log first so the evaluator has something to analyze.";
    logInput.focus();
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  statusText.textContent = "Running the ADK agent on Vertex AI Gemini...";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ log }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "The analysis request failed.");
    }

    const data = await response.json();
    renderResult(data);
    statusText.textContent = "Analysis complete.";
  } catch (error) {
    renderEmptyState("The request failed before a structured analysis could be shown.");
    statusText.textContent = "Unable to analyze the log right now.";
    jsonOutput.textContent = error.message;
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Log";
  }
}

document.querySelectorAll(".sample-chip").forEach((button) => {
  button.addEventListener("click", () => {
    logInput.value = samples[button.dataset.sample];
    statusText.textContent = "Sample loaded. Click Analyze Log to test the agent.";
  });
});

analyzeBtn.addEventListener("click", analyzeLog);

clearBtn.addEventListener("click", () => {
  logInput.value = "";
  statusText.textContent = "Ready for analysis.";
  renderEmptyState("Run an analysis to see the issue summary, cause, remediation, and severity.");
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(jsonOutput.textContent);
    copyBtn.textContent = "Copied";
    setTimeout(() => {
      copyBtn.textContent = "Copy";
    }, 1200);
  } catch {
    copyBtn.textContent = "Failed";
    setTimeout(() => {
      copyBtn.textContent = "Copy";
    }, 1200);
  }
});
