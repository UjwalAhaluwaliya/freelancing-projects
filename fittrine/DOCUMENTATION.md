# Fittrine App Documentation

## 1. Overview

Fittrine is a Flutter-based mobile application designed to help users find fitness partners based on goals, workout preferences, and optionally location. It uses Firebase for backend services (authentication, Firestore database, storage, messaging) and includes features like real-time chat, profile setup, matching logic, and notifications.

The entire app is currently contained in a single Dart file (`lib/main.dart`), with business logic and UI separated by comments.

## 2. Key Features

- **User Authentication**: Email/password registration and login via `firebase_auth`.
- **Profile Setup & Editing**: Collects personal details (name, gender, age, height, weight, location, state/city) plus profile image using Cloudinary.
- **Cloud Storage**: Upload profile images to Cloudinary and store the URL in Firestore.
- **Fitness Goals & Workout Preferences**: Onboarding screens store selections in Firestore.
- **Matching System**:
  - Filters by fitness goal, workout preference.
  - Excludes blocked users and those already swiped.
  - Optional radius-based location filtering (slider in match screen).
  - Swipeable card interface for browsing matches.
  - Matches list screen to review all partners.
- **Real-time Chat**:
  - Messages stored under `chats/{chatId}/messages` with senderId, text, timestamp.
  - Typing indicator implemented by setting `typingUser` on root chat doc.
  - Schedule workouts via calendar/timepicker stored in `chats/{chatId}/schedule/workout`.
- **Blocking & Reporting**: Users can block/report others; data saved in `blocked` and `reports` collections.
- **Notifications**: FCM token saved to user document, local notifications set up to handle incoming messages.

## 3. Technical Stack & Dependencies

- **Flutter SDK** (>=2.10).
- **Firebase packages**: `firebase_core`, `firebase_auth`, `cloud_firestore`, `firebase_storage`, `firebase_messaging`.
- **Media & Utilities**: `image_picker`, `http`, `firebase_local_notifications`, `intl`, `geolocator`.
- **Dev**: `flutter_lints`, `flutter_launcher_icons`.

Dependencies are managed in `pubspec.yaml`. After removing `geoflutterfire` due to version conflicts, location filtering is done manually via `geolocator`.

## 4. Architecture & File Structure

Currently all code resides in `lib/main.dart` but logically divided by comment sections:

1. Imports & helpers (Cloudinary, upload, location functions).
2. Notification setup.
3. `main()` and `FittrineApp` widget.
4. Screens: Splash, Login, Register, ProfileSetup, FitnessGoal, WorkoutPreference, Match, MatchSuccess, UserProfile, Chat, MatchesList.
5. Utility functions: blockUser, reportUser, saveChatNotification, uploadToCloudinary, etc.

### Key Widgets & Classes

- `SplashScreen` – initial loader.
- `LoginScreen` / `RegisterScreen` – authentication flows.
- `ProfileSetupScreen` – step 1 of onboarding with edit mode.
- `FitnessGoalScreen`, `WorkoutPreferenceScreen` – steps 2 & 3.
- `MatchScreen` – primary discovery UI with radius filter.
- `MatchSuccessScreen` – shown after mutual swipe.
- `ChatScreen` – real-time messaging interface.
- `MatchesListScreen` – view past matches.

## 5. Firebase Schema

- `users/{uid}` documents:
  - uid, name, email, createdAt, fcmToken
  - fitnessGoal, workoutPreference, gender, age, height, weight
  - state, city, latitude, longitude, profileImage
- `swipes/{uid}/swipedUsers/{otherUid}` – record when user swiped another.
- `blocked/{uid}/blockedUsers/{otherUid}` – block list.
- `reports` collection – each doc has reportedBy, reportedUser, reason, timestamp.
- `chats/{chatId}` documents:
  - optional `typingUser` field and `schedule/workout` subcollection with time/status.
  - subcollection `messages` storing individual messages.
- `notifications` collection for app notifications (e.g. new message alerts).

## 6. Navigation Flow

1. App launches → `SplashScreen` → check FirebaseAuth.
2. If not logged in → `LoginScreen` → (option to Register) → Login success pushes `MatchScreen`.
3. New user registration: `RegisterScreen` → create account → `ProfileSetupScreen` → `FitnessGoalScreen` → `WorkoutPreferenceScreen` → completes and navigates to `MatchScreen`.
4. From `MatchScreen` user can:
   - Edit profile (opens `MyProfilePreviewScreen` which leads to `ProfileSetupScreen` in edit mode).
   - Logout (return to `LoginScreen`).
   - Open `MatchesListScreen` or swipe through cards to connect.
   - Filter by location radius via dialog.
5. On successful match, `MatchSuccessScreen` with chat button.
6. Chat flows via `ChatScreen`; scheduling workouts and blocking/reporting available.

## 7. Location Filter Flow

- During profile save, request location permission via `geolocator`.
- Store latitude/longitude in user document.
- In `MatchScreen.loadMatches()`, if radius is set and both users have lat/lon, compute distance with `Geolocator.distanceBetween` and filter client-side.
- Radius control through app bar button launching `_showLocationFilterDialog` (slider 0–200 km, 0 disables filter).

## 8. Chat Enhancements

- Typing indicator: store `typingUser` on root chat doc as the UID of typing user.
- UI displays "Typing..." when the other user is currently typing.
- Messages now include timestamp displayed beneath each bubble.

## 9. Building & Deployment

Commands:

```bash
flutter pub get           # install deps
flutter build apk         # build release APK
# debug version: flutter build apk --debug

# Once APK built: adb install build/app/outputs/flutter-apk/app-release.apk
```

Remember to add location and internet permissions to `android/app/src/main/AndroidManifest.xml` and `Info.plist` for iOS.

## 10. Troubleshooting

- **Dependency conflicts**: Use `dependency_overrides` or remove conflicting packages. The geoflutterfire package was removed due to firebase version mismatch.
- **ADB install errors**: Usually caused by device restrictions; ensure developer options, allow install via USB, unlock screen, and uninstall previous builds.
- **Type errors when building**: Casting `doc.data()` properly and specifying generic types avoided errors.

## 11. Future Improvements

- Refactor into multiple Dart files and adopt state management (Provider, Riverpod, Bloc).
- Add distance label on each profile card.
- Add persistent settings (e.g. radius, notification preferences) using `shared_preferences`.
- Integrate phone verification, push notification topics, or premium subscription.
- Add unit/widget tests for each screen and service.

## 12. Useful Commands

- `flutter analyze` – static analysis.
- `flutter test` – run tests (none currently).
- `flutter pub outdated` – check for newer package versions.

## 13. Notes for Interview/Project Defense

- Talk about Flutter’s widget tree, Firebase integration, asynchronous programming (`async`/`await`, streams).
- Discuss trade-offs: keeping everything in one file for simplicity vs. maintainability.
- Explain why manual distance filtering replaced geoflutterfire (dependency issues) and how it works.
- Demonstrate how real-time features (chat, schedule) leverage Firestore snapshots.
- Mention handling of permissions and platform-specific requirements.

---

This document should serve as a comprehensive reference covering technical flows, data structure, and deployment steps for the Fittrine project.