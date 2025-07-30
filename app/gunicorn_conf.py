import os
import multiprocessing

bind = "0.0.0.0:8000"
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv("THREADS", "2"))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = int(os.getenv("TIMEOUT", "60"))
keepalive = int(os.getenv("KEEPALIVE", "15"))
accesslog = "-"
errorlog = "-"
preload_app = True
