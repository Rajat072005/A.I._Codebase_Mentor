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
    const res = await fetch(`${API}/index/live`, {
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

// async function updateRepoInfo(repoName) {
//   // Quick index call for stats (won't reindex, just returns cached info)
//   try {
//     const knownUrls = {
//       "SyncSphere-Website":  "https://github.com/Rajat072005/SyncSphere-Website",
//       "LeetMetrics-WebApp":  "https://github.com/Rajat072005/LeetMetrics-WebApp",
//     };
//     const url = knownUrls[repoName];
//     if (!url) return;

//     const res = await fetch(`${API}/index`, {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ url })
//     });
//     const data = await res.json();
//     if (!data.error) {
//       infoFiles.textContent  = data.file_count  || "—";
//       infoChunks.textContent = data.chunk_count || "—";
//     }
//   } catch { /* ignore */ }
// }

async function updateRepoInfo(repoName) {
  try {
    const res = await fetch(`${API}/repos/${encodeURIComponent(repoName)}/stats`);
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

// Visual identity per intent — turns the plain badge into a scannable,
// color-coded signal instead of generic chat-bubble metadata.
const INTENT_META = {
  overview:       { icon: "◈", label: "overview",       cls: "intent-overview" },
  architecture:   { icon: "▤", label: "architecture",   cls: "intent-architecture" },
  implementation: { icon: "⌁", label: "implementation", cls: "intent-implementation" },
  locate:         { icon: "⊙", label: "locate",         cls: "intent-locate" },
  debug:          { icon: "⚠", label: "debug",          cls: "intent-debug" },
  casual:         { icon: "◍", label: "casual",         cls: "intent-casual" },
};

function getIntentMeta(intent) {
  const key = String(intent || "").toLowerCase().trim();
  return INTENT_META[key] || { icon: "◍", label: key || "general", cls: "intent-default" };
}

function appendMessage(role, text, intent, confidence) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;

  // Sender label — AI messages get a small breathing orb instead of a flat dot.
  const sender = document.createElement("div");
  sender.className = "message-sender";
  if (role === "ai") {
    const orb = document.createElement("span");
    orb.className = "mentor-orb";
    sender.appendChild(orb);
    sender.appendChild(document.createTextNode("Mentor"));
  } else {
    sender.textContent = "You";
  }

  // Bubble
  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  wrapper.appendChild(sender);
  wrapper.appendChild(bubble);

  // Meta row for AI messages
  if (role === "ai" && intent) {
    const meta = document.createElement("div");
    meta.className = "message-meta";

    const im = getIntentMeta(intent);
    const badge = document.createElement("span");
    badge.className = `intent-badge ${im.cls}`;
    badge.innerHTML = `<span class="intent-icon">${im.icon}</span>${im.label}`;
    meta.appendChild(badge);

    if (confidence !== null && confidence !== undefined) {
      const conf = document.createElement("span");
      conf.className = "confidence-meter";
      conf.title = `confidence: ${confidence}/10`;
      conf.innerHTML = `
        <span class="confidence-label">confidence</span>
        <span class="confidence-track"><span class="confidence-fill" style="--fill:${Math.max(0, Math.min(10, confidence)) * 10}%"></span></span>
        <span class="confidence-value">${confidence}/10</span>
      `;
      meta.appendChild(conf);
    }

    wrapper.appendChild(meta);
  }

  messagesArea.appendChild(wrapper);
  scrollToBottom();

  // Render content — AI text streams in; plain text (user messages) is instant.
  if (role === "ai" && typeof marked !== "undefined") {
    streamMarkdownInto(bubble, text || "");
  } else {
    bubble.textContent = text || "";
  }

  return wrapper;
}

// Reveals markdown a few words at a time, re-parsing the growing string on
// each tick so formatting (bold, lists, code fences) is always valid by the
// time it's shown. Falls back to an instant render for very short strings.
function streamMarkdownInto(bubble, fullText) {
  const words = fullText.split(/(\s+)/); // keep whitespace tokens so spacing survives
  if (words.length <= 6) {
    bubble.innerHTML = marked.parse(fullText);
    enhanceCodeBlocks(bubble);
    return;
  }

  bubble.classList.add("streaming");
  const caret = document.createElement("span");
  caret.className = "typing-caret";

  let i = 0;
  const chunk = Math.max(2, Math.round(words.length / 60)); // ~60 ticks regardless of length

  function tick() {
    i = Math.min(words.length, i + chunk);
    const partial = words.slice(0, i).join("");
    bubble.innerHTML = marked.parse(partial);
    bubble.appendChild(caret);
    scrollToBottom();

    if (i < words.length) {
      setTimeout(tick, 16);
    } else {
      bubble.classList.remove("streaming");
      caret.remove();
      bubble.innerHTML = marked.parse(fullText); // final, guaranteed-correct render
      enhanceCodeBlocks(bubble);
      scrollToBottom();
    }
  }

  tick();
}

// Adds a "Copy" button to every code block in an AI answer.
function enhanceCodeBlocks(bubble) {
  bubble.querySelectorAll("pre").forEach((pre) => {
    if (pre.querySelector(".code-copy-btn")) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "code-copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", async () => {
      const code = pre.querySelector("code");
      const text = code ? code.textContent : pre.textContent;
      try {
        await navigator.clipboard.writeText(text);
        btn.textContent = "Copied";
        btn.classList.add("copied");
      } catch {
        btn.textContent = "Select & copy";
      }
      setTimeout(() => {
        btn.textContent = "Copy";
        btn.classList.remove("copied");
      }, 1500);
    });
    pre.appendChild(btn);
  });
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


// ═══════════════════════════════════════════════════════════════════════════
// Presentation-only enhancements
// Everything below is purely visual (cursor glow, magnetic buttons, small
// reveal/pulse classes). None of it reads or writes app state, calls the
// API, or changes when/what gets sent — safe to remove without touching
// how the front end and backend talk to each other.
// ═══════════════════════════════════════════════════════════════════════════

// Only show the custom focus ring for keyboard users, and only show the
// pointer glow once we know there's an actual pointer moving.
(function setupInputModeDetection() {
  window.addEventListener("keydown", (e) => {
    if (e.key === "Tab") document.body.classList.add("using-keyboard");
  });
  window.addEventListener("mousedown", () => {
    document.body.classList.remove("using-keyboard");
  });
})();

// Cursor-reactive ambient glow — trails the pointer with a little lag.
(function setupPointerGlow() {
  const glow = document.getElementById("pointer-glow");
  if (!glow || window.matchMedia("(hover: none)").matches) return;

  let targetX = window.innerWidth / 2;
  let targetY = window.innerHeight / 3;
  let curX = targetX;
  let curY = targetY;
  let raf = null;

  window.addEventListener("mousemove", (e) => {
    targetX = e.clientX;
    targetY = e.clientY;
    glow.classList.add("active");
    if (!raf) raf = requestAnimationFrame(tick);
  });

  function tick() {
    curX += (targetX - curX) * 0.08;
    curY += (targetY - curY) * 0.08;
    glow.style.setProperty("--px", `${curX}px`);
    glow.style.setProperty("--py", `${curY}px`);
    if (Math.abs(targetX - curX) > 0.5 || Math.abs(targetY - curY) > 0.5) {
      raf = requestAnimationFrame(tick);
    } else {
      raf = null;
    }
  }
})();

// Magnetic highlight on primary buttons — a soft light that leans toward
// the cursor while hovering.
(function setupMagneticButtons() {
  document.querySelectorAll(".btn-primary").forEach((btn) => {
    btn.addEventListener("mousemove", (e) => {
      const rect = btn.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      btn.style.setProperty("--mx", `${x}%`);
      btn.style.setProperty("--my", `${y}%`);
    });
  });
})();

// Small "arrived" pop on the index stats once they're revealed, a pulse
// ring on send, a lit-up file grid while indexing runs, a browser-tab hint
// while waiting on a response, and a little success burst on first index.
const _origRunIndexingAnimation = runIndexingAnimation;
runIndexingAnimation = async function (url) {
  const stopGrid = animateFileGrid();
  await _origRunIndexingAnimation(url);
  stopGrid();
  indexStats.classList.add("reveal");
  fireSuccessBurst(startChatBtn);
};

const ORIGINAL_TITLE = document.title;
const _origSendMessage = sendMessage;
sendMessage = async function () {
  if (questionInput.value.trim()) {
    sendBtn.classList.remove("pulse");
    void sendBtn.offsetWidth; // restart animation
    sendBtn.classList.add("pulse");
    document.title = "Thinking… · " + ORIGINAL_TITLE;
  }
  await _origSendMessage();
  document.title = ORIGINAL_TITLE;
};
sendBtn.removeEventListener("click", _origSendMessage);
sendBtn.addEventListener("click", sendMessage);
// Note: the Enter-key handler above already calls sendMessage() through a
// closure, so it picks up this wrapper automatically — no rebind needed.

// ── File-scan visualizer ────────────────────────────────────────────────
function animateFileGrid() {
  const grid = document.getElementById("file-grid");
  if (!grid) return () => {};

  const COLS = 18, ROWS = 4;
  grid.innerHTML = "";
  const cells = [];
  for (let i = 0; i < COLS * ROWS; i++) {
    const cell = document.createElement("div");
    cell.className = "cell";
    grid.appendChild(cell);
    cells.push(cell);
  }

  let active = true;
  (function loop() {
    if (!active) return;
    // Light a small random cluster, unlight an older one — a gentle scan
    // rather than a strict left-to-right sweep, so it doesn't look canned.
    const n = 2 + Math.floor(Math.random() * 3);
    for (let i = 0; i < n; i++) {
      const c = cells[Math.floor(Math.random() * cells.length)];
      c.classList.remove("lit", "lit-violet");
      c.classList.add(Math.random() > 0.5 ? "lit" : "lit-violet");
      setTimeout(() => c.classList.remove("lit", "lit-violet"), 500);
    }
    setTimeout(loop, 90);
  })();

  return function stop() {
    active = false;
    setTimeout(() => {
      cells.forEach((c) => c.classList.remove("lit", "lit-violet"));
    }, 550);
  };
}

// ── Success burst — a handful of particles on first successful index ───
function fireSuccessBurst(anchorEl) {
  if (!anchorEl) return;
  const rect = anchorEl.getBoundingClientRect();
  const originX = rect.left + rect.width / 2;
  const originY = rect.top;
  const colors = ["#45E0C4", "#9B7CF6", "#F3F0FB"];

  for (let i = 0; i < 14; i++) {
    const p = document.createElement("span");
    p.className = "burst-particle";
    const angle = (Math.PI * 2 * i) / 14 + Math.random() * 0.4;
    const dist = 40 + Math.random() * 50;
    p.style.left = `${originX}px`;
    p.style.top = `${originY}px`;
    p.style.background = colors[i % colors.length];
    p.style.setProperty("--bx", `${Math.cos(angle) * dist}px`);
    p.style.setProperty("--by", `${Math.sin(angle) * dist - 20}px`);
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 800);
  }
}

// ── Command palette (⌘K / Ctrl+K) ───────────────────────────────────────
// Reuses existing functions only (switchToChat/repoSelector, intent chips'
// prompts, the back-to-index flow) — no new endpoints, no new state shape.
(function setupCommandPalette() {
  const overlay = document.getElementById("cmdk-overlay");
  const input   = document.getElementById("cmdk-input");
  const list    = document.getElementById("cmdk-list");
  if (!overlay || !input || !list) return;

  let items = [];
  let activeIndex = 0;

  function buildItems() {
    const built = [];

    if (viewChat.classList.contains("active")) {
      Array.from(repoSelector.options).forEach((opt) => {
        if (!opt.value) return;
        built.push({
          group: "Switch repository",
          icon: "⇄",
          label: opt.value,
          hint: opt.value === currentRepo ? "current" : "",
          run: () => {
            repoSelector.value = opt.value;
            repoSelector.dispatchEvent(new Event("change"));
          },
        });
      });

      intentChips.forEach((chip) => {
        const prompt = chip.dataset.prompt;
        if (!prompt) return;
        built.push({
          group: "Ask",
          icon: "◈",
          label: prompt,
          hint: chip.textContent.trim(),
          run: () => {
            questionInput.value = prompt;
            autoResizeTextarea();
            questionInput.focus();
          },
        });
      });

      built.push({
        group: "Navigate",
        icon: "←",
        label: "Index another repo",
        hint: "",
        run: () => backToIndexBtn.click(),
      });
    } else {
      built.push({
        group: "Navigate",
        icon: "→",
        label: "Focus repository URL field",
        hint: "",
        run: () => repoUrlInput.focus(),
      });
      if (currentRepo) {
        built.push({
          group: "Navigate",
          icon: "→",
          label: `Resume chat with ${currentRepo}`,
          hint: "",
          run: () => switchToChat(currentRepo),
        });
      }
    }

    return built;
  }

  function render(filter) {
    const q = (filter || "").toLowerCase().trim();
    const filtered = items.filter(
      (it) => !q || it.label.toLowerCase().includes(q) || it.group.toLowerCase().includes(q)
    );

    list.innerHTML = "";
    if (!filtered.length) {
      list.innerHTML = `<div class="cmdk-empty">No matches</div>`;
      return;
    }

    let lastGroup = null;
    filtered.forEach((it, idx) => {
      if (it.group !== lastGroup) {
        const label = document.createElement("div");
        label.className = "cmdk-group-label";
        label.textContent = it.group;
        list.appendChild(label);
        lastGroup = it.group;
      }
      const row = document.createElement("div");
      row.className = "cmdk-item" + (idx === activeIndex ? " active" : "");
      row.innerHTML = `<span class="cmdk-item-icon">${it.icon}</span><span>${it.label}</span>${it.hint ? `<span class="cmdk-item-hint">${it.hint}</span>` : ""}`;
      row.addEventListener("mouseenter", () => {
        activeIndex = idx;
        render(input.value);
      });
      row.addEventListener("click", () => {
        it.run();
        close();
      });
      list.appendChild(row);
    });

    filtered._all = filtered; // stash for keyboard nav
    render._current = filtered;
  }

  function open() {
    items = buildItems();
    activeIndex = 0;
    overlay.classList.remove("hidden");
    input.value = "";
    render("");
    setTimeout(() => input.focus(), 10);
  }

  function close() {
    overlay.classList.add("hidden");
  }

  window.addEventListener("keydown", (e) => {
    const isK = e.key === "k" || e.key === "K";
    if ((e.metaKey || e.ctrlKey) && isK) {
      e.preventDefault();
      overlay.classList.contains("hidden") ? open() : close();
    } else if (e.key === "Escape" && !overlay.classList.contains("hidden")) {
      close();
    }
  });

  overlay.addEventListener("mousedown", (e) => {
    if (e.target === overlay) close();
  });

  input.addEventListener("input", () => {
    activeIndex = 0;
    render(input.value);
  });

  input.addEventListener("keydown", (e) => {
    const current = render._current || [];
    if (e.key === "ArrowDown") {
      e.preventDefault();
      activeIndex = Math.min(activeIndex + 1, current.length - 1);
      render(input.value);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      activeIndex = Math.max(activeIndex - 1, 0);
      render(input.value);
    } else if (e.key === "Enter") {
      e.preventDefault();
      const pick = current[activeIndex];
      if (pick) {
        pick.run();
        close();
      }
    }
  });
})();
