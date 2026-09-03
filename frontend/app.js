/**
 * AI Codebase Mentor — Frontend App
 * Handles: view switching, indexing flow (demo), and the Q&A chat interface.
 */

const API = "http://localhost:5000";

// ─── State ──────────────────────────────────────────────────────────────────
let currentRepo = null;
let isWaiting = false;

// ─── DOM Refs ───────────────────────────────────────────────────────────────
const viewIndex   = document.getElementById("view-index");
const viewChat    = document.getElementById("view-chat");

const repoUrlInput   = document.getElementById("repo-url-input");
const indexBtn       = document.getElementById("index-btn");
const indexError     = document.getElementById("index-error");
const inputCard      = document.getElementById("input-card");
const progressCard   = document.getElementById("progress-card");
const progressStatus = document.getElementById("progress-status");
const progressName   = document.getElementById("progress-repo-name");
const indexStats     = document.getElementById("index-stats");
const statFiles      = document.getElementById("stat-files");
const statChunks     = document.getElementById("stat-chunks");
const startChatBtn   = document.getElementById("start-chat-btn");

const repoSelector    = document.getElementById("repo-selector");
const chatRepoLabel   = document.getElementById("chat-repo-label");
const infoFiles       = document.getElementById("info-files");
const infoChunks      = document.getElementById("info-chunks");
const messagesArea    = document.getElementById("messages-area");
const questionInput   = document.getElementById("question-input");
const sendBtn         = document.getElementById("send-btn");
const backToIndexBtn  = document.getElementById("back-to-index-btn");
const intentChips     = document.querySelectorAll(".chip");


// ═══════════════════════════════════════════════════════════════════════════
// INDEX VIEW — Repo indexing demo
// ═══════════════════════════════════════════════════════════════════════════

indexBtn.addEventListener("click", startIndexing);

repoUrlInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") startIndexing();
});

async function startIndexing() {
  const url = repoUrlInput.value.trim();
  if (!url) {
    showIndexError("Please enter a GitHub repository URL.");
    return;
  }

  indexError.classList.add("hidden");
  indexBtn.disabled = true;

  // Show progress card, hide input card
  inputCard.classList.add("hidden");
  progressCard.classList.remove("hidden");

  // Run the animated steps
  await runIndexingAnimation(url);
}

async function runIndexingAnimation(url) {
  const steps = [
    { id: "step-clone", label: "Cloning repository",       delay: 900  },
    { id: "step-read",  label: "Reading source files",      delay: 1100 },
    { id: "step-embed", label: "Generating embeddings",     delay: 1400 },
    { id: "step-ready", label: "Finalizing index",          delay: 800  },
  ];

  // Start first step spinning
  setStepSpinning("step-clone");

  // Fire the actual API call in parallel with the animation
  const apiPromise = callIndexAPI(url);

  // Play through each step animation
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    setStepSpinning(step.id);
    await sleep(step.delay);
    setStepDone(step.id);

    // Start next step spinning while current finishes
    if (i + 1 < steps.length) {
      setStepSpinning(steps[i + 1].id);
    }
  }

  // Wait for the API to finish
  const result = await apiPromise;

  if (result.error) {
    progressCard.classList.add("hidden");
    inputCard.classList.remove("hidden");
    indexBtn.disabled = false;
    showIndexError(result.error);
    return;
  }

  // Success — show stats
  progressName.textContent = result.repo_name;
  progressStatus.textContent = "Ready";
  progressStatus.classList.add("done");

  statFiles.textContent  = result.file_count  || "—";
  statChunks.textContent = result.chunk_count || "—";
  indexStats.classList.remove("hidden");
  startChatBtn.classList.remove("hidden");

  // Store repo for the chat
  currentRepo = result.repo_name;
}

async function callIndexAPI(url) {
  try {
    const res = await fetch(`${API}/index`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    return await res.json();
  } catch (err) {
    return { error: "Could not connect to server. Make sure api.py is running." };
  }
}

startChatBtn.addEventListener("click", () => switchToChat(currentRepo));

function showIndexError(msg) {
  indexError.textContent = msg;
  indexError.classList.remove("hidden");
}


// ═══════════════════════════════════════════════════════════════════════════
// CHAT VIEW — Q&A Interface
// ═══════════════════════════════════════════════════════════════════════════

async function switchToChat(repoName) {
  // Switch views
  viewIndex.classList.remove("active");
  viewChat.classList.add("active");

  // Load repos into dropdown
  await loadRepos(repoName);

  // Update header label
  chatRepoLabel.textContent = repoName || "your repository";
}

async function loadRepos(preferredRepo) {
  try {
    const res = await fetch(`${API}/repos`);
    const repos = await res.json();

    repoSelector.innerHTML = "";

    if (!repos.length) {
      repoSelector.innerHTML = '<option value="">No repos found</option>';
      return;
    }

    repos.forEach((repo) => {
      const opt = document.createElement("option");
      opt.value = repo;
      opt.textContent = repo;
      if (repo === preferredRepo) opt.selected = true;
      repoSelector.appendChild(opt);
    });

    currentRepo = repoSelector.value;
    updateRepoInfo(currentRepo);
  } catch {
    repoSelector.innerHTML = '<option value="">Server not reachable</option>';
  }
}

repoSelector.addEventListener("change", () => {
  currentRepo = repoSelector.value;
  chatRepoLabel.textContent = currentRepo;
  updateRepoInfo(currentRepo);
});

async function updateRepoInfo(repoName) {
  // Quick index call for stats (won't reindex, just returns cached info)
  try {
    const knownUrls = {
      "SyncSphere-Website":  "https://github.com/Rajat072005/SyncSphere-Website",
      "LeetMetrics-WebApp":  "https://github.com/Rajat072005/LeetMetrics-WebApp",
    };
    const url = knownUrls[repoName];
    if (!url) return;

    const res = await fetch(`${API}/index`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    if (!data.error) {
      infoFiles.textContent  = data.file_count  || "—";
      infoChunks.textContent = data.chunk_count || "—";
    }
  } catch { /* ignore */ }
}

// ── Intent chips ──
intentChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const prompt = chip.dataset.prompt;
    if (prompt) {
      questionInput.value = prompt;
      questionInput.focus();
      autoResizeTextarea();
    }
  });
});

