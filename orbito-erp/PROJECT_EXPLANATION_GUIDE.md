# Orbito ERP - Project Explanation Guide

This document is made for both:
- Non-technical stakeholders (who want simple understanding)
- Technical reviewers/project leads (who want architecture clarity)

---

## 1) Project in One Line

**Orbito ERP** is an AI-enabled HR and ATS platform that helps a company:
- manage employee operations (auth, profiles, leave, notifications),
- manage hiring pipeline (candidates, jobs, applications, interviews),
- use AI for JD generation and resume scoring,
- automate shortlist actions via n8n workflows.

---

## 2) Why This Project Exists

Most HR teams use scattered tools: one for hiring, one for leave, one for notifications, and manual steps for resume shortlisting.

Orbito ERP combines these into one system:
1. HR process management
2. Hiring lifecycle tracking
3. AI-assisted decisions
4. Automation on top (webhooks/workflows)

---

## 3) Core Value (Non-Technical)

If a resume is strong:
1. HR uploads resume (PDF) + job description.
2. AI gives a match score.
3. If score is above threshold (for example 70), system auto-triggers workflow.
4. HR gets notification, shortlist process starts faster.

This reduces manual screening time and keeps hiring consistent.

---

## 4) Tech Stack

### Backend
- **FastAPI** (Python API layer)
- **Supabase/Postgres** (database)
- **JWT Authentication** (secure login token)
- **Role-based access** (`admin`, `hr`, `employee`)
- **Google Gemini (google-genai SDK)** for AI generation/scoring
- **n8n Webhook** integration for automation

### Frontend
- **React + Vite**
- **React Router** for role-based routes
- **Axios** for API communication

### Automation
- **n8n** workflow with importable JSON

---

## 5) System Modules

### A) Authentication & Access
- User registration/login
- JWT tokens
- Role restricted APIs

### B) Profile & Employee Layer
- Employee profile records
- Role + department mapping

### C) Leave Management
- Employee leave apply
- HR/Admin approve/reject
- Status tracking + notification
- Approval gives achievement points

### D) Notifications
- Real-time-ish notifications stored in DB
- Read/unread tracking

### E) ATS (Hiring Pipeline)
- Candidate create/update/delete
- Job create/update/delete
- Application tracking by stage:
  - `applied -> screening -> interview -> offer -> hired/rejected`
- Invalid transitions blocked
- Hired flow creates employee profile (if needed) + welcome notification

### F) AI Integration
- AI Job Description Generator
- Resume scoring (text input)
- Resume scoring (PDF upload)
- Policy chatbot (n8n webhook + AI fallback)

### G) Automation Layer
- Score above threshold triggers shortlist webhook
- n8n validates payload and executes downstream actions

---

## 6) End-to-End Flow (Simple Story)

### Hiring Example
1. HR creates candidate and job.
2. HR creates application.
3. HR moves stage forward.
4. HR uploads candidate resume PDF and job description.
5. AI returns match score + recommendation.
6. If score >= threshold:
   - shortlist webhook is triggered,
   - HR gets notification,
   - n8n workflow executes.

### Leave Example
1. Employee applies leave.
2. HR approves.
3. Employee gets notification.
4. Employee receives +5 achievement points.

---

## 7) Architecture (Technical but Clear)

Client (React) -> FastAPI -> Supabase DB  
Client (React) -> FastAPI -> Gemini API  
FastAPI -> n8n Webhook (automation trigger)  
n8n -> response back / next automation steps

Key design points:
- Config-driven env settings
- Input validation via Pydantic schemas
- Retry/backoff for n8n webhook failures
- Payload contract validation before sending automation events

---

## 8) Security & Reliability

Implemented:
- JWT auth + role checks
- Environment-based secrets
- CORS configurable by env
- n8n retries with exponential backoff + jitter
- Payload schema validation

For academic use:
- minimal hardening included
- production-grade hardening can be extended later

---

## 9) Data Layer (Supabase)

Project includes:
- migration SQL for full schema creation
- seed SQL for demo users and demo records

This means project setup is reproducible for evaluator/demo.

---

## 10) Demo Credentials (Seed)

- `admin@orbito.local` / `Admin@123`
- `hr@orbito.local` / `Hr@12345`
- `employee@orbito.local` / `Emp@12345`

Important:
- Domain is **orbito.local** (not `orbit.local`).

---

## 11) What to Show in Demo

1. Login as HR.
2. Show dashboard.
3. Create candidate/job/application.
4. Move application stage.
5. Score resume (PDF).
6. Show shortlist trigger response.
7. Show n8n execution.
8. Show notifications page.
9. Login as employee and show leave + points.
10. Login as admin and show user management.

---

## 12) Current Project Status

Strongly complete for academic demo:
- ERP backend flows
- ATS lifecycle
- AI scoring + PDF upload
- n8n integration and importable workflow
- modern frontend dashboards/pages

---

## 13) If Project Lead Asks "What is Unique?"

Answer:
1. Combines HR + ATS + AI + automation in one flow.
2. Resume scoring supports PDF upload, not only plain text.
3. Workflow reliability handled with retries and validation.
4. Reproducible setup via migration + seed + workflow JSON.

---

## 14) Quick Technical Handover Notes

- Backend folder: `backend/`
- Frontend folder: `frontend/`
- Supabase SQL:
  - `backend/supabase/migrations/20260303_001_init_schema.sql`
  - `backend/supabase/seed.sql`
- n8n import:
  - `backend/n8n/workflows/resume_shortlist_workflow.json`
- API docs:
  - `http://localhost:8000/docs`

---

If needed, this guide can be converted into:
- 1-page PPT summary
- viva script (2-5 min)
- project report chapter format
