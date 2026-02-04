# Public Watch — Community Issue Reports

Django project for an AI-powered community daily-life issue reporting system. Users upload images of issues (e.g. potholes, waste, hazards); the system stores reports, optional GPS from EXIF, and mock AI classification. A simple frontend supports upload and map-based location selection.

## Project overview

- **Backend:** Django 4+, Django REST Framework, SQLite (dev).
- **App:** `reports` — models `CommunityIssue`, REST API for upload/location/status, admin, categories, AI integration layer (mock by default).
- **Frontend:** Plain HTML/CSS/JS upload page with Leaflet map for location.
- **Production readiness:** Settings use environment variables; static/media and logging are configured; no auth in this phase.

## Local setup

1. **Clone and enter the project:**
   ```bash
   git clone <your-repo-url>
   cd public_watch
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional for local dev):**
   - `SECRET_KEY` — Django secret (default: dev-only insecure key).
   - `DEBUG` — Set to `True` or `1` for debug mode (default: `False`).
   - `ALLOWED_HOSTS` — Comma-separated hosts (default: `localhost,127.0.0.1`).

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin):**
   ```bash
   python manage.py createsuperuser
   ```

## Run the server

```bash
python manage.py runserver
```

- **Root:** http://127.0.0.1:8000/
- **Report upload page:** http://127.0.0.1:8000/report/
- **Admin:** http://127.0.0.1:8000/admin/
- **Media files:** Served at `/media/` when `DEBUG=True`.

## Seed data

Create sample `CommunityIssue` records for demo/development:

```bash
python manage.py seed_issues
```

This creates at least 10 issues with varied categories, severity, status, and optional coordinates.

## API endpoint summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/issues/` | List issues (id, image_url, status, created_at, latitude, longitude). |
| `POST` | `/api/issues/` | Upload image (multipart/form-data, field `image`). Creates a `CommunityIssue`, runs GPS extraction and AI analysis, returns id, image_url, status, created_at. |
| `PATCH`| `/api/issues/{id}/location/` | Update location. Body: `{"latitude": number, "longitude": number}`. |
| `GET`  | `/api/issues/{id}/status/` | Get issue status (id, status, created_at). |
| `PATCH`| `/api/issues/{id}/status/` | Update status. Body: `{"status": "review" \| "fixed"}`. Allowed: `new` → `review`, `review` → `fixed`. |

## Project structure

- `public_watch/` — Project package (settings, urls, wsgi/asgi).
- `reports/` — App: models, admin, serializers, API views, categories, `services/` (ai_analyzer, ai_mock), `utils` (GPS extraction), templates, tests.
- `media/` — User-uploaded files (created at runtime).
- `staticfiles/` — Collected static files (after `collectstatic`).

See `cursor_tasks.md` and `master_plan.md` for the full plan.
