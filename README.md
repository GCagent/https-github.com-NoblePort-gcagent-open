# Dual-Platform Video Uploader

**NoblePort Systems - NoblePort.eth**

A comprehensive application for uploading videos to both YouTube and DTube with built-in copyright policy awareness and comparison.

## Features

- **Dual-Platform Support**: Upload to YouTube and/or DTube simultaneously
- **Copyright Policy Comparison**: Side-by-side comparison of YouTube vs DTube copyright enforcement
- **Interactive Warnings**: Platform-specific copyright warnings before upload
- **Web Interface**: Modern, responsive web UI for easy video uploads
- **Command-Line Interface**: Full-featured CLI for automation and scripting
- **YouTube Integration**: Full OAuth2 authentication with Google APIs
- **DTube/IPFS Integration**: Decentralized video storage via IPFS
- **Progress Tracking**: Real-time upload progress monitoring
- **Metadata Management**: Comprehensive video metadata handling

## Copyright Policy Comparison

### YouTube
- **Risk Level**: HIGH
- **Enforcement**: Automated Content ID system scans all uploads
- **Automated Scanning**: Yes
- **Blocking**: Immediate, sometimes global
- **Consequences**: Channel strikes, monetization blocks, content removal

### DTube
- **Risk Level**: LOW
- **Enforcement**: No automated scanning; relies on DMCA/manual complaints
- **Automated Scanning**: No
- **Blocking**: Rare - content remains unless legally reported
- **Consequences**: Legal liability remains, but less platform interference

## Installation

### Prerequisites

1. **Python 3.8+**
2. **IPFS** (for DTube uploads)
   ```bash
   # Install IPFS: https://docs.ipfs.io/install/
   ipfs init
   ipfs daemon
   ```
3. **YouTube API Credentials** (for YouTube uploads)
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Download `client_secret.json`

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/NoblePort/gcagent-open.git
cd gcagent-open

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### Configuration

Edit `.env` file with your credentials:

```env
# YouTube API Configuration
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret

# DTube Configuration
DTUBE_PRIVATE_KEY=your_dtube_private_key
DTUBE_USERNAME=your_dtube_username

# IPFS Configuration (usually default)
IPFS_HOST=127.0.0.1
IPFS_PORT=5001

# Application Settings
FLASK_SECRET_KEY=your_secret_key_here
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=5368709120  # 5GB
```

## Usage

### Web Interface

1. Start IPFS daemon (for DTube):
   ```bash
   ipfs daemon
   ```

2. Start the web application:
   ```bash
   python app.py
   ```

3. Open browser to: `http://localhost:5000`

4. Use the web interface to:
   - Compare copyright policies
   - Select platform(s) for upload
   - Upload videos with metadata
   - Track upload progress

### Command-Line Interface

#### Show Copyright Comparison
```bash
python cli.py compare
```

#### Upload to YouTube
```bash
python cli.py upload \
  --platform youtube \
  --video /path/to/video.mp4 \
  --title "My Amazing Video" \
  --description "Video description here" \
  --tags "tag1, tag2, tag3" \
  --privacy private \
  --category 22
```

#### Upload to DTube
```bash
python cli.py upload \
  --platform dtube \
  --video /path/to/video.mp4 \
  --title "My Amazing Video" \
  --description "Video description here" \
  --tags "tag1, tag2, tag3"
```

#### Upload to Both Platforms
```bash
python cli.py upload \
  --platform both \
  --video /path/to/video.mp4 \
  --title "My Amazing Video" \
  --description "Video description here" \
  --tags "tag1, tag2, tag3"
```

#### List YouTube Categories
```bash
python cli.py categories
```

#### Check IPFS Status
```bash
python cli.py check-ipfs
```

## API Reference

### REST API Endpoints

#### Get Copyright Policies
```http
GET /api/copyright-policies
```

Returns comparison of YouTube and DTube copyright policies.

#### Get Platform Info
```http
GET /api/platform-info/<platform>
```

Get detailed information about a specific platform (youtube or dtube).

#### YouTube Authentication
```http
POST /api/youtube/authenticate
```

Authenticate with YouTube and get channel information.

#### Upload Video
```http
POST /api/upload
```

Upload video to selected platform(s).

**Form Data:**
- `video`: Video file
- `title`: Video title
- `description`: Video description
- `tags`: Comma-separated tags
- `platforms`: JSON array of platforms
- `privacy`: YouTube privacy (public/private/unlisted)
- `category`: YouTube category ID

## Python Module Usage

### YouTube Uploader

