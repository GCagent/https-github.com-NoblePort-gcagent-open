#!/bin/bash
# Health check script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

APP_URL="http://localhost:5000"
IPFS_URL="http://localhost:5001"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_ok() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_fail() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

echo "=========================================="
echo "  Health Check - Video Uploader"
echo "=========================================="
echo ""

# Check Application
echo "Checking Application..."
if curl -sf "$APP_URL/health" > /dev/null 2>&1; then
    RESPONSE=$(curl -s "$APP_URL/health")
    print_ok "Application is healthy"
    echo "    $RESPONSE"
else
    print_fail "Application is not responding"
    EXIT_CODE=1
fi

echo ""

# Check IPFS
echo "Checking IPFS..."
if curl -sf "$IPFS_URL/api/v0/id" > /dev/null 2>&1; then
    IPFS_ID=$(curl -s "$IPFS_URL/api/v0/id" | grep -o '"ID":"[^"]*"' | cut -d'"' -f4)
    print_ok "IPFS daemon is running"
    echo "    Peer ID: $IPFS_ID"
else
    print_fail "IPFS daemon is not responding"
    EXIT_CODE=1
fi

echo ""

# Check Services (if systemd)
if command -v systemctl &> /dev/null; then
    echo "Checking Services..."

    if systemctl is-active --quiet video-uploader.service; then
        print_ok "video-uploader.service is active"
    else
        print_fail "video-uploader.service is not active"
        EXIT_CODE=1
    fi

    if systemctl is-active --quiet ipfs.service; then
        print_ok "ipfs.service is active"
    else
        print_fail "ipfs.service is not active"
        EXIT_CODE=1
    fi

    if systemctl is-active --quiet nginx.service; then
        print_ok "nginx.service is active"
    else
        print_warn "nginx.service is not active"
    fi

    echo ""
fi

# Check Docker (if docker-compose)
if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
    echo "Checking Docker Containers..."

    CONTAINER_STATUS=$(docker-compose ps -q video-uploader | xargs docker inspect -f '{{.State.Status}}' 2>/dev/null || echo "not found")

    if [ "$CONTAINER_STATUS" = "running" ]; then
        print_ok "video-uploader container is running"
    else
        print_fail "video-uploader container status: $CONTAINER_STATUS"
        EXIT_CODE=1
    fi

    echo ""
fi

# Check Disk Space
echo "Checking Disk Space..."
UPLOAD_DIR="/var/www/video-uploader/uploads"
if [ -d "$UPLOAD_DIR" ]; then
    DISK_USAGE=$(df -h "$UPLOAD_DIR" | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -lt 80 ]; then
        print_ok "Disk usage: ${DISK_USAGE}%"
    elif [ "$DISK_USAGE" -lt 90 ]; then
        print_warn "Disk usage: ${DISK_USAGE}% (getting high)"
    else
        print_fail "Disk usage: ${DISK_USAGE}% (critical)"
        EXIT_CODE=1
    fi
fi

echo ""

# Check Memory
echo "Checking Memory..."
MEM_AVAILABLE=$(free -m | awk 'NR==2 {print $7}')
if [ "$MEM_AVAILABLE" -gt 500 ]; then
    print_ok "Available memory: ${MEM_AVAILABLE}MB"
else
    print_warn "Available memory: ${MEM_AVAILABLE}MB (low)"
fi

echo ""

# Summary
echo "=========================================="
if [ -z "$EXIT_CODE" ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some checks failed!${NC}"
    exit 1
fi
