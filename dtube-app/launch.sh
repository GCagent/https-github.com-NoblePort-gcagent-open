#!/bin/bash
# DTube Easy Connection App Launcher
# NoblePort Systems

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_banner() {
    echo "=========================================="
    echo "  DTube Easy Connection App"
    echo "  NoblePort Systems"
    echo "=========================================="
    echo ""
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: Python 3 is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Python 3 found${NC}"
}

check_ipfs() {
    if ! command -v ipfs &> /dev/null; then
        echo -e "${YELLOW}! IPFS not installed${NC}"
        echo ""
        echo "Install IPFS:"
        echo "  macOS: brew install ipfs"
        echo "  Linux: https://docs.ipfs.io/install/"
        echo ""
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo -e "${GREEN}✓ IPFS found${NC}"
    fi
}

check_ipfs_daemon() {
    if ipfs id &> /dev/null; then
        PEER_ID=$(ipfs id -f='<id>')
        echo -e "${GREEN}✓ IPFS daemon is running${NC}"
        echo "  Peer ID: ${PEER_ID:0:20}..."
    else
        echo -e "${YELLOW}! IPFS daemon is not running${NC}"
        echo ""
        echo "Starting IPFS daemon..."
        echo ""

        # Try to start IPFS daemon in background
        ipfs daemon &
        IPFS_PID=$!
        echo "  Started IPFS daemon (PID: $IPFS_PID)"
        echo "  Waiting for daemon to be ready..."
        sleep 5

        if ipfs id &> /dev/null; then
            echo -e "${GREEN}✓ IPFS daemon started successfully${NC}"
        else
            echo -e "${RED}✗ Failed to start IPFS daemon${NC}"
            echo "  Please start it manually: ipfs daemon"
            exit 1
        fi
    fi
}

install_dependencies() {
    if [ ! -d "venv" ]; then
        echo ""
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    echo ""
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
}

start_app() {
    echo ""
    echo "=========================================="
    echo "  Starting DTube App..."
    echo "=========================================="
    echo ""
    echo "Access the app at:"
    echo -e "  ${GREEN}http://localhost:5001${NC}"
    echo ""
    echo "Press Ctrl+C to stop"
    echo ""

    source venv/bin/activate
    python app.py
}

cleanup() {
    echo ""
    echo "Shutting down..."

    # Kill IPFS if we started it
    if [ ! -z "$IPFS_PID" ]; then
        kill $IPFS_PID 2>/dev/null || true
        echo "Stopped IPFS daemon"
    fi
}

trap cleanup EXIT

# Main execution
print_banner
check_python
check_ipfs
check_ipfs_daemon
install_dependencies
start_app