// ── Back button ──
backToIndexBtn.addEventListener("click", () => {
  viewChat.classList.remove("active");
  viewIndex.classList.add("active");

  // Reset index view state
  inputCard.classList.remove("hidden");
  progressCard.classList.add("hidden");
  indexStats.classList.add("hidden");
  startChatBtn.classList.add("hidden");
  indexBtn.disabled = false;
  progressStatus.classList.remove("done");
  progressStatus.textContent = "Processing";
  repoUrlInput.value = "";
  resetSteps();
});

// ── Send message ──
sendBtn.addEventListener("click", sendMessage);

questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

questionInput.addEventListener("input", autoResizeTextarea);

async function sendMessage() {
  const question = questionInput.value.trim();
  if (!question || isWaiting || !currentRepo) return;

  clearWelcomeMessage();

  // Render user message
  appendMessage("user", question);
  questionInput.value = "";
  autoResizeTextarea();

  // Show thinking indicator
  isWaiting = true;
  sendBtn.disabled = true;
  const thinkingEl = appendThinking();

  try {
    const res = await fetch(`${API}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo: currentRepo, question })
    });
    const data = await res.json();

    thinkingEl.remove();

    if (data.error) {
      appendMessage("ai", `⚠️ Error: ${data.error}`, null, null);
    } else {
      appendMessage("ai", data.answer, data.intent, data.confidence);
    }
  } catch (err) {
    thinkingEl.remove();
    appendMessage("ai", "⚠️ Could not reach the server. Make sure api.py is running.", null, null);
  } finally {
    isWaiting = false;
    sendBtn.disabled = false;
    questionInput.focus();
  }
}

function appendMessage(role, text, intent, confidence) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;

  // Sender label
  const sender = document.createElement("div");
  sender.className = "message-sender";
  sender.textContent = role === "user" ? "You" : "Mentor";

  // Bubble
  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  if (role === "ai" && typeof marked !== "undefined") {
    bubble.innerHTML = marked.parse(text || "");
  } else {
    bubble.textContent = text || "";
  }

  wrapper.appendChild(sender);
  wrapper.appendChild(bubble);

  // Meta row for AI messages
  if (role === "ai" && intent) {
    const meta = document.createElement("div");
    meta.className = "message-meta";

    const badge = document.createElement("span");
    badge.className = "intent-badge";
    badge.textContent = intent;
    meta.appendChild(badge);

    if (confidence !== null && confidence !== undefined) {
      const conf = document.createElement("span");
      conf.className = "confidence-badge";
      conf.textContent = `confidence: ${confidence}/10`;
      meta.appendChild(conf);
    }

    wrapper.appendChild(meta);
  }

  messagesArea.appendChild(wrapper);
  scrollToBottom();
  return wrapper;
}

function appendThinking() {
  const wrapper = document.createElement("div");
  wrapper.className = "message ai";

  const indicator = document.createElement("div");
  indicator.className = "thinking-indicator";
  indicator.innerHTML = `
    <div class="thinking-dots">
      <span></span><span></span><span></span>
    </div>
    <span class="thinking-label">Thinking...</span>
  `;

  wrapper.appendChild(indicator);
  messagesArea.appendChild(wrapper);
  scrollToBottom();
  return wrapper;
}

function clearWelcomeMessage() {
  const welcome = messagesArea.querySelector(".welcome-message");
  if (welcome) welcome.remove();
}

function scrollToBottom() {
  messagesArea.scrollTop = messagesArea.scrollHeight;
}

function autoResizeTextarea() {
  questionInput.style.height = "auto";
  questionInput.style.height = Math.min(questionInput.scrollHeight, 160) + "px";
}


// ═══════════════════════════════════════════════════════════════════════════
// Progress Step Helpers
// ═══════════════════════════════════════════════════════════════════════════

function setStepSpinning(stepId) {
  const el = document.getElementById(stepId);
  if (!el) return;
  el.classList.remove("pending", "done");
  el.querySelector(".step-icon").textContent = "◌";
  el.querySelector(".step-icon").classList.add("spinning");
}

function setStepDone(stepId) {
  const el = document.getElementById(stepId);
  if (!el) return;
  el.classList.add("done");
  const icon = el.querySelector(".step-icon");
  icon.classList.remove("spinning");
  icon.textContent = "✓";
}

function resetSteps() {
  ["step-clone", "step-read", "step-embed", "step-ready"].forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove("done");
    el.classList.add("pending");
    const icon = el.querySelector(".step-icon");
    icon.classList.remove("spinning");
    icon.textContent = "◌";
  });
}


// ═══════════════════════════════════════════════════════════════════════════
// Utilities
// ═══════════════════════════════════════════════════════════════════════════

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
