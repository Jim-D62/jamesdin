# Plan: Flask Weather App with City Search & Icons

Flask app: user enters city → server calls OpenWeatherMap API → displays weather with icons on a Bootstrap page.

## Steps

### Phase 1 — Project Setup
1. Rename `flask.py` → `app.py` (avoids shadowing flask module)
2. Create `requirements.txt` with `flask` and `requests`
3. Create folders: `templates/`, `static/css/`

### Phase 2 — Backend
4. `GET /` route renders `index.html`
5. `POST /weather` route: reads city from form, calls OpenWeatherMap API (`/data/2.5/weather`), extracts temp/description/humidity/wind/icon, renders template with data or error
6. API key via env var `OPENWEATHER_API_KEY`

### Phase 3 — Frontend
7. `templates/index.html`: Bootstrap 5 CDN, centered card with form, results card with icon/temp/description/humidity/wind, error alert
8. `static/css/style.css`: background color, card shadow, centering

## Relevant Files
- `c:\Users\jamesdin\flask.py` → rename to `app.py`
- `c:\Users\jamesdin\templates\index.html` (new)
- `c:\Users\jamesdin\static\css\style.css` (new)
- `c:\Users\jamesdin\requirements.txt` (new)

## Verification
1. `pip install -r requirements.txt`
2. Set env var: `$env:OPENWEATHER_API_KEY="your_key"`
3. `python app.py` — server on 127.0.0.1:5000
4. Test valid city (London) — confirm weather + icon display
5. Test invalid city — confirm error message
6. Verify icon images load

## Decisions
- Rename flask.py to app.py (required to avoid import shadow)
- Server-side rendering (keeps API key secret)
- Metric units (°C, m/s)
- No database, stateless
- OpenWeatherMap free tier (1000 calls/day)
- Bootstrap 5 for UI
