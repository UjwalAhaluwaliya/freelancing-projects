# AI Parental Control System - Run Instructions

## Prerequisites

- Python 3.10+ with venv
- Flutter SDK
- MongoDB running locally or remotely

---

## 1. Backend

```bash
# From project root (Parent_Monitoring_System)
uvicorn backend.main:app --reload --port 8001
```

- API: http://localhost:8001
- Docs: http://localhost:8001/docs

---

## 2. Parent App

```bash
cd parent_app
flutter run
```

**First-time setup:**
1. Register a parent: Open http://localhost:8001/docs → POST /register-parent with `{"name":"...","email":"...","password":"..."}`
2. Login in the app with email and password
3. Add children from the Children screen
4. View alerts and reports

**API config:** Edit `lib/config/api_config.dart` for your environment:
- Android Emulator: `http://10.0.2.2:8001`
- Physical Device: `http://YOUR_IP_ADDRESS:8001`

---

## 3. Child App

```bash
cd child_app
flutter run
```

**First-time setup:**
1. Get Child ID from Parent app (after adding a child)
2. Login with Child ID and the password set when adding the child
3. Use the browser, view usage, etc.

**API config:** Edit `lib/config/api_config.dart`:
- Android Emulator: `http://10.0.2.2:8001`
- Physical Device: `http://YOUR_IP_ADDRESS:8001`

---

## API Integration Summary

### Parent App
| Feature        | API                    | Auth   |
|----------------|------------------------|--------|
| Login          | POST /login-parent     | No     |
| Get Children   | GET /children         | JWT    |
| Add Child      | POST /add-child       | JWT    |
| Alerts         | GET /alerts/{child_id}| JWT    |
| Reports        | GET /reports/{child_id}| JWT    |

### Child App
| Feature        | API                    | Auth   |
|----------------|------------------------|--------|
| Login          | POST /login-child      | No     |
| Dashboard      | GET /child/dashboard   | JWT    |
| Check URL      | POST /child/check-url  | JWT    |
| Usage          | GET /child/usage       | JWT    |

All protected APIs send: `Authorization: Bearer TOKEN`
