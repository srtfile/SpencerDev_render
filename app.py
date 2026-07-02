from flask import Flask, render_template, request, jsonify
import sys
import io
import threading
from extract_movies import extract_all_m3u8

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    movie_id = data.get('movie_id', '')
    
    # Capture print output
    old_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        links = extract_all_m3u8(movie_id)
        output = captured_output.getvalue()
        return jsonify({
            "links": links,
            "output": output
        })
    finally:
        sys.stdout = old_stdout

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)