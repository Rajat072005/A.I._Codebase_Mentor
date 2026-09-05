"""
LLM Metadata Batch Generator
-----------------------------
Batched version of llm_metadata_generator.py.

Instead of one Gemini call per file, groups several files into a single
call (respecting a rough token budget) and asks for metadata on all of
them at once, returned as a JSON array. This is what actually fixes the
rate-limit problem: fewer calls, not smarter waiting.

If a batch call fails (rate limit, malformed output, size mismatch) after
retries, it is bisected into two smaller batches and retried recursively,
all the way down to single files if needed. At single-file granularity it
falls back to the ORIGINAL, untouched llm_metadata_generator.py — so the
prompt and quality for any file that needs individual handling is exactly
what you already had. Batching only changes call volume, never quality.

Nothing in this file is imported by your existing modules, so it cannot
break anything until you wire it in yourself (see batch_indexer.py).
"""

import json
import time
import random
import google.generativeai as genai

from indexing import llm_metadata_generator  

_model = genai.GenerativeModel("gemini-3.6-flash")

# ── Tuning knobs ────────────────────────────────────────────────────────
MAX_TOKENS_PER_BATCH = 6000     # rough char/4 budget per batch — keeps prompts safely sized
MAX_FILES_PER_BATCH = 10        # hard cap regardless of token budget
MAX_RETRIES = 5                 # per batch/file, before bisecting or giving up
BATCH_DELAY_SECONDS = 3         # small courtesy delay after each successful batch call

_BATCH_PROMPT_TEMPLATE = """
You are an expert software architect analyzing multiple source code files
from the same repository, in a single pass.

CRITICAL: Analyze each file completely independently. Do not let one
file's content, purpose, naming, or style influence another file's
metadata. Treat each file as if it were the only file you had ever seen.

For EACH file below, generate:
  - purpose         : one or two sentences describing what the file does
  - responsibilities: 3-5 high-level responsibilities
  - concepts        : 3-6 important software engineering concepts present
  - keywords        : 5-10 retrieval-friendly keywords

Rules:
1. Analyze only what is visible in each file's own content.
2. Focus on architectural understanding, not line-by-line implementation.
3. Return a JSON array with exactly {file_count} objects, one per file,
   in the SAME ORDER as the files are given below.
4. Each object must have this exact shape:
   {{"path": "<the file's path as given>", "purpose": "", "responsibilities": [], "concepts": [], "keywords": []}}
5. Return only valid JSON. No markdown fences. No explanation outside the JSON.

Files:

{files_block}
"""


def _estimate_tokens(text):
    return max(1, len(text) // 4)  # rough heuristic: ~4 chars per token


def build_batches(files):
    """
    Group files into token-budget-aware batches.
    `files` is a list of {"path": ..., "content": ...} dicts (cache misses only).
    """
    batches = []
    current, current_tokens = [], 0

    for f in files:
        tokens = _estimate_tokens(f["content"])
        if current and (
            len(current) >= MAX_FILES_PER_BATCH
            or current_tokens + tokens > MAX_TOKENS_PER_BATCH
        ):
            batches.append(current)
            current, current_tokens = [], 0
        current.append(f)
        current_tokens += tokens

    if current:
        batches.append(current)

    return batches


def _call_gemini_batch(files):
    """
    Single Gemini call for a batch of files. Returns a parsed, validated
    JSON list, or raises — caller decides whether to retry/bisect.
    """
    files_block = "\n\n".join(
        f"--- FILE: {f['path']} ---\n{f['content']}" for f in files
    )
    prompt = _BATCH_PROMPT_TEMPLATE.format(file_count=len(files), files_block=files_block)

    response = _model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(response_mime_type="application/json"),
    )
    raw = response.text.strip()

    # Defensive cleanup — some SDK/model combos still wrap output in fences
    # occasionally even with response_mime_type set.
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    parsed = json.loads(raw)  # let this raise on malformed JSON — caller handles it

    if not isinstance(parsed, list) or len(parsed) != len(files):
        got = len(parsed) if isinstance(parsed, list) else "non-list"
        raise ValueError(f"Batch size mismatch: sent {len(files)} files, got {got} results")

    required_keys = {"path", "purpose", "responsibilities", "concepts", "keywords"}
    for item in parsed:
        if not required_keys.issubset(item.keys()):
            raise ValueError(f"Malformed metadata object, missing keys: {item}")

    return parsed


def _with_retry(fn, *args, **kwargs):
    """Exponential backoff + jitter. Retries on rate limits, transient errors, or bad output."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_error = e
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"  [retry {attempt + 1}/{MAX_RETRIES}] {e} — waiting {wait:.1f}s")
            time.sleep(wait)
    raise last_error


def _generate_for_batch(files, on_result=None):
    
    if len(files) == 1:
        f = files[0]
        try:
            metadata = _with_retry(llm_metadata_generator.generate_llm_metadata, f["content"])
        except Exception as e:
            print(f"  [failed] {f['path']}: {e}")
            metadata = None
        if on_result:
            on_result(f["path"], metadata)
        return {f["path"]: metadata}

    try:
        results = _with_retry(_call_gemini_batch, files)
        time.sleep(BATCH_DELAY_SECONDS)
        out = {}
        for item, f in zip(results, files):
            metadata = {
                "purpose": item.get("purpose", ""),
                "responsibilities": item.get("responsibilities", []),
                "concepts": item.get("concepts", []),
                "keywords": item.get("keywords", []),
            }
            out[f["path"]] = metadata
            if on_result:
                on_result(f["path"], metadata)
        return out
    except Exception as e:
        print(f"  [batch of {len(files)} failed after retries: {e} — bisecting]")
        mid = len(files) // 2
        left = _generate_for_batch(files[:mid], on_result=on_result)
        right = _generate_for_batch(files[mid:], on_result=on_result)
        return {**left, **right}


def generate_metadata_for_files(files, on_result=None):
    """
    Public entry point. `files` = list of {"path", "content"} dicts
    (already-filtered cache misses). Returns {path: metadata_dict}.

    Pass on_result to get a callback the moment each file's metadata is
    ready — this is what makes a run resumable: a crash or exhausted
    quota mid-run only loses the files not yet completed.
    """
    all_results = {}
    for batch in build_batches(files):
        all_results.update(_generate_for_batch(batch, on_result=on_result))
    return all_results
