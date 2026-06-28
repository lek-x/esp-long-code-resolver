import os

bind = "127.0.0.1:8001"
workers = int(os.getenv("WORKERS", "2"))
threads = int(os.getenv("THREADS", "2"))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = int(os.getenv("TIMEOUT", "60"))
keepalive = int(os.getenv("KEEPALIVE", "15"))
accesslog = "-"
errorlog = "-"
preload_app = True
