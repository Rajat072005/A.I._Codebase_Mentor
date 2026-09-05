

from flask import Blueprint, jsonify, request

from indexing import repository_manager
from utils import helpers

live_index_bp = Blueprint("live_index", __name__)

@live_index_bp.route("/index/live", methods=["POST"])
def index_live_repo():

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

                                                    
    repo_name = stats["repo_name"]

    return jsonify({
        "status": "ready",
        "repo_name": repo_name,
        "file_count": stats["file_count"],
        "chunk_count": stats["chunk_count"],
        "message": f"'{repo_name}' indexed and ready to answer questions."
    })
