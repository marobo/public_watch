# Public Watch — Community Issue Reports

Django project for the AI-powered community daily-life issue reporting system.

## Setup (first-time clone)

```bash
git clone <your-repo-url>
cd public_watch
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

- **Admin:** http://127.0.0.1:8000/admin/
- **Root:** http://127.0.0.1:8000/
- **Media:** served at `/media/` in development

## Project structure

- `public_watch/` — project package (settings, urls, wsgi/asgi)
- `reports/` — app for community issue reports (models/API added in later tasks)

See `cursor_tasks.md` and `master_plan.md` for the full plan.
