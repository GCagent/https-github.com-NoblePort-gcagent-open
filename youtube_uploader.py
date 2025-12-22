"""
YouTube API integration for video uploads
Handles authentication and upload with copyright policy awareness
"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from config import Config, CopyrightPolicy


class YouTubeUploader:
    """Handle YouTube video uploads with OAuth2 authentication"""

    def __init__(self):
        self.credentials = None
        self.youtube = None
        self.scopes = Config.YOUTUBE_SCOPES

    def authenticate(self, credentials_file='client_secret.json', token_file='token.pickle'):
        """
        Authenticate with YouTube API using OAuth2

        Args:
            credentials_file: Path to client_secret.json from Google Console
            token_file: Path to store/load the access token

        Returns:
            bool: True if authentication successful
        """
        # Load saved credentials if they exist
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)

        # If credentials are invalid or don't exist, authenticate
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                if not os.path.exists(credentials_file):
                    raise FileNotFoundError(
                        f"YouTube credentials file not found: {credentials_file}\n"
                        "Download it from Google Cloud Console:\n"
                        "1. Go to https://console.cloud.google.com/\n"
                        "2. Create a project and enable YouTube Data API v3\n"
                        "3. Create OAuth 2.0 credentials\n"
                        "4. Download and save as client_secret.json"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, self.scopes
                )
                self.credentials = flow.run_local_server(port=8080)

            # Save credentials for future use
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)

        self.youtube = build('youtube', 'v3', credentials=self.credentials)
        return True

    def get_copyright_warnings(self):
        """Get copyright warnings for YouTube uploads"""
        policy = CopyrightPolicy.YOUTUBE.copy()
        policy['platform'] = 'youtube'
        return policy

    def upload_video(self, file_path, title, description, category='22',
                    privacy='private', tags=None, check_copyright=True):
        """
        Upload video to YouTube with copyright policy awareness

        Args:
            file_path: Path to video file
            title: Video title
            description: Video description
            category: YouTube category ID (default: 22 = People & Blogs)
            privacy: Privacy status (public, private, unlisted)
            tags: List of tags
            check_copyright: Show copyright warnings before upload

        Returns:
            dict: Upload response with video ID and URL
        """
        if not self.youtube:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")

        # Show copyright warnings
        if check_copyright:
            warnings = self.get_copyright_warnings()
            print("\n" + "="*60)
            print("YOUTUBE COPYRIGHT POLICY WARNING")
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

        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }

        # Create MediaFileUpload object
        media = MediaFileUpload(
            file_path,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True
        )

        try:
            # Execute upload
            print(f"Uploading to YouTube: {title}")
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"Upload progress: {progress}%")

            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            print(f"Upload complete! Video ID: {video_id}")
            print(f"URL: {video_url}")

            return {
                'success': True,
                'platform': 'youtube',
                'video_id': video_id,
                'url': video_url,
                'response': response
            }

        except HttpError as e:
            error_message = f"YouTube API error: {e}"
            print(f"Error: {error_message}")
            return {
                'success': False,
                'platform': 'youtube',
                'error': error_message
            }

    def get_channel_info(self):
        """Get authenticated user's channel information"""
        if not self.youtube:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            request = self.youtube.channels().list(
                part='snippet,statistics',
                mine=True
            )
            response = request.execute()

            if response['items']:
                channel = response['items'][0]
                return {
                    'id': channel['id'],
                    'title': channel['snippet']['title'],
                    'description': channel['snippet']['description'],
                    'subscribers': channel['statistics'].get('subscriberCount', 0),
                    'videos': channel['statistics'].get('videoCount', 0)
                }
            return None

        except HttpError as e:
            print(f"Error fetching channel info: {e}")
            return None


# Category IDs for reference
YOUTUBE_CATEGORIES = {
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles',
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '19': 'Travel & Events',
    '20': 'Gaming',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '27': 'Education',
    '28': 'Science & Technology',
    '29': 'Nonprofits & Activism'
}
