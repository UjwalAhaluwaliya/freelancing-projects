# Strategic Portfolio Rationalization System (SPRS) - Technical + Non-Technical Guide

## 1) Project Overview (Simple)

SPRS ek intelligent platform hai jo organization ke projects ko evaluate karke actionable recommendation deta hai:
- RETAIN -> Project continue karo
- ENHANCE -> Improve karke continue karo
- CONSOLIDATE -> Similar projects merge karo
- DEFER -> Abhi ke liye hold karo
- RETIRE -> Project stop karo

Iska main objective:
- Budget ka better utilization
- Duplicate work reduce karna
- High-risk projects identify karna
- Business strategy aligned projects ko prioritize karna

---

## 2) Business Problem Jo Solve Hota Hai

Manual portfolio review me common problems:
- Subjective decisions
- Project duplication detect nahi hota
- Risk aur ROI ka balanced view missing hota
- Budget constraints ke andar best mix choose karna difficult hota

SPRS data + ML + optimization se ye decision process objective banata hai.

---

## 3) Implemented Tech Stack

### Frontend
- React.js (Vite)
- HTML/CSS/JavaScript
- Axios
- Recharts

### Backend
- Python Flask
- Flask-CORS
- Flask-JWT-Extended (JWT auth + RBAC)
- PyMongo

### Database
- MongoDB

### ML / Optimization
- pandas
- numpy
- scikit-learn
  - Random Forest
  - K-Means
  - TF-IDF + Cosine Similarity
  - Isolation Forest
- PuLP (Linear Programming)

---

## 4) Current System Features (Implemented)

1. Project CRUD APIs (add/list/get/delete)
2. Portfolio analysis pipeline (full ML flow)
3. Recommendation engine with 5 decision labels
4. Dashboard metrics APIs
5. Recommendation panel with project name + ID
6. Modern responsive UI (dashboard + analytics + recommendations + premium login)
7. Real authentication (/auth/login) using MongoDB users
8. Role-based access control with 3 roles:
   - dmin
   - project_manager
   - employee
9. Seed scripts:
   - sample projects (50)
   - default role users

---

## 5) Role-Based Access (RBAC)

### Admin
- Add project
- Delete project
- Run analysis
- View all dashboards/tables/recommendations

### Project Manager
- Add project
- Delete project
- Run analysis
- View all portfolio screens

### Employee
- Read-only access:
  - Dashboard
  - Portfolio Table
  - Recommendations
- Cannot add/delete projects
- Cannot run portfolio analysis

---

## 6) End-to-End Data Flow

1. User login karta hai (/auth/login) and JWT receive karta hai.
2. Frontend JWT ko local storage me save karta hai.
3. Axios har API request me Bearer token bhejta hai.
4. Flask role check karta hai (route-level guards).
5. Project data MongoDB me save/read hota hai.
6. POST /analyze_portfolio par ML pipeline run hoti hai.
7. Outputs portfolio_analysis + ecommendations collections me store hote hain.
8. Frontend dashboard/recommendation pages latest results show karte hain.

---

## 7) ML Algorithms - Technical Name + Non-Technical Meaning

## 7.1 AHP (Analytic Hierarchy Process)
Technical:
- Multiple criteria (ROI, Risk, Strategic Alignment, Cost) ko weighted score me convert karta hai.

Non-tech:
- Ye batata hai project overall kitna "valuable" hai jab multiple business factors ko ek saath dekha jaye.

Helps answer:
- "Kaunsa project strategic aur financially strong hai?"

---

## 7.2 Random Forest (Classification)
Technical:
- Ensemble decision trees se project success probability estimate karta hai.

Non-tech:
- Ye chance nikalta hai ki project successful hone ke kitne chances hain.

Helps answer:
- "Is project ki success probability kya hai?"

---

## 7.3 K-Means Clustering
Technical:
- Projects ko feature similarity ke basis par clusters me group karta hai.

Non-tech:
- Similar type ke projects ko ek group me dikhata hai.

Helps answer:
- "Kaunse projects ek jaise pattern follow kar rahe hain?"

---

## 7.4 TF-IDF + Cosine Similarity
Technical:
- Project description text ko vectorize karke similarity score nikalta hai.

Non-tech:
- Text level pe detect karta hai kaunse project descriptions almost same hain.

Helps answer:
- "Kya hum duplicate ya overlapping projects chala rahe hain?"

---

## 7.5 Isolation Forest
Technical:
- Outlier/anomaly detection algorithm jo unusual project behavior flag karta hai.

Non-tech:
- Ye risky ya abnormal projects pe warning deta hai.

Helps answer:
- "Kaunse projects unusual hain aur extra review chahiye?"

---

## 7.6 Linear Programming (PuLP)
Technical:
- Budget constraint ke under objective maximize karke optimal project set select karta hai.

Non-tech:
- Limited budget me best combination choose karta hai.

Helps answer:
- "Budget same hai to kaunse projects choose karein jisse max value mile?"

---

## 7.7 Recommendation Fusion Layer
Technical:
- AHP + RF + Similarity + Anomaly + Optimization outputs ko rule-based final label me map karta hai.

