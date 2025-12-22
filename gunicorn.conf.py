"""
Gunicorn configuration for production deployment
NoblePort Systems - Dual-Platform Video Uploader
"""
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 1000
timeout = 300
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'video-uploader'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment when using HTTPS)
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'

# Reload on code changes (disable in production)
reload = False

# Maximum requests per worker (helps prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Worker timeout
graceful_timeout = 30
