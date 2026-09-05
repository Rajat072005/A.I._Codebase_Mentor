"""
Live Indexing Routes
----------------------
Adds a new endpoint that indexes ANY public GitHub repo on demand, using
the real pipeline (repository_manager.reindex_repository) — instead of
the KNOWN_REPOS demo lookup that api.py's existing /index route uses.

api.py's existing /index endpoint is left completely untouched: it still
works exactly as before, for the cached demo repos. This file just adds
a second, separate endpoint alongside it.

WIRING (one addition to api.py, near the top where the app is created):

    from live_index_routes import live_index_bp
    app.register_blueprint(live_index_bp)

That's the only change needed in api.py.
"""

from flask import Blueprint, jsonify, request

from indexing import repository_manager
from utils import helpers

live_index_bp = Blueprint("live_index", __name__)


@live_index_bp.route("/index/live", methods=["POST"])
def index_live_repo():
    """
    Index ANY public GitHub repo (not just the cached demo ones).

    Request body:  { "url": "https://github.com/user/repo" }
    Success:       { "status": "ready", "repo_name": "...", "message": "..." }
    Failure:       { "status": "error", "message": "..." }   (4xx/5xx)

    Note on timing: this can take anywhere from under a minute to several
    minutes for a first-time index, depending on repo size — the
    frontend should show a loading state, not expect an instant reply.

    Note on rate limits: Gemini metadata failures during indexing do NOT
    surface here as errors — the batched metadata pipeline already
    absorbs those internally (falls back to placeholder metadata per
    file rather than raising). This endpoint only returns an error for
    things outside that: a bad/private/nonexistent repo URL, a clone
    failure, or an unexpected disk/network error.
    """
    data = request.get_json(silent=True) or {}
    repo_url = (data.get("url") or "").strip()

    if not repo_url:
        return jsonify({"status": "error", "message": "Please provide a repository URL."}), 400

    if "github.com" not in repo_url.lower():
        return jsonify({"status": "error", "message": "Only GitHub repository URLs are supported."}), 400

    try:
        stats = repository_manager.reindex_repository(repo_url)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"Indexing failed: {e}"
        }), 500

    #repo_name = helpers.extract_repo_name(repo_url)
    repo_name = stats["repo_name"]

    return jsonify({
        "status": "ready",
        "repo_name": repo_name,
        "file_count": stats["file_count"],
        "chunk_count": stats["chunk_count"],
        "message": f"'{repo_name}' indexed and ready to answer questions."
    })
