#!/bin/bash
# Docker entrypoint script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

echo "=========================================="
echo "  Starting Dual-Platform Video Uploader"
echo "  NoblePort Systems"
echo "=========================================="

# Start IPFS daemon in background
echo "Starting IPFS daemon..."
ipfs daemon &
IPFS_PID=$!

# Wait for IPFS to be ready
echo "Waiting for IPFS to be ready..."
sleep 5

# Check IPFS status
if ipfs id > /dev/null 2>&1; then
    echo "✓ IPFS daemon started successfully"
    IPFS_ID=$(ipfs id -f='<id>')
    echo "  IPFS Peer ID: $IPFS_ID"
else
    echo "⚠ Warning: IPFS daemon may not be ready"
fi

# Create uploads directory
mkdir -p /app/uploads

echo ""
echo "Application configuration:"
echo "  Upload folder: ${UPLOAD_FOLDER:-/app/uploads}"
echo "  Max file size: ${MAX_FILE_SIZE:-5368709120} bytes"
echo "  IPFS API: ${IPFS_HOST:-127.0.0.1}:${IPFS_PORT:-5001}"
echo ""

# Determine command
CMD=${1:-gunicorn}

if [ "$CMD" = "gunicorn" ]; then
    echo "Starting Gunicorn WSGI server..."
    exec gunicorn \
        --bind 0.0.0.0:5000 \
        --workers 4 \
        --worker-class gevent \
        --timeout 300 \
        --keep-alive 5 \
        --log-level info \
        --access-logfile - \
        --error-logfile - \
        app:app
elif [ "$CMD" = "flask" ]; then
    echo "Starting Flask development server..."
    exec python app.py
elif [ "$CMD" = "cli" ]; then
    shift
    echo "Running CLI command..."
    exec python cli.py "$@"
else
    echo "Running custom command: $@"
    exec "$@"
fi
