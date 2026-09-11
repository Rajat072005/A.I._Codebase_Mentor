/**
 * AI Codebase Mentor — Frontend App
 * Handles: view switching, indexing flow (demo), and the Q&A chat interface.
 */

const API = "";

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

  // Regex for valid GitHub URLs
  const githubRegex = /^https?:\/\/(www\.)?github\.com\/[\w.-]+\/[\w.-]+\/?$/;
  if (!githubRegex.test(url)) {
    showIndexError("Invalid GitHub URL. Format: https://github.com/username/repository");
    return;
  }
  
  // Fast-skip: if already indexed, jump directly to chat
  try {
    const parts = url.replace(/\/$/, "").split("/");
    let repoName = parts.pop().replace(".git", "");
    let repoUser = parts.pop();
    let expectedName = `${repoUser}_${repoName}`;
    
    const res = await fetch(`${API}/repos`);
    const repos = await res.json();
    if (repos.includes(expectedName)) {
      currentRepo = expectedName;
      saveToMyRepos(expectedName);
      switchToChat(expectedName);
      return;
    }
  } catch (err) {
    // Ignore and proceed to normal indexing
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

function saveToMyRepos(repoName) {
  let myRepos = JSON.parse(localStorage.getItem("myRepos") || "[]");
  if (!myRepos.includes(repoName)) {
    myRepos.unshift(repoName);
    localStorage.setItem("myRepos", JSON.stringify(myRepos));
  }
}

async function loadRepos(preferredRepo) {
  try {
    const res = await fetch(`${API}/repos`);
    const allRepos = await res.json();

    repoSelector.innerHTML = "";

    if (preferredRepo) saveToMyRepos(preferredRepo);

    // The chat sidebar intentionally shows only repos *this browser* has
    // indexed or opened before — not the full global pool. Global Repos
    // stays a discovery surface (home page + ⌘K); once you're in a chat,
    // seeing every repo anyone has ever indexed would just be noise.
    const myRepos = JSON.parse(localStorage.getItem("myRepos") || "[]").filter((r) => allRepos.includes(r));

    if (!myRepos.length) {
      repoSelector.innerHTML = '<option value="">No repos yet — index one from the home page</option>';
      currentRepo = null;
      return;
    }

    myRepos.forEach((repo) => {
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
    return;
  }
  // Recall the last question you sent when the box is empty — mirrors the
  // familiar "up arrow to edit your last message" pattern from Slack/Discord.
  if (e.key === "ArrowUp" && questionInput.value === "" && lastUserQuestion) {
    e.preventDefault();
    questionInput.value = lastUserQuestion;
    autoResizeTextarea();
    requestAnimationFrame(() => questionInput.setSelectionRange(lastUserQuestion.length, lastUserQuestion.length));
  }
});

questionInput.addEventListener("input", autoResizeTextarea);

let lastUserQuestion = "";

async function sendMessage() {
  const question = questionInput.value.trim();
  if (!question || isWaiting || !currentRepo) return;

  clearWelcomeMessage();

  // Render user message
  appendMessage("user", question);
  lastUserQuestion = question;
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
      appendMessage("ai", `⚠️ Error: ${data.error}`, null, null, true);
    } else {
      appendMessage("ai", data.answer, data.intent, data.confidence);
    }
  } catch (err) {
    thinkingEl.remove();
    appendMessage("ai", "⚠️ Could not reach the server. Make sure api.py is running. Try pasting a fresh API key in Settings if you've hit the limit.", null, null, true);
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

// Follow-up prompts by intent — same idea as the sidebar chips, but
// surfaced right where the user just got an answer, so the next question
// is one click away instead of a trip back up to the sidebar.
const FOLLOWUP_POOL = {
  overview:       ["Explain the folder structure", "What's the tech stack?", "Where should I start reading?"],
  architecture:   ["Walk me through the data flow", "How do the main modules connect?", "Any circular dependencies?"],
  implementation: ["Show me the relevant code", "Are there tests for this?", "What edge cases are handled?"],
  locate:         ["How is this file used elsewhere?", "What calls into this?", "Show related files"],
  debug:          ["What could cause this to fail silently?", "Suggest a fix", "How would I reproduce this?"],
  casual:         ["Give me a codebase overview", "What should I explore first?", "Explain the architecture"],
};

function appendMessage(role, text, intent, confidence, isError) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}` + (isError ? " is-error" : "");

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
  const time = document.createElement("span");
  time.className = "message-time";
  time.textContent = new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  sender.appendChild(time);

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

  // Copy button — reads the bubble's rendered text at click time, so it
  // works correctly even though the text isn't filled in until below.
  // Skipped for error bubbles — there's nothing useful to copy or follow up on.
  if (role === "ai" && !isError) {
    const actions = document.createElement("div");
    actions.className = "message-actions";
    const copyBtn = document.createElement("button");
    copyBtn.type = "button";
    copyBtn.className = "message-action-btn";
    copyBtn.textContent = "⧉ Copy answer";
    copyBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(bubble.innerText);
        copyBtn.textContent = "✓ Copied";
        copyBtn.classList.add("copied");
      } catch {
        copyBtn.textContent = "Select & copy";
      }
      setTimeout(() => {
        copyBtn.textContent = "⧉ Copy answer";
        copyBtn.classList.remove("copied");
      }, 1500);
    });
    actions.appendChild(copyBtn);
    wrapper.appendChild(actions);
  }

  messagesArea.appendChild(wrapper);
  handleNewMessage(role); // registers this message once — decides scroll + unread count

  // Render content — AI text streams in; plain text (user messages) is instant.
  if (role === "ai" && typeof marked !== "undefined") {
    streamMarkdownInto(bubble, text || "", () => {
      enhanceInlineRefs(bubble);
      if (intent) appendFollowups(wrapper, intent);
      scrollToBottomIfFollowing(); // just follow growth, don't re-count this message
    });
  } else {
    bubble.textContent = text || "";
  }

  return wrapper;
}

// Suggests 3 low-friction next questions under a finished AI answer.
function appendFollowups(wrapper, intent) {
  const key = String(intent || "").toLowerCase().trim();
  const pool = FOLLOWUP_POOL[key];
  if (!pool) return;

  const row = document.createElement("div");
  row.className = "message-followups";
  pool.slice(0, 3).forEach((prompt) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "followup-chip";
    chip.textContent = prompt;
    chip.addEventListener("click", () => {
      questionInput.value = prompt;
      autoResizeTextarea();
      questionInput.focus();
    });
    row.appendChild(chip);
  });
  wrapper.appendChild(row);
  scrollToBottomIfFollowing();
}

// Styles inline code that looks like a file path (has a slash and a
// plausible extension) as a small reference chip — purely a style pass
// over content the backend already returned, no new data involved.
function enhanceInlineRefs(bubble) {
  const pathPattern = /^[\w.\-/]+\/[\w.\-]+\.[a-zA-Z0-9]{1,6}$/;
  bubble.querySelectorAll("code").forEach((el) => {
    if (el.closest("pre")) return; // code blocks are handled separately
    if (pathPattern.test(el.textContent.trim())) {
      el.classList.add("file-ref");
    }
  });
}

// Reveals markdown a few words at a time, re-parsing the growing string on
// each tick so formatting (bold, lists, code fences) is always valid by the
// time it's shown. Falls back to an instant render for very short strings.
function streamMarkdownInto(bubble, fullText, onComplete) {
  const words = fullText.split(/(\s+)/); // keep whitespace tokens so spacing survives
  if (words.length <= 6) {
    bubble.innerHTML = marked.parse(fullText);
    enhanceCodeBlocks(bubble);
    if (onComplete) onComplete();
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
    scrollToBottomIfFollowing();

    if (i < words.length) {
      setTimeout(tick, 16);
    } else {
      bubble.classList.remove("streaming");
      caret.remove();
      bubble.innerHTML = marked.parse(fullText); // final, guaranteed-correct render
      enhanceCodeBlocks(bubble);
      scrollToBottomIfFollowing();
      if (onComplete) onComplete();
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
  scrollToBottomIfFollowing();
  return wrapper;
}

function clearWelcomeMessage() {
  const welcome = messagesArea.querySelector(".welcome-message");
  if (welcome) welcome.remove();
}

function scrollToBottom() {
  messagesArea.scrollTop = messagesArea.scrollHeight;
}

function distanceFromBottom() {
  return messagesArea.scrollHeight - messagesArea.scrollTop - messagesArea.clientHeight;
}

// The single source of truth for "should new content pull the view down".
// Only changes on a real user scroll — never re-derived from geometry at
// content-mutation time, which is what caused the false trip: the
// thinking indicator growing the page a moment after auto-scrolling was
// enough to make a geometry re-check think the user had scrolled away,
// even though nothing had actually moved under them.
let followMode = true;
let unseenAiCount = 0;

// Call once per new top-level message (user or ai) to decide whether to
// scroll and whether it counts toward the unread badge.
function handleNewMessage(role) {
  if (role === "user") followMode = true; // sending implies "show me the reply"
  if (followMode) {
    scrollToBottom();
    unseenAiCount = 0;
  } else if (role === "ai") {
    unseenAiCount++;
  }
  updateJumpLatest();
}

// Call for incremental growth within an already-registered message
// (thinking dots, streaming ticks, follow-up chips appearing) — follows
// along if the user is following, otherwise does nothing. Doesn't touch
// the unread count, so a single answer never gets counted twice.
function scrollToBottomIfFollowing() {
  if (followMode) scrollToBottom();
}

function updateJumpLatest() {
  const btn = document.getElementById("jump-latest");
  const label = document.getElementById("jump-latest-label");
  if (!btn || !label) return;
  if (unseenAiCount > 0 && !followMode) {
    label.textContent = unseenAiCount === 1 ? "New message" : `${unseenAiCount} new messages`;
    btn.classList.remove("hidden");
  } else {
    btn.classList.add("hidden");
  }
}

(function setupJumpLatest() {
  const btn = document.getElementById("jump-latest");
  if (!btn) return;
  btn.addEventListener("click", () => {
    followMode = true;
    scrollToBottom();
    unseenAiCount = 0;
    updateJumpLatest();
  });
  // The only place followMode is ever set from geometry: an actual user
  // scroll gesture. Landing back near the bottom re-enables auto-follow;
  // scrolling away disables it. Content growth alone never touches this.
  messagesArea.addEventListener("scroll", () => {
    followMode = distanceFromBottom() < 80;
    if (followMode) unseenAiCount = 0;
    updateJumpLatest();
  });
})();

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

  const CELLS = 32; // single slim row now — see the CSS note on why
  grid.innerHTML = "";
  const cells = [];
  for (let i = 0; i < CELLS; i++) {
    const cell = document.createElement("div");
    cell.className = "cell";
    grid.appendChild(cell);
    cells.push(cell);
  }

  let active = true;
  (function loop() {
    if (!active) return;
    const n = 1 + Math.floor(Math.random() * 2);
    for (let i = 0; i < n; i++) {
      const c = cells[Math.floor(Math.random() * cells.length)];
      c.classList.remove("lit", "lit-violet");
      c.classList.add(Math.random() > 0.5 ? "lit" : "lit-violet");
      setTimeout(() => c.classList.remove("lit", "lit-violet"), 500);
    }
    setTimeout(loop, 110);
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
// Reuses existing functions only (switchToChat, intent chips' prompts, the
// back-to-index flow) — no new endpoints, no new state shape.
const commandPalette = (function setupCommandPalette() {
  const overlay = document.getElementById("cmdk-overlay");
  const input   = document.getElementById("cmdk-input");
  const list    = document.getElementById("cmdk-list");
  if (!overlay || !input || !list) return { open: () => {} };

  let items = [];
  let activeIndex = 0;
  let currentScope = "all"; // "all" | "global"

  // Builds the full item list, including every indexed repo (not just the
  // ones already loaded into the sidebar's <select>) — this is what makes
  // "search global" actually work from the home page, where the select
  // hasn't been populated with anything yet.
  async function buildItems(scope) {
    const built = [];
    const inChat = viewChat.classList.contains("active");

    let allRepos = [];
    try {
      const res = await fetch(`${API}/repos`);
      allRepos = await res.json();
    } catch {
      /* server unreachable — repo groups just won't appear below */
    }

    if (allRepos.length) {
      const myRepos = JSON.parse(localStorage.getItem("myRepos") || "[]").filter((r) => allRepos.includes(r));
      const globalRepos = allRepos.filter((r) => !myRepos.includes(r));

      // "My Repos" is already visible as its own list on the home page and
      // in the sidebar, so a *global search* only needs to surface repos
      // outside that list — showing both there was pure duplication.
      if (scope !== "global") {
        myRepos.forEach((repo) => {
          built.push({
            group: "My Repos",
            icon: "⌬",
            label: repo,
            hint: repo === currentRepo ? "current" : "",
            run: () => switchToChat(repo),
          });
        });
      }

      globalRepos.forEach((repo) => {
        built.push({
          group: "Global Repos",
          icon: "◈",
          label: repo,
          hint: "",
          run: () => switchToChat(repo),
        });
      });
    }

    if (scope === "global") return built; // repos only — no chips/navigation noise

    if (inChat) {
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
        label: "Index a new repository",
        hint: "",
        run: () => repoUrlInput.focus(),
      });
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
      const emptyMsg = currentScope === "global"
        ? "No other indexed repositories found yet."
        : "No matches";
      list.innerHTML = `<div class="cmdk-empty">${emptyMsg}</div>`;
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
        // Just update classes instead of rebuilding the entire DOM
        const currentActive = list.querySelector(".cmdk-item.active");
        if (currentActive) currentActive.classList.remove("active");
        row.classList.add("active");
        activeIndex = idx;
      });
      
      row.addEventListener("click", () => {
        try {
          it.run();
        } catch (err) {
          console.error("Command palette action failed:", err);
        }
        close();
      });
      list.appendChild(row);
    });

    render._current = filtered;
  }

  async function open(opts) {
    currentScope = (opts && opts.scope) || "all";
    activeIndex = 0;
    overlay.classList.remove("hidden");
    input.value = "";
    input.placeholder = currentScope === "global"
      ? "Search all globally indexed repositories…"
      : "Jump to a repo, ask something, or start over…";
    list.innerHTML = `<div class="cmdk-empty">Loading repositories…</div>`;
    setTimeout(() => input.focus(), 10);

    try {
      items = await buildItems(currentScope);
    } catch (err) {
      console.error("Command palette failed to load items:", err);
      items = [];
    }
    render("");
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

  return { open };
})();


// ═══════════════════════════════════════════════════════════════════════════
// Round 3 — indexing-time engagement, ⌘K onboarding, custom repo switcher
// Same rule as before: presentation and convenience only. Nothing here
// calls a new endpoint or changes what gets sent to the backend.
// ═══════════════════════════════════════════════════════════════════════════

// ── Terminal-style log during indexing ──────────────────────────────────
// Deliberately generic ("chunking source…", not invented filenames) so it
// never implies data we don't actually have.
function animateTerminalLog() {
  const el = document.getElementById("terminal-log");
  if (!el) return () => {};

  const LINES = [
    "resolving repository structure…",
    "walking directory tree…",
    "skipping node_modules, .git…",
    "reading source files…",
    "tokenizing source…",
    "chunking by function & class boundaries…",
    "embedding batch 1/9…", "embedding batch 2/9…", "embedding batch 3/9…",
    "embedding batch 4/9…", "embedding batch 5/9…", "embedding batch 6/9…",
    "writing to vector index…",
    "building symbol map…",
    "cross-referencing imports…",
    "finalizing index…",
  ];

  el.innerHTML = "";
  let i = 0;
  let active = true;

  function pushLine(text) {
    const line = document.createElement("div");
    line.className = "log-line";
    line.innerHTML = `<span class="log-prefix">›</span>${text}`;
    el.appendChild(line);
    while (el.children.length > 6) el.removeChild(el.firstChild);
    el.scrollTop = el.scrollHeight;
  }

  (function loop() {
    if (!active) return;
    pushLine(LINES[i % LINES.length]);
    i++;
    setTimeout(loop, 260 + Math.random() * 220);
  })();

  return function stop() {
    active = false;
    pushLine("done.");
  };
}

// Chain onto the same wrapper that already drives the file grid.
const _origRunIndexingAnimation2 = runIndexingAnimation;
runIndexingAnimation = async function (url) {
  const stopLog = animateTerminalLog();
  const stopTip = animateProgressTips();
  await _origRunIndexingAnimation2(url);
  stopLog();
  stopTip();
};

// ── Rotating capability tips ─────────────────────────────────────────────
function animateProgressTips() {
  const el = document.getElementById("progress-tip");
  if (!el) return () => {};

  const TIPS = [
    "Tip: ask about architecture, not just individual files.",
    "Tip: press ⌘K anywhere to jump to a repo or a question.",
    "Tip: \"Help me debug the login issue\" works — try a real bug.",
    "Tip: you can queue a question above while this finishes.",
    "Tip: answers cite the actual code retrieved, not guesses.",
  ];

  let i = 0;
  el.textContent = TIPS[0];
  const id = setInterval(() => {
    el.classList.add("fade");
    setTimeout(() => {
      i = (i + 1) % TIPS.length;
      el.textContent = TIPS[i];
      el.classList.remove("fade");
    }, 300);
  }, 3200);

  return function stop() {
    clearInterval(id);
    el.textContent = "";
  };
}

// ── Queue a question while indexing runs ────────────────────────────────
let queuedQuestion = "";

const queuedInput = document.getElementById("queued-question-input");
if (queuedInput) {
  queuedInput.addEventListener("input", () => {
    queuedQuestion = queuedInput.value;
  });
}

const _origSwitchToChat = switchToChat;
switchToChat = async function (repoName) {
  await _origSwitchToChat(repoName);
  if (queuedQuestion.trim()) {
    questionInput.value = queuedQuestion.trim();
    autoResizeTextarea();
  }
  maybeShowCmdkHint();
};

// Reset the queue field whenever indexing is restarted.
backToIndexBtn.addEventListener("click", () => {
  queuedQuestion = "";
  if (queuedInput) queuedInput.value = "";
});

// ── ⌘K onboarding hint (shown once, via localStorage — this is a real
//    site the user downloads and hosts, not a claude.ai artifact, so
//    normal browser storage is the right tool here) ─────────────────────
function maybeShowCmdkHint() {
  const hint = document.getElementById("cmdk-hint");
  if (!hint) return;
  let seen = false;
  try { seen = localStorage.getItem("mentor_cmdk_hint_seen") === "1"; } catch {}
  if (seen) return;

  hint.classList.remove("hidden");
  const dismiss = () => {
    hint.classList.add("leaving");
    setTimeout(() => hint.classList.add("hidden"), 300);
    try { localStorage.setItem("mentor_cmdk_hint_seen", "1"); } catch {}
    window.removeEventListener("keydown", onAnyKey);
  };
  const onAnyKey = (e) => {
    if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) dismiss();
  };
  window.addEventListener("keydown", onAnyKey);
  setTimeout(dismiss, 6000);
}

// ── Custom repo switcher — a styled button + panel that drives the real
//    (visually hidden) <select>, so every existing behavior that reads
//    repoSelector.value or listens for its "change" event keeps working. ──
(function setupRepoSwitcher() {
  const wrap    = document.getElementById("repo-switcher");
  const trigger = document.getElementById("repo-switcher-trigger");
  const current = document.getElementById("repo-switcher-current");
  const panel   = document.getElementById("repo-switcher-panel");
  if (!wrap || !trigger || !panel) return;

  // Move the panel to <body> and drive it with position:fixed, computed
  // from the trigger's own coordinates. This is the fix for the dropdown
  // rendering behind/underneath sidebar content — nesting it inside a
  // normal-flow sidebar meant it could get clipped or out-stacked by
  // sibling sections depending on their own layout. As a fixed layer on
  // <body> it always paints above everything, unconditionally.
  document.body.appendChild(panel);

  function position() {
    const r = trigger.getBoundingClientRect();
    panel.style.left  = `${r.left}px`;
    panel.style.top   = `${r.bottom + 6}px`;
    panel.style.width = `${r.width}px`;
  }

  function sync() {
    const opts = Array.from(repoSelector.options).filter((o) => o.value);
    current.textContent = repoSelector.selectedOptions[0]?.textContent || "No repos available";
    trigger.disabled = opts.length === 0;

    panel.innerHTML = "";

    function renderItem(opt) {
      const item = document.createElement("div");
      item.className = "repo-switcher-item" + (opt.value === repoSelector.value ? " selected" : "");
      item.setAttribute("role", "option");
      item.textContent = opt.value;
      item.addEventListener("click", () => {
        repoSelector.value = opt.value;
        repoSelector.dispatchEvent(new Event("change"));
        close();
      });
      panel.appendChild(item);
    }

    // Mirror the <select>'s own grouping (My Repos / Global Repos) instead
    // of a flat list, so the two surfaces stay visually consistent.
    const groups = repoSelector.querySelectorAll("optgroup");
    if (groups.length) {
      groups.forEach((group) => {
        const label = document.createElement("div");
        label.className = "repo-switcher-group-label";
        label.textContent = group.label;
        panel.appendChild(label);
        Array.from(group.children).forEach(renderItem);
      });
    } else {
      opts.forEach(renderItem);
    }
  }

  function open() {
    sync();
    position();
    wrap.classList.add("open");
    panel.classList.remove("hidden");
    trigger.setAttribute("aria-expanded", "true");
  }
  function close() {
    wrap.classList.remove("open");
    panel.classList.add("hidden");
    trigger.setAttribute("aria-expanded", "false");
  }

  trigger.addEventListener("click", () => {
    panel.classList.contains("hidden") ? open() : close();
  });
  document.addEventListener("click", (e) => {
    if (!wrap.contains(e.target) && !panel.contains(e.target)) close();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
  // A fixed-position panel doesn't move with the page, so if the trigger
  // moves under it (scroll/resize) just close rather than show a stale spot.
  window.addEventListener("scroll", () => { if (!panel.classList.contains("hidden")) close(); }, true);
  window.addEventListener("resize", () => { if (!panel.classList.contains("hidden")) close(); });

  // Keep the label in sync no matter what changed the select (custom panel,
  // the command palette, or loadRepos populating it after an index run).
  repoSelector.addEventListener("change", sync);
  const _origLoadRepos = loadRepos;
  loadRepos = async function (preferredRepo) {
    await _origLoadRepos(preferredRepo);
    sync();
  };

  sync();
})();

// ── Hero code-preview annotation rotation (purely decorative) ──────────
(function setupPreviewAnnotation() {
  const el = document.getElementById("preview-annotation");
  if (!el) return;
  const MESSAGES = [
    "✓ traced → getUser(payload.sub)",
    "✓ flagged: no expiry check",
    "✓ linked to 3 call sites",
  ];
  let i = 0;
  // Matches the 4.6s CSS animation duration so the text changes while the
  // annotation is invisible (start of its cycle), never mid-fade.
  setInterval(() => {
    i = (i + 1) % MESSAGES.length;
    el.textContent = MESSAGES[i];
  }, 4600);
})();

// ═══════════════════════════════════════════════════════════════════════════
// API KEY & SETTINGS MODAL
// ═══════════════════════════════════════════════════════════════════════════

const settingsOverlay = document.getElementById("settings-overlay");
const settingsClose = document.getElementById("settings-close");
const settingsSaveBtn = document.getElementById("settings-save-btn");
const settingsSaveStatus = document.getElementById("settings-save-status");
const apiKeyInput = document.getElementById("api-key-input");
const apiKeyToggle = document.getElementById("api-key-toggle");
const btnSettingsIndex = document.getElementById("settings-btn-index");
const btnSettingsChat = document.getElementById("settings-btn-chat");
const settingsDemoBtn = document.getElementById("settings-demo-btn");

function openSettings() {
  apiKeyInput.value = localStorage.getItem("geminiApiKey") || "";
  settingsOverlay.classList.remove("hidden");
  settingsSaveStatus.classList.remove("visible");
  setTimeout(() => apiKeyInput.focus(), 10);
}

function closeSettings() {
  settingsOverlay.classList.add("hidden");
}

function saveApiKey() {
  const key = apiKeyInput.value.trim();
  if (key) {
    localStorage.setItem("geminiApiKey", key);
    settingsSaveStatus.textContent = "✓ Key saved";
  } else {
    localStorage.removeItem("geminiApiKey");
    settingsSaveStatus.textContent = "✓ Demo Mode Activated";
  }
  settingsSaveStatus.classList.add("visible");
  setTimeout(closeSettings, 500);
}

if (apiKeyToggle) {
  apiKeyToggle.addEventListener("click", () => {
    const showing = apiKeyInput.type === "text";
    apiKeyInput.type = showing ? "password" : "text";
    apiKeyToggle.textContent = showing ? "👁" : "🙈";
    apiKeyToggle.title = showing ? "Show key" : "Hide key";
  });
}

if (btnSettingsIndex) btnSettingsIndex.addEventListener("click", openSettings);
if (btnSettingsChat) btnSettingsChat.addEventListener("click", openSettings);
if (settingsClose) settingsClose.addEventListener("click", closeSettings);
if (settingsSaveBtn) settingsSaveBtn.addEventListener("click", saveApiKey);

if (settingsDemoBtn) {
  settingsDemoBtn.addEventListener("click", () => {
    apiKeyInput.value = "";
    saveApiKey();
  });
}
if (apiKeyInput) {
  apiKeyInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") saveApiKey();
  });
}
overlayClickToClose(settingsOverlay, closeSettings);

// Shared helper: click on the dimmed backdrop (not the panel itself) closes
// the modal — same convention as the command palette overlay.
function overlayClickToClose(overlay, close) {
  if (!overlay) return;
  overlay.addEventListener("mousedown", (e) => {
    if (e.target === overlay) close();
  });
}

// Inject the API key into fetch calls
const originalFetch = window.fetch;
window.fetch = async (...args) => {
  let [resource, config] = args;
  const key = localStorage.getItem("geminiApiKey");
  if (key) {
    config = config || {};
    config.headers = { ...config.headers, "X-Gemini-Key": key };
    args[1] = config;
  }
  return originalFetch(...args);
};

// Override the click handlers for index and ask to ensure key exists
const _origStartIndexingFinal = startIndexing;
startIndexing = async function () {
  if (!localStorage.getItem("geminiApiKey")) {
    openSettings();
    return;
  }
  return _origStartIndexingFinal();
};
indexBtn.removeEventListener("click", _origStartIndexingFinal);
indexBtn.addEventListener("click", startIndexing);

const _origSendMessageFinal = sendMessage;
sendMessage = async function () {
  if (!localStorage.getItem("geminiApiKey")) {
    openSettings();
    return;
  }
  return _origSendMessageFinal();
};
// Re-bind the click event
sendBtn.removeEventListener("click", _origSendMessage);
sendBtn.addEventListener("click", sendMessage);

// ═══════════════════════════════════════════════════════════════════════════
// HOME EXPLORE SECTION
// ═══════════════════════════════════════════════════════════════════════════

async function renderHomeRepos() {
  const listEl = document.getElementById("home-my-repos-list");
  if (!listEl) return;
  
  try {
    const res = await fetch(`${API}/repos`);
    const globalRepos = await res.json();
    let myRepos = JSON.parse(localStorage.getItem("myRepos") || "[]");
    myRepos = myRepos.filter(r => globalRepos.includes(r));
    
    listEl.innerHTML = "";
    if (myRepos.length === 0) {
      listEl.innerHTML = `<div class="explore-empty">You haven't indexed any repositories yet.<br>Paste a GitHub link above to get started!</div>`;
      return;
    }
    
    myRepos.forEach(repo => {
      const item = document.createElement("div");
      item.className = "explore-item";
      item.innerHTML = `
        <span class="explore-item-name">${repo}</span>
        <div class="explore-item-controls">
          <button class="remove-repo-btn" title="Remove from My Repos">✕</button>
          <span class="explore-item-action">Chat →</span>
        </div>
      `;
      
      // Click on the card to chat
      item.addEventListener("click", (e) => {
        if (e.target.closest(".remove-repo-btn")) return; // Ignore if they clicked delete
        switchToChat(repo);
      });
      
      // Click on delete button
      const removeBtn = item.querySelector(".remove-repo-btn");
      removeBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        let currentRepos = JSON.parse(localStorage.getItem("myRepos") || "[]");
        currentRepos = currentRepos.filter(r => r !== repo);
        localStorage.setItem("myRepos", JSON.stringify(currentRepos));
        renderHomeRepos(); // Re-render the list immediately
      });
      
      listEl.appendChild(item);
    });
  } catch (err) {
    listEl.innerHTML = `<div class="explore-empty">Could not load repositories. Make sure api.py is running.</div>`;
  }
}

const homeSearchBtn = document.getElementById("home-search-btn");
if (homeSearchBtn) {
  homeSearchBtn.addEventListener("click", () => commandPalette.open({ scope: "global" }));
}

// Initial render
renderHomeRepos();

// Re-render when returning to home view
backToIndexBtn.addEventListener("click", () => {
  renderHomeRepos();
});
