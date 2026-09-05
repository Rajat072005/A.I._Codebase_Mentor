"""
Flask API — AI Codebase Mentor
--------------------------------
Exposes three endpoints for the frontend:

  GET  /repos        → list all indexed repos available in data/
  POST /index        → demo indexing step (uses cached data for V1)
  POST /ask          → run the full Q&A pipeline and return an answer
"""

from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from core.confidence_handler import build_low_confidence_message, should_answer
from core.context_builder import build_context
from core.prompt_builder import build_prompt
from core.question_classifier import classify_question
from core.retrieval_strategy import get_strategy
from core.strategy_executor import execute_strategy
from live_index_routes import live_index_bp
from llm.llm_explainer import generate_answer
from utils import storage
from utils.helpers import build_chunkmap, build_embeddingmap

app = Flask(__name__, static_folder="frontend", static_url_path="")   
app.register_blueprint(live_index_bp)
CORS(app)

DATA_DIR = Path("data")

# In-memory cache of loaded repo data (avoid reloading JSON on every request)
_repo_cache = {}

# Map of known repo URLs to their cached folder names (for the demo indexing step)
KNOWN_REPOS = {
    "syncsphere": "SyncSphere-Website",
    "leet":       "LeetMetrics-WebApp",
}


def _load_repo(repo_name):
    """
    Load a repo's chunks and embeddings into memory (cached after first load).
    Raises FileNotFoundError if the repo data doesn't exist.
    """
    if repo_name not in _repo_cache:
        folder = DATA_DIR / repo_name
        chunks_path = folder / "chunks.json"

        if not chunks_path.exists():
            raise FileNotFoundError(f"No indexed data found for repo: {repo_name}")

        chunks = storage.load_json(str(folder / "chunks.json"))
        embeddings = storage.load_json(str(folder / "embeddings.json"))

        _repo_cache[repo_name] = {
            "chunks": chunks,
            "embeddings": embeddings,
            "chunk_map": build_chunkmap(chunks),
        }

    return _repo_cache[repo_name]


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def serve_frontend():
    """Serve the frontend index.html."""
    return app.send_static_file("index.html")


@app.route("/repos", methods=["GET"])
def get_repos():
    """Return a list of all repos that have been indexed (have chunks.json)."""
    repos = []
    if DATA_DIR.exists():
        for folder in DATA_DIR.iterdir():
            if folder.is_dir() and (folder / "chunks.json").exists():
                repos.append(folder.name)
    return jsonify(repos)

@app.route("/repos/<repo_name>/stats", methods=["GET"])
def get_repo_stats(repo_name):
    """Return file/chunk counts for any already-indexed repo, by reading its chunks.json."""
    folder = DATA_DIR / repo_name
    chunks_path = folder / "chunks.json"
    if not chunks_path.exists():
        return jsonify({"error": "Repo not found."}), 404

    chunks = storage.load_json(str(chunks_path))
    return jsonify({
        "file_count": len({c["path"] for c in chunks}),
        "chunk_count": len(chunks),
    })


@app.route("/index", methods=["POST"])
def index_repo():
    """
    Demo indexing endpoint.

    For V1, we only support pre-cached repos. This endpoint simulates the
    indexing flow for the judges by returning metadata about the cached repo
    without actually re-running the expensive indexing pipeline.
    """
    data = request.get_json()
    repo_url = (data.get("url") or "").strip()

    if not repo_url:
        return jsonify({"error": "Please provide a repository URL."}), 400

    # Match the URL against our known cached repos
    matched_name = None
    for key, name in KNOWN_REPOS.items():
        if key.lower() in repo_url.lower():
            matched_name = name
            break

    if not matched_name:
        return jsonify({
            "error": "This repository is not in the V1 demo cache. Only SyncSphere-Website and LeetMetrics-WebApp are supported."
        }), 400

    folder = DATA_DIR / matched_name
    if not (folder / "chunks.json").exists():
        return jsonify({"error": "Cached data not found for this repository."}), 404

    # Load summary stats from cached data
    chunks = storage.load_json(str(folder / "chunks.json"))
    file_count = len({c["path"] for c in chunks})
    chunk_count = len(chunks)

    return jsonify({
        "repo_name": matched_name,
        "status": "ready",
        "file_count": file_count,
        "chunk_count": chunk_count,
        "message": f"'{matched_name}' is indexed and ready to answer questions."
    })


@app.route("/ask", methods=["POST"])
def ask():
    """
    Main Q&A endpoint.

    Request body: { "repo": "SyncSphere-Website", "question": "How does auth work?" }
    Response:     { "answer": "...", "intent": "implementation", "confidence": 8 }
    """
    data = request.get_json()
    repo_name = (data.get("repo") or "").strip()
    question = (data.get("question") or "").strip()

    if not repo_name or not question:
        return jsonify({"error": "Both 'repo' and 'question' are required."}), 400

    # Load repo data
    try:
        repo = _load_repo(repo_name)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    # Step 1 — Classify the question into one of 7 intents
    intent = classify_question(question)

    # Step 2 — Handle casual questions (no retrieval needed)
    if intent == "casual":
        prompt = build_prompt(intent, question, "")
        answer = generate_answer(prompt)
        return jsonify({
            "answer": answer or "Sorry, I couldn't generate a response.",
            "intent": intent,
            "confidence": None
        })

    # Step 3 — Non-casual: run retrieval pipeline
    strategy = get_strategy(intent)

    context_chunks, top_score = execute_strategy(
        question,
        strategy,
        repo["chunks"],
        repo["chunk_map"],
        repo["embeddings"]
    )

    # Step 4 — Check confidence
    if should_answer(top_score, strategy["confidence_threshold"]):
        context = build_context(repo["chunk_map"], context_chunks)
        prompt = build_prompt(intent, question, context)
        answer = generate_answer(prompt)
    else:
        answer = build_low_confidence_message(question)

    return jsonify({
        "answer": answer or "Sorry, I couldn't generate a response.",
        "intent": intent,
        "confidence": top_score
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
