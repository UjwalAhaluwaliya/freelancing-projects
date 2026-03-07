# AI Parental Control System - Backend

FastAPI backend for a mobile-based AI Parental Control System using MongoDB.

## Prerequisites

- Python 3.10–3.12 (3.13 may require Rust for some dependencies)
- MongoDB (local or remote instance)

## Setup

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:

   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):

   Create a `.env` file in the `backend` directory:

   ```
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=parent_monitoring
   JWT_SECRET_KEY=your-super-secret-key-change-in-production
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ```

## Run the Server

From the **project root** (`Parent_Monitoring_System`):

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Or from the `backend` directory:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- **API docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## API Endpoints

### Auth (existing)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register-parent` | Register a new parent |
| POST | `/login-parent` | Login as parent |
| POST | `/add-child` | Add a child (requires parent JWT) |
| POST | `/login-child` | Login as child |

### Screen Time Control
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/set-limit` | Set daily screen time limit (requires parent JWT) |
| GET | `/usage/{child_id}` | Get usage time for a child (requires parent JWT) |
| POST | `/log-usage` | Log usage; creates alert if limit exceeded (requires parent JWT) |

### Alerts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/alerts/{child_id}` | Get alerts for a child (requires parent JWT) |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports/{child_id}` | Get report: daily usage, blocked attempts, screen time (requires parent JWT) |

### Safety
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/check-url` | Check URL safety; blocks and creates alert if unsafe (requires parent JWT) |
| POST | `/detect-toxic` | Detect toxic words in text; creates alert if toxic (requires parent JWT) |

### Example Requests

**Register Parent**
```json
POST /register-parent
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Login Parent**
```json
POST /login-parent
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Add Child** (requires `Authorization: Bearer <parent_token>`)
```json
POST /add-child
{
  "name": "Jane",
  "age": 10,
  "password": "childpass123"
}
```

**Login Child**
```json
POST /login-child
{
  "child_id": "<child_id_from_add_child_response>",
  "password": "childpass123"
}
```

**Set Screen Time Limit**
```json
POST /set-limit
Authorization: Bearer <parent_token>
{
  "child_id": "<child_id>",
  "daily_limit": 120
}
```

**Check URL**
```json
POST /check-url
Authorization: Bearer <parent_token>
{
  "url": "example.com",
  "child_id": "<child_id>"
}
// Response: {"allowed": true} or {"allowed": false}
```

**Detect Toxic Message**
```json
POST /detect-toxic
Authorization: Bearer <parent_token>
{
  "text": "You are stupid",
  "child_id": "<child_id>"
}
// Response: {"toxic": true} or {"toxic": false}
```

## MongoDB Collections

- **parents**: id, name, email, password (hashed)
- **children**: id, parent_id, name, age, password (hashed)
- **usage_logs**: child_id, date, usage_time
- **alerts**: child_id, message, timestamp, alert_type (blocked_website | toxic_message | screen_time_exceeded)
- **screen_time**: child_id, parent_id, daily_limit
