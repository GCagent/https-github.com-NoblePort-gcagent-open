# DTube Easy Connection App

**NoblePort Systems - Simple DTube Client**

A streamlined, user-friendly application for connecting to DTube and uploading videos to the decentralized video platform.

## Features

- 🔌 **Easy IPFS Connection** - Connect to IPFS daemon with one click
- 👤 **Simple Account Setup** - Just enter your DTube username
- 📤 **Quick Video Upload** - Upload videos directly to IPFS and DTube
- 🎨 **Beautiful Interface** - Clean, modern UI designed for ease of use
- 🚀 **No Configuration** - Works out of the box with sensible defaults
- 💰 **DTube Benefits** - No censorship, earn crypto, true ownership

## Why DTube?

### No Censorship
- No automated Content ID scanning
- No copyright bots
- Your content stays up unless legally challenged

### Earn Cryptocurrency
- Get rewarded in DTC tokens
- Earn from views and engagement
- Direct monetization without ads

### True Ownership
- Videos stored on IPFS (decentralized)
- Metadata on Avalon blockchain
- You control your content forever

## Quick Start

### Prerequisites

1. **Python 3.8+**
2. **IPFS Daemon** (must be running)

### Install IPFS

**macOS (Homebrew):**
```bash
brew install ipfs
ipfs init
ipfs daemon
```

**Linux:**
```bash
wget https://dist.ipfs.io/kubo/v0.17.0/kubo_v0.17.0_linux-amd64.tar.gz
tar -xzf kubo_v0.17.0_linux-amd64.tar.gz
cd kubo
sudo bash install.sh
ipfs init
ipfs daemon
```

**Windows:**
Download from https://dist.ipfs.io/#kubo

### Run the App

```bash
# 1. Navigate to dtube-app directory
cd dtube-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start IPFS daemon (in separate terminal)
ipfs daemon

# 4. Run the app
python app.py

# 5. Open browser to http://localhost:5001
```

### Or use the launcher script:

```bash
chmod +x launch.sh
./launch.sh
```

## How to Use

### Step 1: Connect to IPFS

1. Make sure IPFS daemon is running: `ipfs daemon`
2. Click "Connect IPFS" button
3. Wait for green "Connected" status

### Step 2: Connect Your DTube Account

1. Enter your DTube username
2. (Optional) Enter private key for publishing
3. Click "Connect Account"

### Step 3: Upload Videos

1. Select your video file (MP4, AVI, MOV, MKV, WebM, FLV)
2. Enter title and description
3. Add tags (comma-separated)
4. Click "Upload to DTube"
5. Wait for upload to complete
6. Get your DTube video URL!

## Features in Detail

### IPFS Integration
- Automatic connection to local IPFS daemon
- Support for custom IPFS nodes
- Progress tracking during upload
- IPFS hash and gateway URLs provided

### Account Management
- Username-based connection
- Optional private key for publishing
- Session persistence
- Easy disconnect/reconnect

### Video Upload
- Support for all major video formats
- Up to 5GB file size
- Real-time upload progress
- Automatic IPFS pinning
- DTube metadata publishing

### User Interface
- Clean, modern design
- Step-by-step connection wizard
- Real-time status indicators
- Helpful tooltips and guides
- Mobile-responsive layout

## DTube vs YouTube Comparison

| Feature | DTube | YouTube |
|---------|-------|---------|
| Censorship | None (automated) | Heavy (Content ID) |
| Monetization | Crypto (DTC) | Ads (Google) |
| Storage | IPFS (decentralized) | Google servers |
| Ownership | You own forever | Google's platform |
| Copyright Risk | Low (no auto-scan) | High (auto-strikes) |
| Barriers | Need IPFS | Need Google account |

## Troubleshooting

### IPFS Connection Failed

**Problem:** Can't connect to IPFS

**Solution:**
```bash
# Check if IPFS is running
ipfs id

# If not running:
ipfs daemon

# Check IPFS API address
ipfs config Addresses.API
# Should be: /ip4/127.0.0.1/tcp/5001
```

### Upload Stuck

**Problem:** Upload progress not moving

**Solutions:**
1. Check IPFS daemon is still running
2. Check your internet connection
3. Try smaller video file first
4. Restart IPFS daemon

### Can't Connect to DTube Account

**Problem:** Account connection fails

**Solution:**
1. Verify your DTube username is correct
2. Private key is optional - try without it
3. Check internet connection
4. IPFS must be connected first

## Technical Details

### Architecture

```
┌─────────────────┐
│   Web Browser   │
│   (Frontend)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Flask Server   │
│   (Backend)     │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌─────┐   ┌──────┐
│IPFS │   │DTube │
│Node │   │ API  │
└─────┘   └──────┘
```

### File Upload Process

1. User selects video file
2. File uploaded to Flask server
3. Server uploads to IPFS
4. IPFS returns content hash
5. Server publishes metadata to DTube
6. User gets DTube URL

### Security

- Private keys never stored permanently
- Session-based authentication
- No sensitive data in localStorage
- HTTPS recommended for production

## Configuration

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=5368709120
IPFS_HOST=127.0.0.1
IPFS_PORT=5001
```

### Custom IPFS Node

To use a remote IPFS node:

1. Enter custom host/port in the UI
2. Or set environment variables:
   ```env
   IPFS_HOST=your-ipfs-node.com
   IPFS_PORT=5001
   ```

## Development

### Project Structure

```
dtube-app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── launch.sh          # Launcher script
├── templates/
│   └── index.html     # Main page template
├── static/
│   ├── css/
│   │   └── style.css  # Styles
│   └── js/
│       └── app.js     # Frontend JavaScript
└── uploads/           # Temporary upload folder
```

### Running in Development

```bash
export FLASK_ENV=development
python app.py
```

### API Endpoints

- `GET /` - Main page
- `GET /api/status` - Connection status
- `POST /api/connect/ipfs` - Connect to IPFS
- `POST /api/connect/account` - Connect DTube account
- `POST /api/disconnect` - Disconnect account
- `POST /api/upload` - Upload video
- `GET /api/check-ipfs` - Check IPFS daemon
- `GET /health` - Health check

## Production Deployment

See the main project's `DEPLOYMENT.md` for production deployment options including Docker and systemd services.

Quick production setup:

```bash
# Install dependencies
pip install -r requirements.txt gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## Contributing

Contributions welcome! This is part of the larger Dual-Platform Video Uploader project by NoblePort Systems.

## Support

For issues or questions:
- Check this README
- Review DTube docs: https://about.d.tube
- Review IPFS docs: https://docs.ipfs.io
- Contact NoblePort Systems - NoblePort.eth

## License

MIT License - See LICENSE file in main project

## Credits

**NoblePort Systems - NoblePort.eth**

Part of the Dual-Platform Video Uploader project.

## Links

- **DTube:** https://d.tube
- **IPFS:** https://ipfs.io
- **Avalon Blockchain:** https://avalon.d.tube
- **NoblePort Systems:** NoblePort.eth

---

**Easy DTube uploading for everyone!** 🚀
