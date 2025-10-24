#!/bin/bash
# Quick Start Script for Dual-Platform Video Uploader
# NoblePort Systems

set -e

echo "=========================================="
echo "  Dual-Platform Video Uploader"
echo "  NoblePort Systems - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your credentials!"
fi

# Create uploads directory
mkdir -p uploads

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. For YouTube uploads:"
echo "   - Download client_secret.json from Google Cloud Console"
echo "   - Place it in this directory"
echo ""
echo "2. For DTube uploads:"
echo "   - Install IPFS: https://docs.ipfs.io/install/"
echo "   - Run: ipfs init"
echo "   - Run: ipfs daemon"
echo ""
echo "3. Start the web application:"
echo "   python app.py"
echo ""
echo "4. Or use the CLI:"
echo "   python cli.py --help"
echo ""
echo "For detailed setup instructions, see SETUP_GUIDE.md"
echo ""
echo "=========================================="
