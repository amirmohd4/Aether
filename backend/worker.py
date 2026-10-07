import os
import threading
import time

try:
    from backend.aether_core.worker_runtime import AetherWorkerRuntime
except ModuleNotFoundError:
    from aether_core.worker_runtime import AetherWorkerRuntime


def run_background_worker() -> None:
    """Keep the durable worker loop alive alongside the web process."""
    runtime = AetherWorkerRuntime()
    interval = int(os.getenv("AETHER_WORKER_INTERVAL_SECONDS", "5"))

    while True:
        try:
            runtime.run_once()
        except Exception as exc:
            print(f"[Aether Worker] tick failed: {exc}", flush=True)
        time.sleep(max(1, interval))


def run_worker_only() -> None:
    interval = int(os.getenv("AETHER_WORKER_INTERVAL_SECONDS", "5"))
    AetherWorkerRuntime().run_forever(interval)


if __name__ == "__main__":
    if os.getenv("AETHER_EMBED_WORKER", "false").lower() == "true":
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
