import os

from aether_core.worker_runtime import AetherWorkerRuntime


if __name__ == "__main__":
    interval = int(os.getenv("AETHER_WORKER_INTERVAL_SECONDS", "5"))
    AetherWorkerRuntime().run_forever(interval)
