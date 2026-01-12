# DTube App - Quick Start Guide

**Get uploading to DTube in 3 minutes!**

## The Fastest Way

```bash
cd dtube-app
./launch.sh
```

That's it! The launcher will:
- Check Python and IPFS
- Install dependencies
- Start IPFS daemon if needed
- Launch the app at http://localhost:5001

## Step-by-Step Setup

### 1. Install IPFS (One-Time Setup)

**macOS:**
```bash
brew install ipfs
ipfs init
```

**Linux:**
```bash
wget https://dist.ipfs.io/kubo/v0.17.0/kubo_v0.17.0_linux-amd64.tar.gz
tar -xzf kubo_v0.17.0_linux-amd64.tar.gz
cd kubo && sudo bash install.sh
ipfs init
```

### 2. Start IPFS Daemon

```bash
ipfs daemon
```

Keep this running in a separate terminal.

### 3. Run the DTube App

**Option A: Use the launcher (recommended)**
```bash
cd dtube-app
./launch.sh
```

**Option B: Manual start**
```bash
cd dtube-app
pip install -r requirements.txt
python app.py
```

### 4. Open Your Browser

Go to: **http://localhost:5001**

## Using the App

### First Time Setup

1. **Connect to IPFS**
   - Click "Connect IPFS" button
   - You'll see green "Connected" status

2. **Connect Your DTube Account**
   - Enter your DTube username
   - Private key is optional (leave empty for view-only)
   - Click "Connect Account"

### Upload a Video

1. Click "Choose File" and select your video
2. Enter title and description
3. Add tags (comma-separated)
4. Click "Upload to DTube"
5. Wait for upload to complete
6. Get your DTube URL!

## Troubleshooting

### "Can't connect to IPFS"

Make sure IPFS daemon is running:
```bash
ipfs daemon
```

### "IPFS not installed"

Install IPFS:
- macOS: `brew install ipfs`
- Linux: https://docs.ipfs.io/install/

### "Connection refused"

Check IPFS is listening on port 5001:
```bash
ipfs config Addresses.API
# Should show: /ip4/127.0.0.1/tcp/5001
```

### "Upload stuck"

1. Check IPFS daemon is still running
2. Try a smaller video file first
3. Check your internet connection

## Tips

- **File Size:** Keep videos under 1GB for faster uploads
- **Format:** MP4 works best
- **Tags:** Use relevant tags for discoverability
- **Titles:** Clear, descriptive titles get more views

## DTube Benefits

✅ **No Censorship** - No automated content blocking
✅ **Earn Crypto** - Get DTC tokens from engagement
✅ **Own Forever** - Your content on IPFS/blockchain
✅ **No Ads** - Monetize directly with crypto

## Need Help?

- Read the full README.md
- Check DTube docs: https://about.d.tube
- Check IPFS docs: https://docs.ipfs.io

---

**NoblePort Systems - NoblePort.eth**
*Making DTube easy for everyone!*
