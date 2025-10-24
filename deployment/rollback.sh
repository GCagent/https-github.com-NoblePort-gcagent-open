#!/bin/bash
# Rollback script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

APP_DIR="/var/www/video-uploader"
VENV_DIR="$APP_DIR/venv"

if [ -z "$1" ]; then
    echo "Usage: $0 <commit-hash>"
    echo ""
    echo "Recent commits:"
    cd $APP_DIR
    git log --oneline -10
    exit 1
fi

COMMIT=$1

echo "=========================================="
echo "  Rolling back to commit: $COMMIT"
echo "=========================================="

cd $APP_DIR

# Backup current state
BACKUP_BRANCH="backup-$(date +%Y%m%d-%H%M%S)"
git branch $BACKUP_BRANCH

echo "Created backup branch: $BACKUP_BRANCH"

# Checkout commit
git checkout $COMMIT

# Update dependencies
echo "Updating Python dependencies..."
$VENV_DIR/bin/pip install --upgrade -r requirements.txt

# Restart services
echo "Restarting services..."
sudo systemctl restart video-uploader.service

echo ""
echo "Rollback complete!"
echo "To restore: git checkout main"
echo "Check status: systemctl status video-uploader.service"