```python
from youtube_uploader import YouTubeUploader

# Initialize
uploader = YouTubeUploader()

# Authenticate
uploader.authenticate()

# Get channel info
channel = uploader.get_channel_info()
print(f"Channel: {channel['title']}")

# Upload video
result = uploader.upload_video(
    file_path="video.mp4",
    title="My Video",
    description="Description here",
    tags=["tag1", "tag2"],
    privacy="private",
    category="22"
)

print(f"Video URL: {result['url']}")
```

### DTube Uploader

```python
from dtube_uploader import DtubeUploader

# Initialize
uploader = DtubeUploader()

# Connect to IPFS
uploader.connect_ipfs()

# Upload video
result = uploader.upload_video(
    file_path="video.mp4",
    title="My Video",
    description="Description here",
    tags=["tag1", "tag2"]
)

print(f"IPFS Hash: {result['ipfs_hash']}")
print(f"DTube URL: {result['url']}")
```

### Copyright Policy Comparison

```python
from config import CopyrightPolicy

# Get all policies
comparison = CopyrightPolicy.get_comparison()

# Get YouTube warnings
yt_warnings = CopyrightPolicy.YOUTUBE['warnings']
for warning in yt_warnings:
    print(f"- {warning}")

# Get DTube warnings
dt_warnings = CopyrightPolicy.DTUBE['warnings']
for warning in dt_warnings:
    print(f"- {warning}")
```

## File Structure

```
.
├── app.py                  # Flask web application
├── cli.py                  # Command-line interface
├── config.py               # Configuration and copyright policies
├── youtube_uploader.py     # YouTube API integration
├── dtube_uploader.py       # DTube/IPFS integration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore file
├── README.md               # This file
├── templates/
│   └── index.html          # Web interface template
├── static/
│   ├── css/
│   │   └── style.css       # Web interface styles
│   └── js/
│       └── app.js          # Web interface JavaScript
└── uploads/                # Temporary upload folder
```

## YouTube Categories

| ID | Category |
|----|----------|
| 1  | Film & Animation |
| 2  | Autos & Vehicles |
| 10 | Music |
| 15 | Pets & Animals |
| 17 | Sports |
| 19 | Travel & Events |
| 20 | Gaming |
| 22 | People & Blogs |
| 23 | Comedy |
| 24 | Entertainment |
| 25 | News & Politics |
| 26 | Howto & Style |
| 27 | Education |
| 28 | Science & Technology |
| 29 | Nonprofits & Activism |

## Security & Legal Considerations

### Important Warnings

1. **Copyright Liability**: Using this tool does NOT absolve you of copyright liability. You are responsible for ensuring you have rights to upload content.

2. **YouTube Risks**:
   - Automated Content ID will scan your uploads
   - Copyrighted content may be blocked or monetized by rights holders
   - Channel strikes can lead to account termination
   - Fair use claims may still be flagged

3. **DTube Risks**:
   - While less likely to be auto-blocked, you remain legally liable
   - Rights holders can file DMCA takedown notices
   - Content on IPFS may persist even after removal attempts
   - Decentralized nature doesn't provide legal protection

4. **Best Practices**:
   - Only upload content you own or have explicit permission to use
   - Keep records of licensing and permissions
   - Understand fair use doctrine in your jurisdiction
   - Respond promptly to any legal notices
   - Consider using royalty-free music and stock footage

### API Keys & Credentials

- Never commit API keys or credentials to version control
- Use environment variables for sensitive data
- Rotate credentials regularly
- Use OAuth2 token files safely (they're in .gitignore)

## Troubleshooting

### YouTube Authentication Issues

**Problem**: OAuth2 authentication fails

**Solution**:
1. Verify `client_secret.json` is in the project directory
2. Check that YouTube Data API v3 is enabled in Google Cloud Console
3. Ensure OAuth consent screen is configured
4. Try deleting `token.pickle` and re-authenticating

### IPFS Connection Issues

**Problem**: Cannot connect to IPFS

**Solution**:
```bash
# Check if IPFS daemon is running
ipfs id

# If not running, start it
ipfs daemon

# Check the API address
ipfs config Addresses.API
# Should be: /ip4/127.0.0.1/tcp/5001
```

### File Upload Errors

**Problem**: File size too large

**Solution**:
- YouTube: Max 256GB (or 12 hours)
- DTube/IPFS: Depends on IPFS configuration
- Adjust `MAX_FILE_SIZE` in `.env`

**Problem**: Unsupported file format

**Solution**: Convert video to supported format (MP4, AVI, MOV, MKV, WebM, FLV)

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Credits

**NoblePort Systems**
- NoblePort.eth
- [GitHub](https://github.com/NoblePort)

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact NoblePort.eth

## Disclaimer

This software is provided "as is" without warranty of any kind. The authors are not responsible for any copyright infringement or legal issues arising from the use of this software. Users are solely responsible for ensuring they have the right to upload and distribute content.

---

**NoblePort Systems - Empowering Decentralized Content Creation**
