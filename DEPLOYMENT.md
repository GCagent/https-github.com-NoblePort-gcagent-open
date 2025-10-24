# Deployment Guide - Dual-Platform Video Uploader

**NoblePort Systems - Production Deployment**

This guide covers deploying the Dual-Platform Video Uploader application to production environments using multiple methods.

## Table of Contents

1. [Deployment Methods](#deployment-methods)
2. [Docker Deployment](#docker-deployment)
3. [Traditional Linux Deployment](#traditional-linux-deployment)
4. [Configuration](#configuration)
5. [SSL/HTTPS Setup](#sslhttps-setup)
6. [Monitoring](#monitoring)
7. [Maintenance](#maintenance)
8. [Troubleshooting](#troubleshooting)

## Deployment Methods

### Available Methods

1. **Docker (Recommended)** - Containerized deployment with Docker Compose
2. **Systemd** - Traditional Linux service deployment
3. **Manual** - Direct Python/Gunicorn deployment

## Docker Deployment

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 20GB disk space

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/NoblePort/gcagent-open.git
cd gcagent-open

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with your credentials

# 3. Add YouTube credentials (if using YouTube)
# Place client_secret.json in project root

# 4. Deploy
chmod +x deployment/docker-deploy.sh
./deployment/docker-deploy.sh
```

### Manual Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Commands

```bash
# Restart application
docker-compose restart video-uploader

# Shell access
docker-compose exec video-uploader bash

# Run CLI commands
docker-compose exec video-uploader python cli.py compare

# View application logs
docker-compose logs -f video-uploader

# View IPFS logs
docker-compose logs -f video-uploader | grep -i ipfs

# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d
```

### Docker Compose Configuration

The `docker-compose.yml` includes:

- **video-uploader**: Main application container
  - Flask app on port 5000
  - IPFS daemon on ports 5001 (API) and 8080 (Gateway)
  - Auto-restart enabled
  - Health checks configured

- **nginx**: Reverse proxy
  - HTTP on port 80
  - HTTPS on port 443 (when configured)
  - Rate limiting
  - SSL termination

## Traditional Linux Deployment

### Prerequisites

- Ubuntu 20.04+ or Debian 11+
- Python 3.8+
- Nginx
- Systemd
- Root access

### Automated Deployment

```bash
# Run deployment script as root
sudo bash deployment/deploy.sh
```

This script will:
1. Install system dependencies
2. Install IPFS
3. Set up application in `/var/www/video-uploader`
4. Create Python virtual environment
5. Configure systemd services
6. Set up Nginx reverse proxy
7. Start all services

### Manual Deployment Steps

#### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    git \
    curl \
    wget
```

#### 2. Install IPFS

```bash
wget https://dist.ipfs.io/kubo/v0.17.0/kubo_v0.17.0_linux-amd64.tar.gz
tar -xzf kubo_v0.17.0_linux-amd64.tar.gz
cd kubo
sudo bash install.sh
```

#### 3. Set Up Application

```bash
# Create app directory
sudo mkdir -p /var/www/video-uploader
cd /var/www/video-uploader

# Clone repository
sudo git clone https://github.com/NoblePort/gcagent-open.git .

# Create virtual environment
sudo python3 -m venv venv

# Install dependencies
sudo venv/bin/pip install -r requirements-prod.txt

# Create uploads directory
sudo mkdir -p uploads

# Set permissions
sudo chown -R www-data:www-data /var/www/video-uploader
```

#### 4. Configure Environment

```bash
sudo cp .env.example .env
sudo nano .env  # Edit with your settings
sudo chown www-data:www-data .env
sudo chmod 600 .env
```

#### 5. Initialize IPFS

```bash
sudo -u www-data IPFS_PATH=/var/www/video-uploader/.ipfs ipfs init
sudo -u www-data IPFS_PATH=/var/www/video-uploader/.ipfs \
    ipfs config Addresses.API /ip4/127.0.0.1/tcp/5001
```

#### 6. Set Up Systemd Services

```bash
# Copy service files
sudo cp deployment/ipfs.service /etc/systemd/system/
sudo cp deployment/video-uploader.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable ipfs.service
sudo systemctl start ipfs.service

sudo systemctl enable video-uploader.service
sudo systemctl start video-uploader.service
```

#### 7. Configure Nginx

```bash
# Copy Nginx config
sudo cp deployment/nginx.conf /etc/nginx/sites-available/video-uploader

# Enable site
sudo ln -s /etc/nginx/sites-available/video-uploader \
    /etc/nginx/sites-enabled/video-uploader

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## Configuration

### Environment Variables

Edit `.env` file with your configuration:

```env
# Flask settings
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# YouTube API (optional)
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=

# DTube (optional)
DTUBE_USERNAME=your-username
DTUBE_PRIVATE_KEY=your-private-key

# IPFS
IPFS_HOST=127.0.0.1
IPFS_PORT=5001

# Application
UPLOAD_FOLDER=/var/www/video-uploader/uploads
MAX_FILE_SIZE=5368709120
```

### Gunicorn Configuration

Edit `gunicorn.conf.py` for production tuning:

```python
# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Worker timeout (increase for large uploads)
timeout = 600

# Maximum requests per worker
max_requests = 1000
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### Manual SSL Certificate

```bash
# Create SSL directory
sudo mkdir -p /etc/nginx/ssl

# Copy your certificates
sudo cp your-cert.pem /etc/nginx/ssl/cert.pem
sudo cp your-key.pem /etc/nginx/ssl/key.pem

# Set permissions
sudo chmod 600 /etc/nginx/ssl/key.pem
```

Update Nginx configuration to enable HTTPS (uncomment SSL section in `deployment/nginx.conf`).

## Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:5000/health

# IPFS health
curl http://localhost:5001/api/v0/id

# Nginx status
curl http://localhost/health
```

### Service Status

```bash
# Check all services
sudo systemctl status video-uploader.service
sudo systemctl status ipfs.service
sudo systemctl status nginx

# View logs
sudo journalctl -u video-uploader.service -f
sudo journalctl -u ipfs.service -f
```

### Log Locations

- **Application**: `journalctl -u video-uploader.service`
- **IPFS**: `journalctl -u ipfs.service`
- **Nginx**: `/var/log/nginx/video-uploader-*.log`
- **Docker**: `docker-compose logs`

### Monitoring Script

Create a monitoring script:

```bash
#!/bin/bash
# /usr/local/bin/monitor-video-uploader.sh

# Check application
if ! curl -sf http://localhost:5000/health > /dev/null; then
    echo "Application is down!"
    sudo systemctl restart video-uploader.service
fi

# Check IPFS
if ! curl -sf http://localhost:5001/api/v0/id > /dev/null; then
    echo "IPFS is down!"
    sudo systemctl restart ipfs.service
fi
```

Add to cron:
```bash
*/5 * * * * /usr/local/bin/monitor-video-uploader.sh
```

## Maintenance

### Updates

```bash
# Using update script
cd /var/www/video-uploader
sudo ./deployment/update.sh

# Manual update
sudo -u www-data git pull
sudo venv/bin/pip install --upgrade -r requirements-prod.txt
sudo systemctl restart video-uploader.service
```

### Backups

```bash
# Create backup
sudo ./deployment/backup.sh

# Backups are stored in: /var/backups/video-uploader/
```

### Rollback

```bash
# List recent commits
cd /var/www/video-uploader
git log --oneline -10

# Rollback to specific commit
sudo ./deployment/rollback.sh <commit-hash>
```

### Database Maintenance (if applicable)

```bash
# Clear old upload files
find /var/www/video-uploader/uploads -type f -mtime +7 -delete

# Clean IPFS cache
sudo -u www-data IPFS_PATH=/var/www/video-uploader/.ipfs ipfs repo gc
```

## Scaling

### Horizontal Scaling

For high-traffic deployments:

1. **Load Balancer**: Use Nginx or HAProxy
2. **Multiple App Servers**: Deploy app on multiple servers
3. **Shared Storage**: Use NFS or S3 for uploads
4. **Redis**: For session management and caching

### Vertical Scaling

Increase resources:

```python
# gunicorn.conf.py
workers = 8  # Increase for more CPU cores
worker_connections = 2000
timeout = 600  # For large uploads
```

## Security Checklist

- [ ] Change default `FLASK_SECRET_KEY`
- [ ] Configure firewall (ufw/iptables)
- [ ] Enable HTTPS/SSL
- [ ] Set up fail2ban
- [ ] Regular security updates
- [ ] Secure API credentials
- [ ] Configure rate limiting
- [ ] Set file upload limits
- [ ] Enable Nginx security headers
- [ ] Restrict IPFS API access

### Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

# Block IPFS ports from external access
# (keep accessible only locally)
sudo ufw enable
```

## Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u video-uploader.service -n 50

# Check configuration
source /var/www/video-uploader/venv/bin/activate
cd /var/www/video-uploader
python -c "from app import app; print('OK')"

# Check permissions
ls -la /var/www/video-uploader/
```

### IPFS Issues

```bash
# Check IPFS status
sudo systemctl status ipfs.service

# Test IPFS
sudo -u www-data IPFS_PATH=/var/www/video-uploader/.ipfs ipfs id

# Reset IPFS (WARNING: loses data)
sudo systemctl stop ipfs.service
sudo rm -rf /var/www/video-uploader/.ipfs
sudo -u www-data ipfs init
sudo systemctl start ipfs.service
```

### Upload Failures

```bash
# Check disk space
df -h

# Check upload directory permissions
ls -la /var/www/video-uploader/uploads/

# Check file size limits
grep -i "client_max_body_size" /etc/nginx/sites-available/video-uploader
```

### High Memory Usage

```bash
# Check memory
free -h

# Restart services
sudo systemctl restart video-uploader.service

# Reduce workers
# Edit gunicorn.conf.py: workers = 2
```

## Performance Tuning

### Nginx

```nginx
# /etc/nginx/nginx.conf
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
}
```

### Gunicorn

```python
# gunicorn.conf.py
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 2000
max_requests = 1000
max_requests_jitter = 50
```

### System Limits

```bash
# /etc/security/limits.conf
www-data soft nofile 65536
www-data hard nofile 65536
```

## Support

For deployment issues:

- Check logs first: `journalctl -u video-uploader.service -f`
- Review this documentation
- Check GitHub issues
- Contact NoblePort Systems

---

**NoblePort Systems - Professional Video Uploader Deployment**
