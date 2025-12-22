#!/bin/bash
# Backup script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

APP_DIR="/var/www/video-uploader"
BACKUP_DIR="/var/backups/video-uploader"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="backup-$TIMESTAMP"

echo "=========================================="
echo "  Creating backup: $BACKUP_NAME"
echo "=========================================="

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application files
echo "Backing up application files..."
tar -czf "$BACKUP_DIR/$BACKUP_NAME-app.tar.gz" \
    -C $APP_DIR \
    --exclude='venv' \
    --exclude='uploads' \
    --exclude='__pycache__' \
    --exclude='.git' \
    .

# Backup .env file
echo "Backing up configuration..."
cp $APP_DIR/.env "$BACKUP_DIR/$BACKUP_NAME.env"

# Backup IPFS data (optional, can be large)
if [ -d "$APP_DIR/.ipfs" ]; then
    echo "Backing up IPFS data..."
    tar -czf "$BACKUP_DIR/$BACKUP_NAME-ipfs.tar.gz" \
        -C $APP_DIR \
        .ipfs
fi

# Backup database if exists (future use)
# mysqldump video_uploader > "$BACKUP_DIR/$BACKUP_NAME.sql"

# List backups
echo ""
echo "Backup created successfully!"
echo "Location: $BACKUP_DIR/$BACKUP_NAME-*"
echo ""
echo "Available backups:"
ls -lh $BACKUP_DIR/ | tail -5

# Keep only last 10 backups
echo ""
echo "Cleaning old backups (keeping last 10)..."
cd $BACKUP_DIR
ls -t | tail -n +31 | xargs -r rm --

echo "Backup complete!"
