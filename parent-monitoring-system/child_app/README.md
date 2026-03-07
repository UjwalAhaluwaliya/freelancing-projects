# Kids Zone - Flutter Child App

Child-facing app for the AI Parental Control System. Provides a controlled browsing environment with parent-monitored screen time and URL filtering.

## Screens

1. **Login** - Child ID and password
2. **Dashboard** - Remaining screen time, Open Browser, View Usage buttons
3. **Smart Browser** - Enter URL, check with backend before loading; blocked sites show "Access Blocked"
4. **Time Limit** - Shown when screen time exceeded; "Please contact your parent"
5. **Usage** - Today's usage time

## Setup

1. **Prerequisites**
   - Flutter SDK (3.10+)
   - Backend API running

2. **Configure API URL**
   Edit `lib/config/api_config.dart`:
   - Android emulator: `http://10.0.2.2:8000`
   - Physical device: `http://YOUR_IP:8000`

3. **Child ID**
   Get Child ID from the Parent app after adding a child.

4. **Run**
   ```bash
   cd child_app
   flutter pub get
   flutter run
   ```

## Project Structure

```
lib/
├── config/       # API configuration
├── screens/      # Login, Dashboard, Browser, Time Limit, Usage
├── services/     # API, Auth, Child services
├── theme/        # App theme
├── widgets/      # ActionCard, TimeCard
└── main.dart
```

## Backend Endpoints Used

- `POST /login-child` - Child authentication
- `GET /child/dashboard` - Remaining time, limit status
- `GET /child/usage` - Usage data
- `POST /child/check-url` - URL safety check (child JWT)
