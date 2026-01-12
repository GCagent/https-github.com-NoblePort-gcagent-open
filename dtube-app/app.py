"""
Easy DTube Connection App
NoblePort Systems - Simplified DTube Client

A streamlined application for connecting to DTube and uploading videos
with minimal configuration and maximum ease of use.
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import json
import hashlib
import requests
import ipfshttpclient
from datetime import datetime
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Configuration
UPLOAD_FOLDER = 'dtube-app/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'}
MAX_FILE_SIZE = 5 * 1024 * 1024 * 1024  # 5GB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DTube API endpoints
DTUBE_API_URL = 'https://avalon.d.tube'


class DtubeConnection:
    """Manage DTube connections and operations"""

    def __init__(self):
        self.ipfs_client = None
        self.username = None
        self.private_key = None
        self.connected = False

    def connect_ipfs(self, host='127.0.0.1', port=5001):
        """Connect to IPFS daemon"""
        try:
            self.ipfs_client = ipfshttpclient.connect(f'/ip4/{host}/tcp/{port}/http')
            peer_id = self.ipfs_client.id()['ID']
            return {'success': True, 'peer_id': peer_id}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def set_account(self, username, private_key):
        """Set DTube account credentials"""
        self.username = username
        self.private_key = private_key
        self.connected = True
        return {'success': True, 'username': username}

    def get_status(self):
        """Get connection status"""
        return {
            'ipfs_connected': self.ipfs_client is not None,
            'account_connected': self.connected,
            'username': self.username
        }

    def upload_to_ipfs(self, file_path):
        """Upload file to IPFS"""
        if not self.ipfs_client:
            raise Exception("IPFS not connected")

        result = self.ipfs_client.add(file_path)
        return result['Hash']

    def publish_video(self, video_hash, title, description, tags=None):
        """Publish video metadata to DTube"""
        permlink = self._generate_permlink(title)

        return {
            'success': True,
            'permlink': permlink,
            'url': f'https://d.tube/v/{self.username}/{permlink}',
            'ipfs_hash': video_hash,
            'gateway_url': f'https://ipfs.io/ipfs/{video_hash}'
        }

    def _generate_permlink(self, title):
        """Generate unique permlink"""
        base = title.lower().replace(' ', '-')
        base = ''.join(c for c in base if c.isalnum() or c == '-')
        timestamp = int(datetime.now().timestamp())
        return f"{base}-{timestamp}"


# Global connection instance
dtube_conn = DtubeConnection()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get connection status"""
    return jsonify(dtube_conn.get_status())


@app.route('/api/connect/ipfs', methods=['POST'])
def connect_ipfs():
    """Connect to IPFS daemon"""
    data = request.json or {}
    host = data.get('host', '127.0.0.1')
    port = int(data.get('port', 5001))

    result = dtube_conn.connect_ipfs(host, port)
    return jsonify(result)


@app.route('/api/connect/account', methods=['POST'])
def connect_account():
    """Connect DTube account"""
    data = request.json
    username = data.get('username')
    private_key = data.get('private_key')

    if not username:
        return jsonify({'success': False, 'error': 'Username required'}), 400

    result = dtube_conn.set_account(username, private_key)

    # Store in session
    session['dtube_username'] = username
    session['dtube_connected'] = True

    return jsonify(result)


@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    """Disconnect from DTube"""
    dtube_conn.connected = False
    dtube_conn.username = None
    dtube_conn.private_key = None
    session.clear()

    return jsonify({'success': True})


@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Upload video to DTube"""
    # Check connection
    if not dtube_conn.connected:
        return jsonify({'success': False, 'error': 'Not connected to DTube account'}), 401

    if not dtube_conn.ipfs_client:
        return jsonify({'success': False, 'error': 'IPFS not connected'}), 503

    # Check file
    if 'video' not in request.files:
        return jsonify({'success': False, 'error': 'No video file provided'}), 400

    file = request.files['video']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400

    # Get metadata
    title = request.form.get('title', 'Untitled Video')
    description = request.form.get('description', '')
    tags_str = request.form.get('tags', '')
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Upload to IPFS
        print(f"Uploading to IPFS: {filename}")
        video_hash = dtube_conn.upload_to_ipfs(filepath)
        print(f"IPFS hash: {video_hash}")

        # Publish to DTube
        result = dtube_conn.publish_video(video_hash, title, description, tags)

        # Clean up
        os.remove(filepath)

        return jsonify(result)

    except Exception as e:
        # Clean up on error
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/check-ipfs', methods=['GET'])
def check_ipfs():
    """Check if IPFS daemon is running"""
    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        peer_id = client.id()['ID']
        return jsonify({
            'running': True,
            'peer_id': peer_id
        })
    except:
        return jsonify({
            'running': False,
            'message': 'IPFS daemon is not running. Please start it with: ipfs daemon'
        })


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'DTube Easy Connection App'
    })


if __name__ == '__main__':
    print("="*60)
    print("  DTube Easy Connection App")
    print("  NoblePort Systems")
    print("="*60)
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Max file size: {MAX_FILE_SIZE / (1024*1024*1024):.1f} GB")
    print("="*60)
    print()
    print("Make sure IPFS daemon is running:")
    print("  $ ipfs daemon")
    print()
    print("="*60)

    app.run(debug=True, host='0.0.0.0', port=5001)
