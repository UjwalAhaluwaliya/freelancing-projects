# Parent Control - Flutter Mobile App

Modern Flutter mobile app for the AI Parental Control System. Parent-facing app with dashboard, child management, alerts, and reports.

## Screens

1. **Login** - Email and password authentication
2. **Dashboard** - Child list, today's usage, alerts preview
3. **Children** - Add child, view child list
4. **Alerts** - View all alerts in card format
5. **Reports** - Screen time, blocked attempts, daily usage

## Setup

1. **Prerequisites**
   - Flutter SDK (3.10+)
   - Backend API running (see `../backend/README.md`)

2. **Configure API URL**
   Edit `lib/config/api_config.dart`:
   - **Android emulator**: `http://10.0.2.2:8000` (default)
   - **iOS simulator**: `http://localhost:8000`
   - **Physical device**: `http://YOUR_MACHINE_IP:8000`

3. **Install & Run**
   ```bash
   cd parent_app
   flutter pub get
   flutter run
   ```

## Project Structure

```
lib/
├── config/          # API configuration
├── models/           # App state
├── screens/          # Login, Dashboard, Children, Alerts, Reports
├── services/         # API, Auth, Parent, Data services
├── theme/            # App theme
├── widgets/          # Reusable components (StatCard, ChildCard, AlertCard)
└── main.dart
```

## Design

- Material Design 3
- Blue primary color (#2563EB)
- Rounded cards (16px radius)
- Bottom navigation bar
- Clean spacing and typography
