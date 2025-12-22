#!/bin/bash
# Deployment script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

echo "=========================================="
echo "  Dual-Platform Video Uploader"
echo "  Deployment Script - NoblePort Systems"
echo "=========================================="
echo ""

# Configuration
APP_DIR="/var/www/video-uploader"
APP_USER="www-data"
APP_GROUP="www-data"
VENV_DIR="$APP_DIR/venv"
REPO_URL="https://github.com/NoblePort/gcagent-open.git"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "Please run as root or with sudo"
        exit 1
    fi
}

install_dependencies() {
    print_status "Installing system dependencies..."
    apt-get update
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        nginx \
        git \
        curl \
        wget \
        ca-certificates
    print_status "System dependencies installed"
}

install_ipfs() {
    if command -v ipfs &> /dev/null; then
        print_status "IPFS already installed"
        return
    fi

    print_status "Installing IPFS..."
    cd /tmp
    wget -q https://dist.ipfs.io/kubo/v0.17.0/kubo_v0.17.0_linux-amd64.tar.gz
    tar -xzf kubo_v0.17.0_linux-amd64.tar.gz
    cd kubo
    bash install.sh
    cd ..
    rm -rf kubo kubo_v0.17.0_linux-amd64.tar.gz
    print_status "IPFS installed"
}

setup_application() {
    print_status "Setting up application..."

    # Create app directory
    mkdir -p $APP_DIR
    cd $APP_DIR

    # Clone or update repository
    if [ -d "$APP_DIR/.git" ]; then
        print_status "Updating repository..."
        git pull
    else
        print_status "Cloning repository..."
        git clone $REPO_URL .
    fi

    # Create virtual environment
    print_status "Creating virtual environment..."
    python3 -m venv $VENV_DIR

    # Install Python dependencies
    print_status "Installing Python dependencies..."
    $VENV_DIR/bin/pip install --upgrade pip
    $VENV_DIR/bin/pip install -r requirements.txt
    $VENV_DIR/bin/pip install gunicorn gevent

    # Create uploads directory
    mkdir -p $APP_DIR/uploads

    # Set permissions
    chown -R $APP_USER:$APP_GROUP $APP_DIR
    chmod -R 755 $APP_DIR
    chmod 770 $APP_DIR/uploads

    print_status "Application setup complete"
}

setup_ipfs_user() {
    print_status "Setting up IPFS for $APP_USER..."

    # Initialize IPFS as app user
    sudo -u $APP_USER IPFS_PATH=$APP_DIR/.ipfs ipfs init || true

    # Configure IPFS
    sudo -u $APP_USER IPFS_PATH=$APP_DIR/.ipfs ipfs config Addresses.API /ip4/127.0.0.1/tcp/5001

    print_status "IPFS configured"
}

setup_systemd() {
    print_status "Setting up systemd services..."

    # Copy service files
    cp $APP_DIR/deployment/ipfs.service /etc/systemd/system/
    cp $APP_DIR/deployment/video-uploader.service /etc/systemd/system/

    # Reload systemd
    systemctl daemon-reload

    # Enable services
    systemctl enable ipfs.service
    systemctl enable video-uploader.service

    print_status "Systemd services configured"
}

setup_nginx() {
    print_status "Setting up Nginx..."

    # Backup existing config if any
    if [ -f /etc/nginx/sites-available/video-uploader ]; then
        cp /etc/nginx/sites-available/video-uploader /etc/nginx/sites-available/video-uploader.backup
    fi

    # Copy Nginx config
    cp $APP_DIR/deployment/nginx.conf /etc/nginx/sites-available/video-uploader

    # Enable site
    ln -sf /etc/nginx/sites-available/video-uploader /etc/nginx/sites-enabled/video-uploader

    # Remove default site if exists
    rm -f /etc/nginx/sites-enabled/default

    # Test Nginx config
    nginx -t

    print_status "Nginx configured"
}

setup_env() {
    if [ ! -f "$APP_DIR/.env" ]; then
        print_warning "Creating .env file from example..."
        cp $APP_DIR/.env.example $APP_DIR/.env
        chown $APP_USER:$APP_GROUP $APP_DIR/.env
        chmod 600 $APP_DIR/.env
        print_warning "Please edit $APP_DIR/.env with your credentials!"
    else
        print_status ".env file already exists"
    fi
}

start_services() {
    print_status "Starting services..."

    # Start IPFS
    systemctl restart ipfs.service
    sleep 3

    # Start application
    systemctl restart video-uploader.service
    sleep 2

    # Restart Nginx
    systemctl restart nginx

    print_status "Services started"
}

show_status() {
    echo ""
    echo "=========================================="
    echo "  Service Status"
    echo "=========================================="
    systemctl status ipfs.service --no-pager -l || true
    echo ""
    systemctl status video-uploader.service --no-pager -l || true
    echo ""
    systemctl status nginx --no-pager -l || true
    echo ""
}

show_summary() {
    echo ""
    echo "=========================================="
    echo "  Deployment Complete!"
    echo "=========================================="
    echo ""
    echo "Application Directory: $APP_DIR"
    echo "Configuration File: $APP_DIR/.env"
    echo ""
    echo "Services:"
    echo "  - IPFS Daemon: systemctl status ipfs.service"
    echo "  - Video Uploader: systemctl status video-uploader.service"
    echo "  - Nginx: systemctl status nginx"
    echo ""
    echo "Commands:"
    echo "  - View logs: journalctl -u video-uploader.service -f"
    echo "  - Restart app: systemctl restart video-uploader.service"
    echo "  - CLI tool: cd $APP_DIR && $VENV_DIR/bin/python cli.py --help"
    echo ""
    echo "Next steps:"
    echo "  1. Edit $APP_DIR/.env with your credentials"
    echo "  2. Add client_secret.json to $APP_DIR/ for YouTube"
    echo "  3. Restart: systemctl restart video-uploader.service"
    echo "  4. Access at: http://your-server-ip/"
    echo ""
    echo "=========================================="
}

# Main deployment process
main() {
    check_root
    install_dependencies
    install_ipfs
    setup_application
    setup_ipfs_user
    setup_env
    setup_systemd
    setup_nginx
    start_services
    show_status
    show_summary
}

# Run deployment
main