Non-tech:
- Sare model signals combine karke final decision deta hai (retain/enhance/consolidate/defer/retire).

Helps answer:
- "Final action kya lena chahiye?"

---

## 8) Backend API List (Current)

### Public
- POST /auth/login
- GET /

### Authenticated (All roles)
- GET /projects
- GET /project/<id>
- GET /recommendations
- GET /dashboard_metrics

### Restricted (dmin, project_manager)
- POST /add_project
- DELETE /project/<id>
- POST /analyze_portfolio

---

## 9) Frontend Screens

1. Login Page (real backend login)
2. Dashboard Page (metrics + top recommendations)
3. Add Project Page (role protected)
4. Portfolio Table
5. Analytics Dashboard (role protected)
6. Recommendation Panel

Charts implemented:
- ROI Distribution
- Risk Distribution
- Portfolio Priority Scores
- Project Clusters

---

## 10) Important Collections in MongoDB

- projects
- users
- portfolio_analysis
- ecommendations

---

## 11) Seed Data and Demo Accounts

### Sample Projects
- File: ackend/ml_models/sample_projects.json
- Seed script: ackend/scripts/seed_projects.py

### Users (RBAC)
- Seed script: ackend/scripts/seed_users.py

Default demo users:
- dmin@sprs.local / admin123
- pm@sprs.local / pm123
- employee@sprs.local / employee123

---

## 12) Environment Variables

### Backend (ackend/.env)
- MONGO_URI
- MONGO_DB_NAME
- API_HOST
- API_PORT
- API_DEBUG
- CORS_ORIGINS
- JWT_SECRET_KEY
- JWT_EXPIRES_HOURS

### Frontend (rontend/.env)
- VITE_API_BASE_URL

---

## 13) Folder Structure (Current)

`	ext
Strategic_Portfolio/
  backend/
    app.py
    config.py
    requirements.txt
    routes/
      auth_routes.py
      project_routes.py
      analysis_routes.py
    services/
      user_service.py
      analysis_service.py
      project_service.py
      recommendation_service.py
      dashboard_service.py
    ml_models/
      pipeline.py
      ahp_model.py
      random_forest_model.py
      clustering_model.py
      similarity_model.py
      anomaly_model.py
      optimization_model.py
      recommender.py
      sample_projects.json
    scripts/
      seed_projects.py
      seed_users.py
  frontend/
    src/
      pages/
      components/
      services/
      utils/
      styles/
  README.md
  PROJECT_TECHNICAL_GUIDE.md
`

---

## 14) Local Run Summary

1. MongoDB start karo
2. Backend dependencies install karo
3. Frontend dependencies install karo
4. Seed projects + seed users run karo
5. Backend run karo
6. Frontend run karo
7. Login with role account and test role-based views

Detailed commands ke liye root README.md follow karo.

---

## 15) Non-Technical 30-Second Explanation

"SPRS ek smart assistant hai jo company ke projects ka audit karke batata hai kaunsa project continue, improve, merge, hold, ya stop karna chahiye. Ye decision AI models aur budget optimization pe based hota hai, isliye decisions fast aur data-driven bante hain. Alag roles (admin/manager/employee) ko alag screens aur permissions milti hain."

---

## 16) Next Recommended Enhancements

1. Admin UI for user create/disable/role change
2. Audit trail for every action
3. Model explainability panel (feature importance per recommendation)
4. Scheduled retraining and drift monitoring
5. Export reports (PDF/Excel)

---

## 17) Demo Login Credentials (Role-wise)

Use these credentials after running `python scripts/seed_users.py`:

| Role | Email | Password | Permissions |
|---|---|---|---|
| Admin | `admin@sprs.local` | `admin123` | Full access |
| Project Manager | `pm@sprs.local` | `pm123` | Add/Delete projects, run analysis, view all portfolio pages |
| Employee | `employee@sprs.local` | `employee123` | Read-only dashboard/portfolio/recommendations |

Note: These are demo credentials for local development only.

## 18) Role Difference Matrix (What Each Role Can Do)

| Capability | Admin | Project Manager | Employee |
|---|---|---|---|
| Login to platform | Yes | Yes | Yes |
| View dashboard metrics | Yes | Yes | Yes |
| View portfolio table | Yes | Yes | Yes |
| View recommendations | Yes | Yes | Yes |
| Add project | Yes | Yes | No |
| Delete project | Yes | Yes | No |
| Run portfolio analysis (ML) | Yes | Yes | No |
| Access analytics page actions | Yes | Yes | No |
| Manage users/roles | Planned (future admin module) | No | No |

### Plain-language difference

- `Admin`: Full control for platform and portfolio operations.
- `Project Manager`: Operational control for projects and analysis, but no platform administration.
- `Employee`: Read-only visibility for tracking and understanding decisions.

### Why this split is useful

- Prevents accidental high-impact actions by read-only users.
- Keeps analysis and data changes in accountable hands.
- Gives organization-wide transparency without giving everyone write access.
