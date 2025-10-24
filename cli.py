#!/usr/bin/env python3
"""
Command-line interface for dual-platform video uploader
For NoblePort Systems
"""
import sys
import argparse
from youtube_uploader import YouTubeUploader, YOUTUBE_CATEGORIES
from dtube_uploader import DtubeUploader, check_ipfs_daemon
from config import CopyrightPolicy
import json


def print_banner():
    """Print application banner"""
    print("="*70)
    print("  Dual-Platform Video Uploader - CLI")
    print("  NoblePort Systems")
    print("  YouTube & DTube Upload Tool")
    print("="*70)
    print()


def show_copyright_comparison():
    """Display copyright policy comparison"""
    comparison = CopyrightPolicy.get_comparison()

    print("\n" + "="*70)
    print("COPYRIGHT POLICY COMPARISON")
    print("="*70)

    # YouTube
    yt = comparison['youtube']
    print(f"\nYOUTUBE:")
    print(f"  Risk Level: {yt['risk_level']}")
    print(f"  Enforcement: {yt['enforcement']}")
    print(f"  Automated Scanning: {'Yes' if yt['automated_scanning'] else 'No'}")
    print(f"  Strictness: {yt['strictness']}")

    # DTube
    dt = comparison['dtube']
    print(f"\nDTUBE:")
    print(f"  Risk Level: {dt['risk_level']}")
    print(f"  Enforcement: {dt['enforcement']}")
    print(f"  Automated Scanning: {'Yes' if dt['automated_scanning'] else 'No'}")
    print(f"  Strictness: {dt['strictness']}")

    # Summary
    print(f"\nRECOMMENDATIONS:")
    summary = comparison['summary']
    for key, value in summary.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print("="*70 + "\n")


def upload_to_youtube(args):
    """Upload video to YouTube"""
    print("\nInitializing YouTube upload...")

    uploader = YouTubeUploader()

    # Authenticate
    print("Authenticating with YouTube...")
    try:
        uploader.authenticate()
        channel = uploader.get_channel_info()
        if channel:
            print(f"Authenticated as: {channel['title']}")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

    # Upload video
    result = uploader.upload_video(
        file_path=args.video,
        title=args.title,
        description=args.description or '',
        category=args.category,
        privacy=args.privacy,
        tags=args.tags.split(',') if args.tags else [],
        check_copyright=not args.skip_warnings
    )

    if result['success']:
        print(f"\n{'='*70}")
        print("UPLOAD SUCCESSFUL!")
        print(f"{'='*70}")
        print(f"Platform: YouTube")
        print(f"Video ID: {result['video_id']}")
        print(f"URL: {result['url']}")
        print(f"{'='*70}\n")
        return True
    else:
        print(f"\nUpload failed: {result['error']}\n")
        return False


def upload_to_dtube(args):
    """Upload video to DTube"""
    print("\nInitializing DTube upload...")

    # Check IPFS daemon
    if not check_ipfs_daemon():
        print("\nERROR: IPFS daemon must be running for DTube uploads.")
        print("Please start IPFS daemon with: ipfs daemon")
        return False

    uploader = DtubeUploader()

    # Upload video
    result = uploader.upload_video(
        file_path=args.video,
        title=args.title,
        description=args.description or '',
        tags=args.tags.split(',') if args.tags else [],
        check_copyright=not args.skip_warnings
    )

    if result['success']:
        print(f"\n{'='*70}")
        print("UPLOAD SUCCESSFUL!")
        print(f"{'='*70}")
        print(f"Platform: DTube")
        print(f"IPFS Hash: {result['ipfs_hash']}")
        print(f"DTube URL: {result['url']}")
        print(f"IPFS Gateway: {result['ipfs_gateway']}")
        if 'note' in result:
            print(f"\nNote: {result['note']}")
        print(f"{'='*70}\n")
        return True
    else:
        print(f"\nUpload failed: {result['error']}\n")
        return False


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Dual-Platform Video Uploader for YouTube and DTube',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload to YouTube
  python cli.py upload --platform youtube --video myvideo.mp4 --title "My Video"

  # Upload to DTube
  python cli.py upload --platform dtube --video myvideo.mp4 --title "My Video"

  # Upload to both platforms
  python cli.py upload --platform both --video myvideo.mp4 --title "My Video"

  # Show copyright comparison
  python cli.py compare

  # List YouTube categories
  python cli.py categories
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload video to platform(s)')
    upload_parser.add_argument('--video', required=True, help='Path to video file')
    upload_parser.add_argument('--title', required=True, help='Video title')
    upload_parser.add_argument('--description', help='Video description')
    upload_parser.add_argument('--tags', help='Comma-separated tags')
    upload_parser.add_argument('--platform', choices=['youtube', 'dtube', 'both'],
                              default='youtube', help='Upload platform')
    upload_parser.add_argument('--privacy', choices=['public', 'private', 'unlisted'],
                              default='private', help='YouTube privacy setting')
    upload_parser.add_argument('--category', default='22',
                              help='YouTube category ID (default: 22 = People & Blogs)')
    upload_parser.add_argument('--skip-warnings', action='store_true',
                              help='Skip copyright warnings')

    # Compare command
    subparsers.add_parser('compare', help='Show copyright policy comparison')

    # Categories command
    subparsers.add_parser('categories', help='List YouTube categories')

    # IPFS check command
    subparsers.add_parser('check-ipfs', help='Check IPFS daemon status')

    args = parser.parse_args()

    print_banner()

    if args.command == 'upload':
        success = True

        if args.platform in ['youtube', 'both']:
            success = upload_to_youtube(args) and success

        if args.platform in ['dtube', 'both']:
            success = upload_to_dtube(args) and success

        sys.exit(0 if success else 1)

    elif args.command == 'compare':
        show_copyright_comparison()

    elif args.command == 'categories':
        print("\nYouTube Categories:")
        print("="*70)
        for cat_id, cat_name in sorted(YOUTUBE_CATEGORIES.items(), key=lambda x: int(x[0])):
            print(f"  {cat_id:>3}: {cat_name}")
        print("="*70 + "\n")

    elif args.command == 'check-ipfs':
        print("\nChecking IPFS daemon status...")
        check_ipfs_daemon()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
