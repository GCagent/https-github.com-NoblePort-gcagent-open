#!/bin/bash
# Update script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

APP_DIR="/var/www/video-uploader"
VENV_DIR="$APP_DIR/venv"

echo "=========================================="
echo "  Updating Video Uploader Application"
echo "=========================================="

cd $APP_DIR

# Pull latest code
echo "Pulling latest changes..."
git pull

# Update dependencies
echo "Updating Python dependencies..."
$VENV_DIR/bin/pip install --upgrade -r requirements.txt

# Restart services
echo "Restarting services..."
sudo systemctl restart video-uploader.service

echo ""
echo "Update complete!"
echo "Check status: systemctl status video-uploader.service"
