# SpencerDev M3U8 Extractor API

A Flask API service that extracts M3U8 streaming links from SpencerDev servers. Deployable on Render.

## Original Repository
https://github.com/srtfile/servers.spencerdevs.xyz/

## Features

- 🚀 RESTful API for M3U8 extraction
- 🔐 Chrome impersonation with curl_cffi
- 🌐 Rotating residential proxy support
- 🔄 Automatic proxy fallback
- 📦 Ready for Render deployment

## Deploy to Render

### One-Click Deploy

1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will auto-detect the `render.yaml` configuration
6. Click "Create Web Service"

### Manual Deploy

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Name**: spencerdev-m3u8-extractor
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Instance Type**: Free (or paid for better performance)

## API Endpoints

### `GET /`
Returns API information and available endpoints.

```bash
curl https://your-app.onrender.com/
```

### `GET /health`
Health check endpoint.

```bash
curl https://your-app.onrender.com/health
```

### `GET /extract?movie_id=<id>`
Extract M3U8 links by movie ID.

```bash
curl "https://your-app.onrender.com/extract?movie_id=254"
```

### `POST /extract`
Extract M3U8 links via POST request.

```bash
curl -X POST https://your-app.onrender.com/extract \
  -H "Content-Type: application/json" \
  -d '{"movie_id": "254"}'
```

### `GET /extract/<movie_id>`
Extract M3U8 links with movie ID in URL path.

```bash
curl https://your-app.onrender.com/extract/254
```

## Response Format

```json
{
  "movie_id": "254",
  "links_found": 5,
  "m3u8_links": [
    "https://example.com/stream1.m3u8",
    "https://example.com/stream2.m3u8"
  ]
}
```

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Test Locally

```bash
# Get API info
curl http://localhost:5000/

# Extract links
curl "http://localhost:5000/extract?movie_id=254"
```

## Command Line Usage

The original command-line script is still available:

```bash
python extract_movies.py 254
# or
python extract_movies.py --url "https://spencerdevs.xyz/movie/254"
```

## Environment Variables

No additional environment variables required. Proxy credentials are embedded in the code.

## Technical Details

- **Framework**: Flask with Gunicorn
- **Python Version**: 3.11
- **Key Dependencies**:
  - `curl_cffi`: Chrome impersonation for bypassing detection
  - `cryptography`: AES decryption for snoopdog payload
  - `flask`: Web API framework
  - `gunicorn`: Production WSGI server

## Proxy Configuration

The service uses rotating residential proxies to avoid rate limiting. Proxies are configured in `extract_movies.py`.

## License

MIT