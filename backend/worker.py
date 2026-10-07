import os
import sys
import threading
import time
from pathlib import Path

# When executed as "python backend/worker.py", Python puts /app/backend on
# sys.path but not the repository root. Add the root so backend.* imports
# resolve consistently in Render and local container execution.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[1])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

# Import through the backend package so the web app and worker share the same
# Python module namespace and SQLAlchemy metadata.
from backend.aether_core.worker_runtime import AetherWorkerRuntime


def run_background_worker() -> None:
    """Run durable case/notification work beside the web process."""
    runtime = AetherWorkerRuntime()
    interval = max(1, int(os.getenv("AETHER_WORKER_INTERVAL_SECONDS", "5")))
    startup_delay = max(0, int(os.getenv("AETHER_WORKER_STARTUP_DELAY_SECONDS", "8")))

    if startup_delay:
        time.sleep(startup_delay)

    while True:
        try:
            result = runtime.run_once()
            print(
                "[Aether Worker] tick "
                f"processed={result.get('count', 0)} "
                f"notifications={result.get('notifications', {})}",
                flush=True,
            )
        except Exception as exc:
            # Never take the web API down because the worker backend is unavailable.
            print(f"[Aether Worker] tick failed: {exc}", flush=True)
        time.sleep(interval)


def run_worker_only() -> None:
    interval = max(1, int(os.getenv("AETHER_WORKER_INTERVAL_SECONDS", "5")))
    AetherWorkerRuntime().run_forever(interval)


if __name__ == "__main__":
    if os.getenv("AETHER_EMBED_WORKER", "false").strip().lower() == "true":
        import uvicorn

        worker_thread = threading.Thread(
            target=run_background_worker,
            name="aether-worker",
            daemon=True,
        )
        worker_thread.start()

        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", "8081")),
        )
    else:
        run_worker_only()
