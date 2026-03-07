# Attendance Monitoring App

Production-ready Attendance Management System with role-based backend APIs and a modern Expo mobile app.

## Tech Stack

- Backend: Node.js, Express, MongoDB, Mongoose, JWT, bcrypt
- Mobile: React Native (Expo), React Navigation, Axios, NativeWind

## Project Structure

```text
Attendance_Monitoring_App/
  backend/
    config/
    controllers/
    middleware/
    models/
    routes/
    services/
    utils/
    scripts/
    server.js
  mobile/
    components/
    screens/
    navigation/
    services/
    utils/
    context/
    App.js
```

## Backend Setup

1. Open terminal in `backend`
2. Install dependencies:

```bash
npm install
```

3. Create `.env` from `.env.example`
4. Start server:

```bash
npm start
```

5. Optional seed data:

```bash
npm run seed
```

Backend base URL: `http://localhost:5000/api`

### Seed Credentials

- Admin: `admin@college.edu` / `admin123`
- Faculty: `faculty@college.edu` / `faculty123`
- Student: `student1@college.edu` / `student123`

## Mobile Setup

1. Open terminal in `mobile`
2. Install dependencies:

```bash
npm install
```

3. Update backend URL in `mobile/utils/config.js`
   - Emulator/real device should point to your machine IP, not `localhost`
4. Start Expo:

```bash
npx expo start
```

## API Summary

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`

### Admin
- `POST /api/admin/students`
- `POST /api/admin/faculty`
- `POST /api/admin/classes`
- `POST /api/admin/subjects`
- `GET /api/admin/reports/overview`
- `POST /api/admin/announcements`

### Faculty
- `GET /api/faculty/classes`
- `GET /api/faculty/classes/:classId/students`
- `POST /api/faculty/attendance`
- `PUT /api/faculty/attendance/update`
- `GET /api/faculty/attendance/class`

### Student
- `GET /api/student/attendance/me`
- `POST /api/student/leave-request`

### Notifications
- `GET /api/notifications`
- `POST /api/notifications`
- `PATCH /api/notifications/:id/read`

### Reports
- `GET /api/reports/attendance/export?format=csv|pdf`

## Features Delivered

- JWT authentication with bcrypt password hashing
- Role-based access control (admin, faculty, student)
- Attendance marking + editing + duplicate prevention
- Attendance percentage calculation (overall and subject-wise)
- Low attendance alert notifications (<75%)
- Admin announcements
- CSV/PDF attendance export
- Modern card-based mobile UI with gradient headers

## Production Notes

- Use strong `JWT_SECRET` in production
- Add request validation layer (`joi`/`zod`) before deployment
- Add rate limiting + API logging pipeline
- Move secrets to managed secret store
- Add CI with tests and linting
