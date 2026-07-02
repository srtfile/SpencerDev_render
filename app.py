#!/usr/bin/env python3
"""
Flask API wrapper for SpencerDev M3U8 Extractor
Deployable on Render with Web Interface
"""

from flask import Flask, jsonify, request, render_template_string
import re
from extract_movies import extract_all_m3u8

app = Flask(__name__)

# HTML Template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpencerDev M3U8 Extractor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
            color: #667eea;
        }
        .loading.active {
            display: block;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .results {
            display: none;
            margin-top: 30px;
        }
        .results.active {
            display: block;
        }
        .results h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .link-item {
            background: #f8f9fa;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            word-break: break-all;
            font-size: 0.85em;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .link-text {
            flex: 1;
            margin-right: 10px;
        }
        .copy-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            white-space: nowrap;
        }
        .copy-btn:hover {
            background: #5568d3;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #c33;
            margin-top: 20px;
        }
        .success {
            background: #efe;
            color: #3c3;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3c3;
            margin-top: 20px;
        }
        .example {
            background: #f0f7ff;
            padding: 10px;
            border-radius: 8px;
            margin-top: 8px;
            font-size: 0.85em;
            color: #666;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 0.85em;
        }
        .api-link {
            color: #667eea;
            text-decoration: none;
        }
        .api-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 M3U8 Extractor</h1>
        <p class="subtitle">Extract streaming links from SpencerDev servers</p>
        
        <form id="extractForm">
            <div class="input-group">
                <label for="movieId">Movie ID or TMDB ID</label>
                <input 
                    type="text" 
                    id="movieId" 
                    name="movieId" 
                    placeholder="e.g., 254, 11, 550"
                    required
                >
                <div class="example">
                    💡 <strong>Examples:</strong> 254, 11, 550<br>
                    Or full URL: https://spencerdevs.xyz/movie/254
                </div>
            </div>
            
            <button type="submit" id="submitBtn">🔍 Extract Links</button>
        </form>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Extracting M3U8 links... This may take 10-30 seconds</p>
        </div>

        <div class="results" id="results"></div>

        <div class="footer">
            <p>API Endpoint: <a href="/api" class="api-link">/api</a></p>
            <p>Made with ❤️ for SpencerDev community</p>
        </div>
    </div>

    <script>
        const form = document.getElementById('extractForm');
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        const submitBtn = document.getElementById('submitBtn');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const movieId = document.getElementById('movieId').value.trim();
            
            // Clear previous results
            results.innerHTML = '';
            results.classList.remove('active');
            loading.classList.add('active');
            submitBtn.disabled = true;

            try {
                const response = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ movie_id: movieId })
                });

                const data = await response.json();

                loading.classList.remove('active');
                results.classList.add('active');
                submitBtn.disabled = false;

                if (response.ok && data.m3u8_links && data.m3u8_links.length > 0) {
                    results.innerHTML = `
                        <div class="success">
                            ✅ Found ${data.links_found} streaming link(s) for Movie ID: ${data.movie_id}
                        </div>
                        <h2>📺 Streaming Links</h2>
                        ${data.m3u8_links.map((link, index) => `
                            <div class="link-item">
                                <div class="link-text">
                                    <strong>Link ${index + 1}:</strong><br>
                                    <code>${link}</code>
                                </div>
                                <button class="copy-btn" onclick="copyToClipboard('${link.replace(/'/g, "\\'")}', this)">
                                    📋 Copy
                                </button>
                            </div>
                        `).join('')}
                    `;
                } else {
                    results.innerHTML = `
                        <div class="error">
                            ❌ ${data.error || 'No streaming links found. The movie might not be available or the ID is incorrect.'}
                        </div>
                    `;
                }
            } catch (error) {
                loading.classList.remove('active');
                results.classList.add('active');
                submitBtn.disabled = false;
                
                results.innerHTML = `
                    <div class="error">
                        ❌ Error: ${error.message || 'Failed to extract links. Please try again.'}
                    </div>
                `;
            }
        });

        function copyToClipboard(text, button) {
            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.textContent;
                button.textContent = '✓ Copied!';
                button.style.background = '#4caf50';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.style.background = '#667eea';
                }, 2000);
            }).catch(err => {
                alert('Failed to copy: ' + err);
            });
        }
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    """Render the web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api')
def api_info():
    """API documentation endpoint"""
    return jsonify({
        "service": "SpencerDev M3U8 Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "/": "Web interface",
            "/api": "API information",
            "/health": "Health check",
            "/api/extract": "Extract M3U8 links (GET/POST)",
            "/api/extract/<movie_id>": "Extract M3U8 links by movie ID"
        },
        "usage": {
            "GET": "/api/extract?movie_id=254",
            "POST": "/api/extract with JSON body: {\"movie_id\": \"254\"}",
            "GET": "/api/extract/254"
        }
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "m3u8-extractor"}), 200


@app.route('/api/extract', methods=['GET', 'POST'])
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


@app.route('/api/extract/<movie_id>', methods=['GET'])
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
