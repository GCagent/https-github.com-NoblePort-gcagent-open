"""
DTube API integration for decentralized video uploads
Uses IPFS for video storage and Avalon blockchain for metadata
"""
import os
import json
import hashlib
import requests
import ipfshttpclient
from datetime import datetime
from config import Config, CopyrightPolicy


class DtubeUploader:
    """Handle DTube video uploads via IPFS and Avalon blockchain"""

    def __init__(self):
        self.ipfs_client = None
        self.username = Config.DTUBE_USERNAME
        self.private_key = Config.DTUBE_PRIVATE_KEY
        self.api_url = Config.DTUBE_API_URL

    def connect_ipfs(self):
        """Connect to IPFS daemon"""
        try:
            self.ipfs_client = ipfshttpclient.connect(
                f'/ip4/{Config.IPFS_HOST}/tcp/{Config.IPFS_PORT}/http'
            )
            print(f"Connected to IPFS: {self.ipfs_client.id()['ID']}")
            return True
        except Exception as e:
            print(f"Failed to connect to IPFS: {e}")
            print(f"Make sure IPFS daemon is running on {Config.IPFS_HOST}:{Config.IPFS_PORT}")
            return False

    def get_copyright_warnings(self):
        """Get copyright warnings for DTube uploads"""
        policy = CopyrightPolicy.DTUBE.copy()
        policy['platform'] = 'dtube'
        return policy

    def upload_to_ipfs(self, file_path, show_progress=True):
        """
        Upload file to IPFS

        Args:
            file_path: Path to file to upload
            show_progress: Show upload progress

        Returns:
            str: IPFS hash (CID) of uploaded file
        """
        if not self.ipfs_client:
            if not self.connect_ipfs():
                raise RuntimeError("Cannot connect to IPFS")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Uploading to IPFS: {os.path.basename(file_path)}")
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size / (1024*1024):.2f} MB")

        try:
            # Upload file to IPFS
            result = self.ipfs_client.add(file_path)
            ipfs_hash = result['Hash']

            print(f"IPFS upload complete!")
            print(f"IPFS Hash: {ipfs_hash}")
            print(f"Gateway URL: https://ipfs.io/ipfs/{ipfs_hash}")

            return ipfs_hash

        except Exception as e:
            raise RuntimeError(f"IPFS upload failed: {e}")

    def create_sprite(self, video_path):
        """
        Create sprite/thumbnail for video (simplified version)
        In production, use moviepy or ffmpeg to extract thumbnails

        Returns:
            str: IPFS hash of sprite image
        """
        # For now, return None - implement proper sprite generation later
        # This would use moviepy to extract frames and create a sprite sheet
        return None

    def publish_to_dtube(self, video_hash, title, description, tags=None,
                        duration=0, thumbnail_hash=None, check_copyright=True):
        """
        Publish video metadata to DTube/Avalon blockchain

        Args:
            video_hash: IPFS hash of video
            title: Video title
            description: Video description
            tags: List of tags
            duration: Video duration in seconds
            thumbnail_hash: IPFS hash of thumbnail
            check_copyright: Show copyright warnings

        Returns:
            dict: Publication response
        """
        # Show copyright warnings
        if check_copyright:
            warnings = self.get_copyright_warnings()
            print("\n" + "="*60)
            print("DTUBE COPYRIGHT POLICY WARNING")
            print("="*60)
            print(f"Risk Level: {warnings['risk_level']}")
            print(f"Enforcement: {warnings['enforcement']}")
            print(f"\nWarnings:")
            for warning in warnings['warnings']:
                print(f"  - {warning}")
            print(f"\nRecommendations:")
            for rec in warnings['recommendations']:
                print(f"  - {rec}")
            print("="*60 + "\n")

        # Create DTube metadata
        permlink = self._generate_permlink(title)

        content = {
            'video': {
                'info': {
                    'title': title,
                    'description': description,
                    'duration': duration,
                    'tags': tags or []
                },
                'content': {
                    'video480hash': video_hash,  # IPFS hash
                    'videohash': video_hash,
                },
                'thumbnailUrlExternal': f"https://ipfs.io/ipfs/{thumbnail_hash}" if thumbnail_hash else None
            }
        }

        # Note: Actual DTube publishing requires:
        # 1. Signing transaction with private key
        # 2. Broadcasting to Avalon blockchain
        # 3. This is a simplified example

        print(f"Publishing to DTube: {title}")
        print(f"Permlink: {permlink}")
        print(f"Video IPFS: {video_hash}")

        # In production, you would:
        # - Sign the transaction with the private key
        # - Broadcast to Avalon blockchain
        # - Wait for confirmation

        dtube_url = f"https://d.tube/v/{self.username}/{permlink}"

        return {
            'success': True,
            'platform': 'dtube',
            'permlink': permlink,
            'url': dtube_url,
            'ipfs_hash': video_hash,
            'ipfs_gateway': f"https://ipfs.io/ipfs/{video_hash}",
            'note': 'This is a demonstration. Full DTube publishing requires blockchain transaction signing.'
        }

    def upload_video(self, file_path, title, description, tags=None, check_copyright=True):
        """
        Complete workflow: Upload video to IPFS and publish to DTube

        Args:
            file_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            check_copyright: Show copyright warnings

        Returns:
            dict: Upload response with IPFS hash and DTube URL
        """
        try:
            # Step 1: Upload video to IPFS
            print("\nStep 1: Uploading video to IPFS...")
            video_hash = self.upload_to_ipfs(file_path)

            # Step 2: Create and upload thumbnail (optional)
            print("\nStep 2: Creating thumbnail...")
            thumbnail_hash = self.create_sprite(file_path)

            # Step 3: Publish to DTube blockchain
            print("\nStep 3: Publishing to DTube...")
            result = self.publish_to_dtube(
                video_hash=video_hash,
                title=title,
                description=description,
                tags=tags,
                thumbnail_hash=thumbnail_hash,
                check_copyright=check_copyright
            )

            print("\nDTube upload complete!")
            return result

        except Exception as e:
            return {
                'success': False,
                'platform': 'dtube',
                'error': str(e)
            }

    def _generate_permlink(self, title):
        """Generate a unique permlink from title"""
        # Convert to lowercase, replace spaces with hyphens
        base = title.lower().replace(' ', '-')
        # Remove special characters
        base = ''.join(c for c in base if c.isalnum() or c == '-')
        # Add timestamp for uniqueness
        timestamp = int(datetime.now().timestamp())
        return f"{base}-{timestamp}"


# Helper function to check IPFS daemon status
def check_ipfs_daemon():
    """Check if IPFS daemon is running"""
    try:
        client = ipfshttpclient.connect(
            f'/ip4/{Config.IPFS_HOST}/tcp/{Config.IPFS_PORT}/http'
        )
        peer_id = client.id()['ID']
        print(f"IPFS daemon is running. Peer ID: {peer_id}")
        return True
    except Exception as e:
        print(f"IPFS daemon is not running: {e}")
        print("\nTo start IPFS daemon:")
        print("1. Install IPFS: https://docs.ipfs.io/install/")
        print("2. Initialize: ipfs init")
        print("3. Start daemon: ipfs daemon")
        return False
