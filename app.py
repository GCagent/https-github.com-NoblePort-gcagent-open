"""
Main Flask application for dual-platform video uploader
Provides web interface for uploading to YouTube and DTube
"""
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config, CopyrightPolicy
from youtube_uploader import YouTubeUploader
from dtube_uploader import DtubeUploader
import json

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize uploaders
youtube_uploader = YouTubeUploader()
dtube_uploader = DtubeUploader()

# Initialize app
Config.init_app()

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/copyright-policies', methods=['GET'])
def get_copyright_policies():
    """Get copyright policy comparison"""
    return jsonify(CopyrightPolicy.get_comparison())


@app.route('/api/platform-info/<platform>', methods=['GET'])
def get_platform_info(platform):
    """Get information about a specific platform"""
    if platform.lower() == 'youtube':
        return jsonify(CopyrightPolicy.YOUTUBE)
    elif platform.lower() == 'dtube':
        return jsonify(CopyrightPolicy.DTUBE)
    else:
        return jsonify({'error': 'Invalid platform'}), 400


@app.route('/api/youtube/authenticate', methods=['POST'])
def youtube_authenticate():
    """Authenticate with YouTube"""
    try:
        youtube_uploader.authenticate()
        channel_info = youtube_uploader.get_channel_info()
        return jsonify({
            'success': True,
            'channel': channel_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/youtube/channel-info', methods=['GET'])
def youtube_channel_info():
    """Get YouTube channel information"""
    try:
        info = youtube_uploader.get_channel_info()
        if info:
            return jsonify({'success': True, 'channel': info})
        else:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_video():
    """
    Upload video to selected platform(s)

    Form data:
        - video: Video file
        - title: Video title
        - description: Video description
        - tags: Comma-separated tags
        - platforms: JSON array of platforms ['youtube', 'dtube', or both]
        - privacy: Privacy setting for YouTube (public/private/unlisted)
        - category: YouTube category ID
    """
    # Check if file is present
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    # Get form data
    title = request.form.get('title', 'Untitled Video')
    description = request.form.get('description', '')
    tags_str = request.form.get('tags', '')
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
    platforms = json.loads(request.form.get('platforms', '["youtube"]'))
    privacy = request.form.get('privacy', 'private')
    category = request.form.get('category', '22')

    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    results = []

    # Upload to selected platforms
    try:
        if 'youtube' in platforms:
            print("Uploading to YouTube...")
            result = youtube_uploader.upload_video(
                file_path=filepath,
                title=title,
                description=description,
                category=category,
                privacy=privacy,
                tags=tags,
                check_copyright=False  # Warnings shown in UI
            )
            results.append(result)

        if 'dtube' in platforms:
            print("Uploading to DTube...")
            result = dtube_uploader.upload_video(
                file_path=filepath,
                title=title,
                description=description,
                tags=tags,
                check_copyright=False  # Warnings shown in UI
            )
            results.append(result)

        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        # Clean up on error
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze-copyright', methods=['POST'])
def analyze_copyright():
    """
    Analyze video for copyright concerns and provide platform recommendations

    This is a placeholder for future ML-based copyright detection
    """
    data = request.json
    video_description = data.get('description', '')
    has_music = data.get('has_music', False)
    has_other_content = data.get('has_other_content', False)

    recommendations = {
        'youtube_risk': 'medium',
        'dtube_risk': 'low',
        'recommendations': []
    }

    if has_music:
        recommendations['youtube_risk'] = 'high'
        recommendations['recommendations'].append(
            'Video contains music - high risk on YouTube. Consider YouTube Audio Library or licensed music.'
        )

    if has_other_content:
        recommendations['youtube_risk'] = 'high'
        recommendations['recommendations'].append(
            'Video contains third-party content - may be blocked on YouTube.'
        )

    if not has_music and not has_other_content:
        recommendations['youtube_risk'] = 'low'
        recommendations['recommendations'].append(
            'Original content - safe for both platforms.'
        )

    recommendations['recommendations'].append(
        f'DTube has no automated scanning but you remain legally liable.'
    )

    return jsonify(recommendations)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Video Uploader API'})


if __name__ == '__main__':
    print("="*60)
    print("Dual-Platform Video Uploader")
    print("NoblePort Systems")
    print("="*60)
    print(f"Upload folder: {Config.UPLOAD_FOLDER}")
    print(f"Max file size: {Config.MAX_FILE_SIZE / (1024*1024*1024):.2f} GB")
    print("="*60)

    app.run(debug=True, host='0.0.0.0', port=5000)
