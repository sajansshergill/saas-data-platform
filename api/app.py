from __future__ import annotations

import os
import subprocess
import threading
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from pipelines.db import get_engine


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
PIPELINE_LOG = LOG_DIR / "pipeline.log"

_lock = threading.Lock()
_proc: subprocess.Popen[str] | None = None


def _run_pipeline() -> None:
    """Run scripts/run_all.py and stream logs to a file."""
    global _proc
    with _lock:
        if _proc and _proc.poll() is None:
            return

        PIPELINE_LOG.write_text("")
        env = os.environ.copy()
        _proc = subprocess.Popen(
            ["python", "scripts/run_all.py"],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
        )

    assert _proc.stdout is not None
    with PIPELINE_LOG.open("a") as f:
        for line in _proc.stdout:
            f.write(line)


app = FastAPI(title="SaaS Data Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "time": int(time.time())}


@app.post("/pipeline/run")
def pipeline_run() -> dict:
    with _lock:
        if _proc and _proc.poll() is None:
            return {"status": "running"}

    t = threading.Thread(target=_run_pipeline, daemon=True)
    t.start()
    return {"status": "started"}


@app.get("/pipeline/status")
def pipeline_status() -> dict:
    with _lock:
        if not _proc:
            return {"status": "idle"}
        code = _proc.poll()
        if code is None:
            return {"status": "running"}
        return {"status": "succeeded" if code == 0 else "failed", "exit_code": code}


@app.get("/pipeline/logs")
def pipeline_logs(lines: int = 200) -> dict:
    if lines < 1 or lines > 2000:
        raise HTTPException(status_code=400, detail="lines must be 1..2000")
    if not PIPELINE_LOG.exists():
        return {"lines": []}

    text_content = PIPELINE_LOG.read_text(errors="replace")
    all_lines = text_content.splitlines()
    return {"lines": all_lines[-lines:]}


@app.get("/metrics/summary")
def metrics_summary() -> dict:
    """Simple KPI snapshot backed by Postgres."""
    engine = get_engine()
    with engine.connect() as conn:
        total_customers = conn.scalar(text("select count(*) from customers"))
        total_subscriptions = conn.scalar(text("select count(*) from subscriptions"))
        active_subscriptions = conn.scalar(
            text("select count(*) from subscriptions where status = 'active'")
        )
        current_mrr = conn.scalar(
            text(
                """
                select coalesce(sum(monthly_amount), 0)
                from subscriptions
                where status = 'active'
                """
            )
        )
    return {
        "total_customers": int(total_customers or 0),
        "total_subscriptions": int(total_subscriptions or 0),
        "active_subscriptions": int(active_subscriptions or 0),
        "current_mrr": float(current_mrr or 0.0),
    }


@app.get("/metrics/mrr")
def metrics_mrr() -> dict:
    """
    Monthly recurring revenue over time.

    Backed by the dbt `mrr` model:
      revenue_month (date), mrr (numeric)
    """
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text("select revenue_month, mrr from mrr order by revenue_month")
        ).mappings()
        data = [
            {
                "revenue_month": str(row["revenue_month"]),
                "mrr": float(row["mrr"] or 0.0),
            }
            for row in rows
        ]
    return {"points": data}

