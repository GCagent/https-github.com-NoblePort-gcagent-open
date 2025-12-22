# Setup Guide - Dual-Platform Video Uploader

This guide will walk you through setting up the dual-platform video uploader for YouTube and DTube.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [YouTube Setup](#youtube-setup)
3. [DTube Setup](#dtube-setup)
4. [Application Setup](#application-setup)
5. [First Upload](#first-upload)

## System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space (more for video processing)
- **Internet**: Broadband connection for uploads

### Required Software
- Python 3.8+
- pip (Python package manager)
- IPFS (for DTube)
- Git (optional, for cloning repository)

## YouTube Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "New Project"
3. Enter project name (e.g., "Video Uploader")
4. Click "Create"

### Step 2: Enable YouTube Data API

1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and click "Enable"

### Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External" (unless you have Google Workspace)
3. Fill in required fields:
   - App name: "Video Uploader"
   - User support email: your email
   - Developer contact: your email
4. Click "Save and Continue"
5. On "Scopes" page, click "Add or Remove Scopes"
6. Search for YouTube and add:
   - `https://www.googleapis.com/auth/youtube.upload`
7. Click "Save and Continue"
8. Add test users (your Gmail address)
9. Click "Save and Continue"

### Step 4: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Desktop app"
4. Name it "Video Uploader Client"
5. Click "Create"
6. Click "Download JSON"
7. Save the file as `client_secret.json` in the project directory

### Step 5: Verify Setup

Your `client_secret.json` should look like this:
```json
{
  "installed": {
    "client_id": "xxxxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    ...
  }
}
```

## DTube Setup

### Step 1: Install IPFS

#### Linux/macOS
```bash
# Download IPFS
wget https://dist.ipfs.io/go-ipfs/v0.17.0/go-ipfs_v0.17.0_linux-amd64.tar.gz

# Extract
tar -xvzf go-ipfs_v0.17.0_linux-amd64.tar.gz

# Install
cd go-ipfs
sudo bash install.sh

# Verify
ipfs --version
```

#### Windows
1. Download from https://dist.ipfs.io/#go-ipfs
2. Extract to `C:\Program Files\ipfs`
3. Add to PATH
4. Open PowerShell and verify: `ipfs --version`

#### macOS (using Homebrew)
```bash
brew install ipfs
```

### Step 2: Initialize IPFS

```bash
# Initialize IPFS repository
ipfs init

# You should see output like:
# peer identity: QmXXXXXXXXXXXXXXXXXXX
# Save this peer ID!
```

### Step 3: Configure IPFS

```bash
# Set API to accept local connections
ipfs config Addresses.API /ip4/127.0.0.1/tcp/5001

# Optional: Increase storage limit
ipfs config Datastore.StorageMax 50GB
```

### Step 4: Start IPFS Daemon

```bash
# Start IPFS daemon
ipfs daemon

# You should see:
# Daemon is ready
```

**Keep this terminal open while using DTube uploads!**

### Step 5: Verify IPFS is Running

Open a new terminal:
```bash
# Check IPFS status
ipfs id

# Should show your peer ID and addresses
```

### Step 6: Get DTube Account (Optional)

1. Go to https://d.tube/
2. Create an account
3. Save your username and private key
4. Add to `.env` file (see below)

## Application Setup

### Step 1: Clone/Download Repository

```bash
# Clone with Git
git clone https://github.com/NoblePort/gcagent-open.git
cd gcagent-open

# Or download and extract ZIP
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# If you get errors, try:
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
nano .env  # or use your favorite editor
```

Edit `.env` with your settings:
```env
# YouTube - leave blank, OAuth will handle it
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=

# DTube - optional, only if you have account
DTUBE_PRIVATE_KEY=your_dtube_private_key
DTUBE_USERNAME=your_dtube_username

# IPFS - default settings usually work
IPFS_HOST=127.0.0.1
IPFS_PORT=5001

# App settings
FLASK_SECRET_KEY=change-this-to-random-string
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=5368709120
```

### Step 5: Create Uploads Directory

```bash
# Create directory for temporary uploads
mkdir -p uploads
```

### Step 6: Place YouTube Credentials

```bash
# Make sure client_secret.json is in project root
ls client_secret.json

# Should exist and be readable
```

## First Upload

### Test YouTube Upload (CLI)

1. Make sure IPFS daemon is running (if testing DTube)
2. Run the CLI:
   ```bash
   python cli.py upload \
     --platform youtube \
     --video test_video.mp4 \
     --title "Test Upload" \
     --description "Testing the uploader" \
     --privacy private
   ```
3. Browser will open for OAuth authentication
4. Sign in with Google account
5. Grant permissions to the app
6. Upload will begin

### Test DTube Upload (CLI)

```bash
# Make sure IPFS daemon is running!
ipfs daemon

# In another terminal:
python cli.py upload \
  --platform dtube \
  --video test_video.mp4 \
  --title "Test Upload" \
  --description "Testing the uploader"
```

### Test Web Interface

1. Start IPFS daemon:
   ```bash
   ipfs daemon
   ```

2. In another terminal, start the web app:
   ```bash
   python app.py
   ```

3. Open browser to: http://localhost:5000

4. Upload a video through the web interface

## Common Setup Issues

### Issue: "No module named 'google'"

**Solution**:
```bash
pip install --upgrade google-api-python-client google-auth-oauthlib
```

### Issue: "Cannot connect to IPFS"

**Solution**:
```bash
# Check if daemon is running
ps aux | grep ipfs

# If not running:
ipfs daemon

# Check API address
ipfs config Addresses.API
# Should be: /ip4/127.0.0.1/tcp/5001
```

### Issue: "YouTube OAuth fails"

**Solution**:
1. Delete `token.pickle` file
2. Verify `client_secret.json` is correct
3. Check OAuth consent screen is configured
4. Ensure YouTube Data API v3 is enabled

### Issue: "ModuleNotFoundError"

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "File too large"

**Solution**:
Edit `.env` and increase `MAX_FILE_SIZE`:
```env
MAX_FILE_SIZE=10737418240  # 10GB
```

## Next Steps

After successful setup:

1. **Read the README.md** for detailed usage instructions
2. **Review copyright policies** before uploading content
3. **Test with small videos** first
4. **Keep IPFS daemon running** for DTube uploads
5. **Monitor upload progress** in terminal or web interface

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section in README.md
2. Review error messages carefully
3. Check that all prerequisites are installed
4. Verify IPFS daemon is running (for DTube)
5. Ensure `client_secret.json` is correct (for YouTube)

## Security Checklist

- [ ] `client_secret.json` is in `.gitignore`
- [ ] `.env` file is not committed to Git
- [ ] Strong `FLASK_SECRET_KEY` is set
- [ ] YouTube OAuth tokens are secure
- [ ] DTube private keys (if any) are secure
- [ ] File upload size limits are reasonable

---

**You're all set! Start uploading to YouTube and DTube!**

NoblePort Systems - NoblePort.eth
