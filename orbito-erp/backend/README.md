# Orbito ERP Backend

## Setup

1. Create env file:
   - Copy `.env.example` to `.env`
   - Set required keys:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `GEMINI_API_KEY`
     - `N8N_WEBHOOK_URL`
   - Minimal security hardening:
     - keep `APP_ENV=development` for local
     - for production use `APP_ENV=production`
     - in production: set strict `CORS_ORIGINS` and strong `JWT_SECRET_KEY` (32+ chars)
   - Optional retry tuning:
     - `N8N_REQUEST_TIMEOUT_SECONDS`
     - `N8N_MAX_RETRIES`
     - `N8N_RETRY_BASE_DELAY_SECONDS`
2. Create virtual env:
   - `python -m venv .venv`
3. Install dependencies:
   - `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

## Run

- `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`

## Test

- `.\.venv\Scripts\python.exe -m pytest -q`

## Database (Supabase)

1. Run migration SQL:
   - `supabase/migrations/20260303_001_init_schema.sql`
2. Run seed SQL:
   - `supabase/seed.sql`
3. Reference:
   - `supabase/README.md`

## n8n Workflow Import

1. Open n8n UI.
2. Import file:
   - `n8n/workflows/resume_shortlist_workflow.json`
3. Add real email/task nodes after `Shortlist Action Placeholder`.
