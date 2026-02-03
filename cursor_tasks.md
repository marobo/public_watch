# Community Daily-Life Issue Reporting System

This repository is built step-by-step using **Cursor AI tasks**.  
Each task has its own README-style section so it can be executed **one at a time** safely.

---

## TASK 1 — Project Bootstrap

### Objective
Initialize a Django project with REST support and media uploads.

### Cursor Prompt
```
Create a new Django project named "community_issues".

Requirements:
- Django 4+
- Django REST Framework
- Project named "public_watch"
- App named "reports"
- Enable media file uploads
- Use SQLite for development

Deliverables:
- Django project structure
- settings.py configured for MEDIA_ROOT and MEDIA_URL
- reports app created and registered
```

### Expected Outcome
- Project runs with `python manage.py runserver`
- Media uploads work locally

---

## TASK 2 — Database Models

### Objective
Create the core data model for community issue reporting.

### Cursor Prompt
```
Inside the "reports" app, create database models for community issue reporting.

Model: CommunityIssue
Fields:
- image (ImageField, upload to "issues/")
- main_category (CharField, max_length=50)
- sub_category (CharField, max_length=100)
- severity (CharField, choices: low, medium, high)
- risks (JSONField)
- description (TextField)
- latitude (FloatField, nullable)
- longitude (FloatField, nullable)
- status (choices: new, review, fixed)
- created_at (DateTimeField, auto_now_add=True)

Generate and apply migrations.
```

### Expected Outcome
- Database migrated
- Model visible in Django shell

---

## TASK 3 — Admin Panel

### Objective
Enable admins to review and manage reported issues.

### Cursor Prompt
```
Register the CommunityIssue model in Django admin.

Admin requirements:
- List display: id, main_category, severity, status, created_at
- Filters: main_category, severity, status
- Search: description, sub_category
```

### Expected Outcome
- Issues visible in `/admin`
- Easy filtering and review

---

## TASK 4 — Image Upload API

### Objective
Allow users to submit issues via image upload.

### Cursor Prompt
```
Create a REST API endpoint to upload an image and create a CommunityIssue.

Endpoint:
POST /api/issues/

Behavior:
- Accept image upload (multipart/form-data)
- Save image to database
- Create issue with status = "new"
- Return JSON with issue ID and image URL

Use Django REST Framework.
```

### Expected Outcome
- API accepts images
- Issue created successfully

---

## TASK 5 — GPS Extraction Utility

### Objective
Automatically extract location data from images when available.

### Cursor Prompt
```
Create a Python utility function to extract GPS coordinates from an uploaded image using EXIF metadata.

Requirements:
- Use Pillow or exifread
- Return (latitude, longitude) or (None, None)
- Handle images without GPS safely

Integrate this utility into the image upload API.
```

### Expected Outcome
- GPS stored if available
- No crashes on missing EXIF

---

## TASK 6 — AI Classification (Mock)

### Objective
Simulate AI analysis before real integration.

### Cursor Prompt
```
Create a mock AI classification service for image analysis.

Function: analyze_image(image_path)

Return fixed JSON structure:
{
  "main_category": "Roads & Transport",
  "sub_category": "Pothole",
  "severity": "high",
  "risks": ["safety"],
  "description": "Visible pothole causing unsafe driving conditions."
}

Integrate this into the upload API and save results into CommunityIssue.
```

### Expected Outcome
- AI fields populated automatically

---

## TASK 7 — Real AI Integration Layer

### Objective
Prepare a clean layer for real AI vision models.

### Cursor Prompt
```
Create a service layer for AI image analysis.

Requirements:
- Separate file: services/ai_analyzer.py
- Function: analyze_image(image_path)
- Accept image + prompt
- Return structured JSON

Do NOT hardcode API keys.
Leave TODO comments for AI provider configuration.
```

### Expected Outcome
- AI logic isolated
- Easy provider swap later

---

## TASK 8 — Category Framework

### Objective
Standardize issue categories across the system.

### Cursor Prompt
```
Define a centralized category configuration for community issues.

Categories:
1. Roads & Transport
2. Water & Sanitation
3. Waste & Environment
4. Public Facilities
5. Safety & Hazards
6. Housing & Neighborhood
7. Accessibility & Inclusion
8. Other

Create:
- categories.py
- Use this config in AI prompt generation
```

### Expected Outcome
- Single source of truth for categories

---

## TASK 9 — Frontend Upload Page

### Objective
Provide a simple UI for community reporting.

### Cursor Prompt
```
Create a simple HTML frontend page for image upload.

Requirements:
- Image upload form
- Submit via JavaScript fetch()
- Display analysis results:
  - Category
  - Severity
  - Description
  - Location (if available)

Use plain HTML, CSS, and vanilla JavaScript.
```

### Expected Outcome
- One-page reporting flow

---

## TASK 10 — Map Integration

### Objective
Allow manual location selection when GPS is missing.

### Cursor Prompt
```
Integrate a map view using Leaflet.js.

Requirements:
- Show marker if latitude/longitude exists
- Allow user to manually select location if GPS missing
- Save selected location back to CommunityIssue via API
```

### Expected Outcome
- Accurate issue locations

---

## TASK 11 — Status Workflow

### Objective
Track issue resolution lifecycle.

### Cursor Prompt
```
Add status update API endpoint.

Endpoint:
PATCH /api/issues/{id}/status/

Allowed transitions:
- new → review
- review → fixed

Validate transitions and return updated issue JSON.
```

### Expected Outcome
- Controlled issue lifecycle

---

## TASK 12 — Seed Data & Tests

### Objective
Ensure reliability and demo readiness.

### Cursor Prompt
```
Create sample seed data with:
- Different categories
- Different severity levels
- With and without GPS

Add basic tests for:
- Image upload
- AI analysis integration
- GPS extraction
```

### Expected Outcome
- Stable demo data
- Confidence in core flows

---

## TASK 13 — Production Readiness

### Objective
Prepare system for real deployment.

### Cursor Prompt
```
Prepare project for production:
- Environment variables for secrets
- Static & media handling
- Database migration readiness
- Basic logging for AI failures
```

### Expected Outcome
- Deployment-ready foundation

---

## Final Note

✔ Run **one task at a time** in Cursor  
✔ Commit after each task  
✔ Replace mock AI only when UI + API are stable

This structure is designed for **government, NGO, or civic-scale systems**.

