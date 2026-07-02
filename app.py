#!/usr/bin/env python3
"""
Flask API wrapper for SpencerDev M3U8 Extractor
Deployable on Render
"""

from flask import Flask, jsonify, request
import re
from extract_movies import extract_all_m3u8

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({
        "service": "SpencerDev M3U8 Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "/": "API information",
            "/health": "Health check",
            "/extract": "Extract M3U8 links (GET/POST)",
            "/extract/<movie_id>": "Extract M3U8 links by movie ID"
        },
        "usage": {
            "GET": "/extract?movie_id=254",
            "POST": "/extract with JSON body: {\"movie_id\": \"254\"}",
            "GET": "/extract/254"
        }
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "m3u8-extractor"}), 200


@app.route('/extract', methods=['GET', 'POST'])
def extract():
    """Extract M3U8 links from movie ID or URL"""
    movie_id = None
    
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        movie_id = data.get('movie_id') or data.get('url')
    else:
        movie_id = request.args.get('movie_id') or request.args.get('url')
    
    if not movie_id:
        return jsonify({
            "error": "Missing movie_id parameter",
            "usage": "?movie_id=254 or POST {\"movie_id\": \"254\"}"
        }), 400
    
    # Extract movie ID from URL if full URL provided
    match = re.search(r"/movie/(\d+)", str(movie_id))
    movie_id = match.group(1) if match else str(movie_id).strip()
    
    if not movie_id.isdigit():
        return jsonify({"error": "Invalid movie ID format"}), 400
    
    try:
        links = extract_all_m3u8(movie_id)
        return jsonify({
            "movie_id": movie_id,
            "links_found": len(links),
            "m3u8_links": links
        })
    except Exception as e:
        return jsonify({
            "error": "Extraction failed",
            "details": str(e)
        }), 500


@app.route('/extract/<movie_id>', methods=['GET'])
def extract_by_id(movie_id):
    """Extract M3U8 links by movie ID in URL path"""
    # Extract movie ID from URL if full URL provided
    match = re.search(r"/movie/(\d+)", movie_id)
    movie_id = match.group(1) if match else movie_id.strip()
    
    if not movie_id.isdigit():
        return jsonify({"error": "Invalid movie ID format"}), 400
    
    try:
        links = extract_all_m3u8(movie_id)
        return jsonify({
            "movie_id": movie_id,
            "links_found": len(links),
            "m3u8_links": links
        })
    except Exception as e:
        return jsonify({
            "error": "Extraction failed",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    # For local testing
    app.run(host='0.0.0.0', port=5000, debug=True)
