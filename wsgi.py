"""
WSGI entry point for production deployment
NoblePort Systems - Dual-Platform Video Uploader
"""
from app import app

if __name__ == "__main__":
    app.run()
