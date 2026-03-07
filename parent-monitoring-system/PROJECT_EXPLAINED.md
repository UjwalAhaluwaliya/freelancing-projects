# Parent Monitoring System - Simple + Technical Guide

## 1) Ye project karta kya hai? (Non-Technical)

Ye system parents ko help karta hai bachchon ki device activity monitor aur control karne me.

Parent app se:
- Child add kar sakte ho
- Daily screen time limit set kar sakte ho
- Reports dekh sakte ho (usage, blocked attempts)
- Alerts dekh sakte ho (unsafe website, etc.)
- Child ka aaj ka usage reset kar sakte ho

Child app me:
- Child login karta hai
- Remaining time dekh sakta hai
- Browser open karta hai
- Unsafe websites block hoti hain
- Time limit khatam hone par browsing block ho jati hai

Backend:
- Dono apps ko connect karta hai
- Data store karta hai
- Rules enforce karta hai (auth, ownership, time limit, blocking)

---

## 2) High-Level Flow (Simple Language)

1. Parent account banata/login karta hai.
2. Parent child add karta hai.
3. Parent child ke liye daily limit set karta hai (e.g., 60 min).
4. Child app me parent email + child name/id + password se login hota hai.
5. Child browser use karta hai:
- Har minute usage log hota hai
- Remaining time kam hota hai
- Unsafe URL block hota hai
- Remaining time 0 hone ke baad naya URL open nahi hota
6. Parent reports me dekh sakta hai:
- Kitna use hua
- Limit kya set hai
- Blocked attempts
7. Parent chahe to "Reset Today's Usage" karke aaj ka usage 0 kar sakta hai.

---

## 3) Technical Stack

### Backend
- Python
- FastAPI
- MongoDB (collections based storage)
- JWT auth (Parent token / Child token)

### Parent App
- Flutter (Dart)
- HTTP API calls to backend
- Provider-based app state (tab navigation + selected child flow)

### Child App
- Flutter (Dart)
- WebView for browsing
- Periodic usage logging (every 1 minute)
- Backend-based limit and safety checks

---

## 4) Major Modules

### Backend API Routes
- `auth`: parent/child login, add child, get children
- `screen_time`: set limit, get usage, reset usage
- `child`: child dashboard, child usage, child URL checks, child log usage
- `reports`: combined child report data
- `alerts`: alerts list per child
- `safety`: URL/text safety checks

### Data Collections (MongoDB)
- `parents`
- `children`
- `screen_time`
- `usage_logs`
- `alerts`

---

## 5) Important Fixes Already Applied

### A) Reports me "No children linked" false issue fixed
- Reports tab now refreshes when user enters tab or selected child changes.
- Child add karne ke baad report list stale nahi rehti.

### B) Time limit hard enforcement improved
- Child URL check now verifies time limit first.
- Limit reach hone ke baad child new URL open nahi kar sakta.

### C) Parent usage reset feature added
- Parent report screen se selected child ka today's usage reset kar sakta hai.
- Reset ke baad child ko limit ke according time phir se mil sakta hai.

### D) Same child-name conflict fixed
- Child login now parent-scoped using `parent_email`.
- Agar same name multiple parents ke under ho, wrong child login ka risk remove.

---

## 6) What Is Used vs Not Used

### Used
- JWT auth with separate parent/child roles
- Parent ownership checks (`ensure_parent_owns_child`)
- Parent email + child identity login path
- Server-side time-limit validation
- Server-side URL safety blocking
- Reports + alerts + usage aggregation

### Intentionally Not Used (abhi tak)
- OTP / phone verification
- Social login
- Real-time websocket updates
- Payment/subscription system
- Advanced role hierarchy (beyond parent/child)
- Complex analytics dashboard tools

---

## 7) Security & Access Rules

- Parent token only parent routes pe valid.
- Child token only child routes pe valid.
- Parent sirf apne linked child data access kar sakta hai.
- Child browser access backend checks ke through decide hota hai.

---

## 8) Build Readiness

Current state:
- Backend critical updated files compile-check pass.
- Child app analyze clean.
- Parent app me only info-level lint notes (non-blocking), build blocker nahi.

---

## 9) Non-Technical One-Line Summary

Ye system parent ko control deta hai aur child ko safe + time-limited internet usage deta hai, jahan rules backend se enforce hote hain aur dono apps sync me kaam karti hain.

