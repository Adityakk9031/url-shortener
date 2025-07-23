
from flask import Flask, request, jsonify, redirect
from app.models import save_url_mapping, get_original_url, increment_clicks, get_url_stats
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    
    if not original_url or not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    save_url_mapping(short_code, original_url)
    
    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    })

@app.route('/<short_code>')
def redirect_url(short_code):
    mapping = get_original_url(short_code)
    if not mapping:
        return jsonify({"error": "Short URL not found"}), 404

    increment_clicks(short_code)
    return redirect(mapping['url'])

@app.route('/api/stats/<short_code>')
def stats(short_code):
    mapping = get_url_stats(short_code)
    if not mapping:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "url": mapping['url'],
        "clicks": mapping['clicks'],
        "created_at": mapping['created_at'].isoformat()
    })
