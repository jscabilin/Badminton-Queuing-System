from __future__ import annotations

import os
import urllib.request
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="Badminton Queue & Fair-Play System", version="0.1.0")


def _supabase_config() -> dict[str, str]:
    return {
        "url": os.getenv("SUPABASE_URL", "").strip(),
        "key": os.getenv("SUPABASE_KEY", "").strip(),
    }


def _project_base_url(raw_url: str) -> str:
    url = raw_url.rstrip("/")
    if url.endswith("/rest/v1"):
        url = url[: -len("/rest/v1")]
    return url


def test_supabase_connection() -> dict[str, Any]:
    config = _supabase_config()
    if not config["url"] or not config["key"]:
        return {"ok": False, "message": "SUPABASE_URL or SUPABASE_KEY is missing"}

    base_url = _project_base_url(config["url"])
    request = urllib.request.Request(
        f"{base_url}/auth/v1/health",
        headers={"apikey": config["key"]},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return {
                "ok": True,
                "status_code": response.status,
                "message": "Reached the Supabase auth service",
            }
    except Exception as exc:
        return {"ok": False, "message": str(exc)}


@app.on_event("startup")
def startup_log() -> None:
    print("Backend started. Visit /docs to explore the API.")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Badminton Queue & Fair-Play System API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/backend-test")
def backend_test() -> dict[str, Any]:
    return {"status": "running", "supabase": test_supabase_connection()}
