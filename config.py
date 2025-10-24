"""
Configuration module for the dual-platform video uploader
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 5368709120))  # 5GB default

    # YouTube settings
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
    YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    # DTube settings
    DTUBE_PRIVATE_KEY = os.getenv('DTUBE_PRIVATE_KEY')
    DTUBE_USERNAME = os.getenv('DTUBE_USERNAME')
    DTUBE_API_URL = 'https://avalon.d.tube'

    # IPFS settings
    IPFS_HOST = os.getenv('IPFS_HOST', '127.0.0.1')
    IPFS_PORT = int(os.getenv('IPFS_PORT', 5001))

    @staticmethod
    def init_app():
        """Initialize application directories"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


class CopyrightPolicy:
    """Copyright policy information for each platform"""

    YOUTUBE = {
        'name': 'YouTube',
        'enforcement': 'Automated Content ID system scans all uploads',
        'blocking': 'Immediate blocking or monetization based on rights holder choice',
        'strictness': 'Very Strict',
        'risk_level': 'HIGH',
        'automated_scanning': True,
        'warnings': [
            'Content ID scans all uploads automatically',
            'Copyrighted content may be blocked globally',
            'Channel strikes can lead to account termination',
            'Fair use claims may still be flagged',
            'Monetization may be blocked or diverted to rights holders'
        ],
        'recommendations': [
            'Use only original content or properly licensed material',
            'Obtain written permission for copyrighted content',
            'Review YouTube copyright guidelines before uploading',
            'Consider using YouTube Audio Library for music',
            'Be prepared to dispute false claims through YouTube process'
        ]
    }

    DTUBE = {
        'name': 'DTube',
        'enforcement': 'No automated scanning; relies on DMCA/manual complaints',
        'blocking': 'Rare - content remains unless legally reported',
        'strictness': 'Lenient',
        'risk_level': 'LOW',
        'automated_scanning': False,
        'warnings': [
            'No automated copyright detection',
            'You are still legally liable for copyright infringement',
            'Rights holders can file DMCA takedown notices',
            'Decentralized storage may make removal difficult',
            'No platform protection against lawsuits'
        ],
        'recommendations': [
            'Understand you remain legally responsible for content',
            'Keep records of content ownership or licensing',
            'Respond promptly to any DMCA notices',
            'Consider fair use doctrine applicability',
            'Be aware content may persist on IPFS even after removal attempts'
        ]
    }

    @staticmethod
    def get_comparison():
        """Get a comparison matrix of both platforms"""
        return {
            'youtube': CopyrightPolicy.YOUTUBE,
            'dtube': CopyrightPolicy.DTUBE,
            'summary': {
                'best_for_original_content': 'Both platforms',
                'best_for_remixes_compilations': 'DTube (but still legally risky)',
                'best_for_monetization': 'YouTube (if content is original)',
                'lowest_takedown_risk': 'DTube',
                'most_professional': 'YouTube'
            }
        }
