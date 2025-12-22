#!/bin/bash
# Docker deployment script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

echo "=========================================="
echo "  Docker Deployment - Video Uploader"
echo "  NoblePort Systems"
echo "=========================================="

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials before continuing!"
    echo "   Press Enter when ready..."
    read
fi

# Check for client_secret.json
if [ ! -f "client_secret.json" ]; then
    echo "⚠️  Warning: client_secret.json not found"
    echo "   YouTube uploads will not work without this file"
    echo "   Download from Google Cloud Console"
    echo ""
fi

# Build and start containers
echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting containers..."
docker-compose up -d

echo ""
echo "Waiting for services to start..."
sleep 10

# Check container status
echo ""
echo "Container Status:"
docker-compose ps

# Show logs
echo ""
echo "Recent logs:"
docker-compose logs --tail=20

echo ""
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
echo ""
echo "Services:"
echo "  - Application: http://localhost:5000"
echo "  - IPFS API: http://localhost:5001"
echo "  - IPFS Gateway: http://localhost:8080"
echo "  - Nginx: http://localhost:80"
echo ""
echo "Commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop: docker-compose stop"
echo "  - Restart: docker-compose restart"
echo "  - Shell: docker-compose exec video-uploader bash"
echo "  - CLI: docker-compose exec video-uploader python cli.py --help"
echo ""
echo "=========================================="
