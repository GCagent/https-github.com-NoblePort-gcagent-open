#!/usr/bin/env python3
"""
Basic tests for the dual-platform video uploader
NoblePort Systems
"""

def test_config():
    """Test configuration module"""
    print("Testing configuration...")
    from config import Config, CopyrightPolicy

    # Test Config
    assert Config.UPLOAD_FOLDER is not None
    assert Config.MAX_FILE_SIZE > 0
    print("  ✓ Config class loaded")

    # Test CopyrightPolicy
    comparison = CopyrightPolicy.get_comparison()
    assert 'youtube' in comparison
    assert 'dtube' in comparison
    assert 'summary' in comparison
    print("  ✓ Copyright policies loaded")

    # Test YouTube policy
    yt = CopyrightPolicy.YOUTUBE
    assert yt['name'] == 'YouTube'
    assert yt['risk_level'] == 'HIGH'
    assert yt['automated_scanning'] == True
    print("  ✓ YouTube policy correct")

    # Test DTube policy
    dt = CopyrightPolicy.DTUBE
    assert dt['name'] == 'DTube'
    assert dt['risk_level'] == 'LOW'
    assert dt['automated_scanning'] == False
    print("  ✓ DTube policy correct")

    print("Configuration tests passed!\n")


def test_youtube_uploader():
    """Test YouTube uploader module"""
    print("Testing YouTube uploader...")
    from youtube_uploader import YouTubeUploader, YOUTUBE_CATEGORIES

    # Test initialization
    uploader = YouTubeUploader()
    assert uploader is not None
    print("  ✓ YouTubeUploader initialized")

    # Test warnings
    warnings = uploader.get_copyright_warnings()
    assert warnings['platform'] == 'youtube'
    assert len(warnings['warnings']) > 0
    print("  ✓ Copyright warnings available")

    # Test categories
    assert len(YOUTUBE_CATEGORIES) > 0
    assert '22' in YOUTUBE_CATEGORIES
    print("  ✓ Categories loaded")

    print("YouTube uploader tests passed!\n")


def test_dtube_uploader():
    """Test DTube uploader module"""
    print("Testing DTube uploader...")
    from dtube_uploader import DtubeUploader

    # Test initialization
    uploader = DtubeUploader()
    assert uploader is not None
    print("  ✓ DtubeUploader initialized")

    # Test warnings
    warnings = uploader.get_copyright_warnings()
    assert warnings['platform'] == 'dtube'
    assert len(warnings['warnings']) > 0
    print("  ✓ Copyright warnings available")

    # Test permlink generation
    permlink = uploader._generate_permlink("Test Video Title")
    assert 'test-video-title' in permlink
    print("  ✓ Permlink generation works")

    print("DTube uploader tests passed!\n")


def test_flask_app():
    """Test Flask application"""
    print("Testing Flask app...")
    from app import app

    # Test app exists
    assert app is not None
    print("  ✓ Flask app initialized")

    # Test routes
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        print("  ✓ Health endpoint works")

        # Test copyright policies endpoint
        response = client.get('/api/copyright-policies')
        assert response.status_code == 200
        data = response.get_json()
        assert 'youtube' in data
        assert 'dtube' in data
        print("  ✓ Copyright policies API works")

        # Test platform info endpoint
        response = client.get('/api/platform-info/youtube')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'YouTube'
        print("  ✓ Platform info API works")

    print("Flask app tests passed!\n")


def main():
    """Run all tests"""
    print("="*60)
    print("  Dual-Platform Video Uploader - Test Suite")
    print("  NoblePort Systems")
    print("="*60)
    print()

    try:
        test_config()
        test_youtube_uploader()
        test_dtube_uploader()
        test_flask_app()

        print("="*60)
        print("  ALL TESTS PASSED!")
        print("="*60)
        print()
        print("The application is ready to use!")
        print()
        print("Next steps:")
        print("  1. Configure your .env file")
        print("  2. Add client_secret.json for YouTube")
        print("  3. Start IPFS daemon for DTube")
        print("  4. Run: python app.py")
        print()
        return True

    except Exception as e:
        print()
        print("="*60)
        print("  TEST FAILED!")
        print("="*60)
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
