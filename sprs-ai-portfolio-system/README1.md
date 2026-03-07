# Strategic Portfolio Rationalization System (SPRS)

SPRS is a full-stack portfolio intelligence platform with role-based access control (RBAC):
- `admin`
- `project_manager`
- `employee`

It uses Flask + MongoDB + ML models and a React frontend.

## 1) Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB 6+

## 2) Setup Environment

### Backend

```powershell
cd backend
copy .env.example .env
```

Edit `.env` if needed:
- `MONGO_URI=mongodb://localhost:27017`
- `MONGO_DB_NAME=sprs_db`
- `API_HOST=0.0.0.0`
- `API_PORT=5000`
- `API_DEBUG=true`
- `CORS_ORIGINS=http://localhost:5173`
- `JWT_SECRET_KEY=change-this-in-production`
- `JWT_EXPIRES_HOURS=8`

### Frontend

```powershell
cd frontend
copy .env.example .env
```

Default frontend API base URL:
- `VITE_API_BASE_URL=http://localhost:5000`

## 3) Install Dependencies

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend

```powershell
cd frontend
npm install
```

## 4) Run MongoDB

Option A:

```powershell
net start MongoDB
```

Option B:

```powershell
mongod --dbpath C:\data\db
```

## 5) Seed Data

### Seed projects (50 records)

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python scripts\seed_projects.py
```

### Seed users (RBAC accounts)

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python scripts\seed_users.py
```

Demo accounts:
- Admin: `admin@sprs.local` / `admin123`
- Project Manager: `pm@sprs.local` / `pm123`
- Employee: `employee@sprs.local` / `employee123`

## 6) Run Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python app.py
```

Health check:

```powershell
curl http://localhost:5000/
```

## 7) Run Frontend

```powershell
cd frontend
npm run dev
```

Open: `http://localhost:5173`

## 8) Role Permissions

### Admin
- Can add/delete projects
- Can run portfolio analysis
- Can view dashboard, projects, analytics, recommendations

### Project Manager
- Same operational access as admin for portfolio work
- Cannot manage platform-level admin settings (future extension)

### Employee
- Read-only views:
  - Dashboard
  - Portfolio Table
  - Recommendations
- Cannot add/delete projects
- Cannot run analysis

## 9) API Endpoints

Public:
- `POST /auth/login`
- `GET /`

Authenticated (all roles):
- `GET /projects`
- `GET /project/<id>`
- `GET /recommendations`
- `GET /dashboard_metrics`

Restricted (`admin`, `project_manager`):
- `POST /add_project`
- `DELETE /project/<id>`
- `POST /analyze_portfolio`

## 10) Quick Testing Workflow

1. Login as `admin@sprs.local`.
2. Open Portfolio Table and verify projects.
3. Run analysis from Analytics.
4. Open Recommendations and Dashboard.
5. Logout and login as `employee@sprs.local`.
6. Verify Add Project / Analytics routes are restricted.

Backend validation:

```powershell
cd backend
python -m compileall .
```

Frontend validation:

```powershell
cd frontend
npm run build
```

## Demo Login Credentials

- Admin: `admin@sprs.local` / `admin123`
- Project Manager: `pm@sprs.local` / `pm123`
- Employee: `employee@sprs.local` / `employee123`

(For local development/demo only.)

## Role Difference (SPRS Permissions)

| Capability | Admin | Project Manager | Employee |
|---|---|---|---|
| View Dashboard | Yes | Yes | Yes |
| View Portfolio | Yes | Yes | Yes |
| View Recommendations | Yes | Yes | Yes |
| Add Project | Yes | Yes | No |
| Delete Project | Yes | Yes | No |
| Run Analysis | Yes | Yes | No |
| User/Role Management | Planned | No | No |

Summary:
- Admin: Full control
- Project Manager: Portfolio operations
- Employee: Read-only
