# Attendance Monitoring App - Simple Project Guide

## 1) Project Kya Hai?
Yeh ek **Attendance Management System** hai jisme 3 roles hain:
- `Admin`
- `Faculty`
- `Student`

Is app ka purpose:
- Attendance mark karna
- Attendance report dekhna
- Leave request bhejna/approve karna
- Notifications bhejna

---

## 2) Tech Stack (Easy Language)

### Mobile App (Frontend)
- **React Native (Expo)**: Android app banane ke liye
- **React Navigation**: Screen se screen move karne ke liye
- **Axios**: Backend API call karne ke liye
- **NativeWind (Tailwind style)**: App ka UI sundar aur consistent banane ke liye

### Backend (Server)
- **Node.js**: JavaScript runtime server side
- **Express.js**: API banane ka framework
- **MongoDB**: Data store (database)
- **Mongoose**: MongoDB ke models/schemas manage karne ke liye

### Security
- **JWT (JSON Web Token)**: Login ke baad user verify karne ke liye
- **bcrypt**: Password hash karne ke liye (plain text save nahi hota)
- **Role-based Access**: Har role ko sirf uske allowed features milte hain

---

## 3) Folder Structure

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
    context/
    navigation/
    screens/
    services/
    utils/
    App.js
```

---

## 4) Role-wise Flow

## Admin Flow
1. Login as `admin`
2. Admin dashboard open
3. Admin create kare:
   - Student
   - Faculty
   - Class
   - Subject
4. Faculty assignment subject ke sath set hoti hai
5. Announcements bhej sakta hai
6. Overall analytics dekh sakta hai

## Faculty Flow
1. Login as `faculty`
2. Assigned classes/subjects dikhenge
3. Attendance mark/edit kar sakta hai
4. Class attendance reports dekh sakta hai
5. Student leave requests approve/reject kar sakta hai

## Student Flow
1. Login as `student`
2. Attendance dashboard dekhta hai (overall + subject-wise)
3. Leave request submit karta hai
4. Notifications me attendance alerts + leave updates dekhta hai
5. Leave history me status track kar sakta hai (`pending/approved/rejected`)

---

## 5) Data Flow (Simple)

1. User mobile app me login karta hai.
2. Backend token return karta hai.
3. App token ko save karti hai.
4. Har protected API ke sath token bheja jata hai.
5. Backend token verify karta hai:
   - valid => data return
   - invalid => unauthorized

---

## 6) Database Collections (MongoDB)

## Users
- `name`
- `email`
- `password` (hashed)
- `role` (`admin/faculty/student`)
- `department`
- `classId` (students ke liye)

## Classes
- `className`
- `semester`
- `department`

## Subjects
- `subjectName`
- `classId`
- `facultyId`

## Attendance
- `studentId`
- `subjectId`
- `classId`
- `date`
- `status` (`present/absent`)
- `markedBy`

## LeaveRequests
- `studentId`
- `date`
- `reason`
- `status` (`pending/approved/rejected`)

## Notifications
- `userId`
- `message`
- `type`
- `read`

---

## 7) Main APIs

## Auth
- `POST /api/auth/register`
- `POST /api/auth/login`

## Admin
- `POST /api/admin/students`
- `POST /api/admin/faculty`
- `POST /api/admin/classes`
- `POST /api/admin/subjects`
- `GET /api/admin/classes`
- `GET /api/admin/faculty/list`
- `GET /api/admin/reports/overview`
- `POST /api/admin/announcements`

## Faculty
- `GET /api/faculty/classes`
- `GET /api/faculty/classes/:classId/students`
- `POST /api/faculty/attendance`
- `PUT /api/faculty/attendance/update`
- `GET /api/faculty/attendance/class`
- `GET /api/faculty/leave-requests`
- `PUT /api/faculty/leave-requests/status`

## Student
- `GET /api/student/attendance/me`
- `POST /api/student/leave-request`
- `GET /api/student/leave-requests/me`

## Notifications
- `GET /api/notifications`
- `POST /api/notifications`
- `PATCH /api/notifications/:id/read`

## Reports
- `GET /api/reports/attendance/export?format=csv|pdf`

---

## 8) Important Business Rules

- Duplicate attendance same student + subject + date pe allow nahi hai
- Attendance percentage auto calculate hota hai
- 75% se kam attendance par low-attendance notification ja sakta hai
- Leave approve/reject faculty karti hai (student ki class mapping ke basis pe)
- Student sirf apna data dekh sakta hai

---

## 9) Non-Technical Glossary (Simple)

- **API**: App aur server ke beech communication ka rasta.
- **Database**: Jahan data permanently store hota hai.
- **JWT Token**: Login proof card. Isse server ko pata chalta hai user kaun hai.
- **Hashing (bcrypt)**: Password ko unreadable secure form me convert karna.
- **Role-based Access**: Kaun kya dekh/kar sakta hai, role ke hisab se control.
- **Endpoint**: API ka specific URL action.
- **Middleware**: Request ke beech me security/check layer.
- **Controller**: Jahan business logic likha hota hai.
- **Schema/Model**: Database data ka structure.
- **CSV Export**: Data spreadsheet format me nikalna.

---

## 10) Run Guide (Quick)

## Backend
```cmd
cd C:\Users\admin\Attendance_Monitoring_App\backend
copy .env.example .env
npm install
npm start
```

## Optional seed data
```cmd
npm run seed
```

## Mobile (Dev)
```cmd
cd C:\Users\admin\Attendance_Monitoring_App\mobile
npm install
npx expo start -c
```

## Mobile (Local APK)
```cmd
cd C:\Users\admin\Attendance_Monitoring_App\mobile
npx expo prebuild --platform android --clean
cd android
gradlew.bat assembleRelease
```

APK output:
`mobile/android/app/build/outputs/apk/release/app-release.apk`

---

## 11) Common Issues + Fix

- `Unauthorized token missing`
  - App reinstall ya cache clear karo
  - Backend restart karo
  - Fresh login karo

- `Mongo ECONNREFUSED 127.0.0.1:27017`
  - MongoDB service start karo

- `There is not enough space on the disk`
  - C drive free karo
  - Gradle cache clean karo

- Mobile app backend se connect nahi ho raha
  - `mobile/utils/config.js` me `localhost` ki jagah PC LAN IP use karo
  - Phone + PC same Wi-Fi pe hon

---

## 12) Final Summary

Yeh project production-style architecture ke sath bana hai:
- secure auth
- role-based control
- modular backend
- modern mobile UI
- real attendance + leave workflow
- notifications + exports

Agar non-technical stakeholder ko explain karna ho:
**"Admin system setup karta hai, faculty attendance aur leaves manage karti hai, student apna attendance aur leave status track karta hai."**
