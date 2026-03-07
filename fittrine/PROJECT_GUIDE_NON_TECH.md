# Fittrine App - Simple Project Guide (Non-Technical)

## 1. App ka Purpose
Fittrine ek fitness partner finding app hai. User apna profile banata hai, apna goal select karta hai, phir similar goals wale logon ko swipe karke connect karta hai.

## 2. User Journey (Step-by-Step)
1. User app open karta hai.
2. Login ya Register karta hai.
3. Profile details fill karta hai (name, age, gender, city, photo, etc.).
4. Fitness goal select karta hai (jaise weight loss, muscle gain).
5. Workout preference select karta hai (gym, home, yoga, etc.).
6. Match screen par similar users cards me dikhte hain.
7. Swipe right = like, swipe left = skip.
8. Agar dono users ne like kiya, match ban jaata hai.
9. Matched user ke saath chat/schedule possible hai.
10. User daily self-progress bhi save kar sakta hai date-wise.

## 3. Main Screens (Simple Language)
- `Login / Register`: Account banana ya login karna
- `Profile Setup`: Personal details bharna
- `Fitness Goal`: Target choose karna
- `Workout Preference`: Workout style choose karna
- `Find Your Match`: Swipe cards for partner
- `Your Matches`: Jo users matched ho chuke hain
- `Chat`: Matched users ke saath message
- `Self Progress`: Daily workout history save/view

## 4. Kya Kaam Kar Raha Hai (Expected Flow)
- Email/password authentication
- Profile save + edit
- Match listing based on goal + preference
- Swipe skip and like flow
- Mutual like -> match document create
- Your Matches listing
- Chat module
- Self Progress date-wise entry and previous history
- Location filter support (distance-based)

## 5. Kya Attention Chahiye Hota Hai (Operational Points)
- Firestore rules deploy na hone par `permission-denied` errors aa sakte hain.
- Swipe right (like), profile edit, progress save ye sab Firestore permissions par depend karte hain.
- Location filter ke liye app permission allow hona zaroori hai.

## 6. Tech Stack (Simple + Technical)
- Frontend: Flutter (Dart)
- Backend/Auth/DB: Firebase (Auth + Firestore)
- Notifications: Firebase Messaging + Local Notifications
- Image Handling: Image Picker + Cloudinary upload
- Location: Geolocator

## 7. Firestore Data (High Level)
- `users/{uid}` -> user profile
- `swipes/{uid}/swipedUsers/{otherUid}` -> swipe history
- `likes/{uid}/likedUsers/{otherUid}` -> likes
- `matches/{uid}/matchedUsers/{otherUid}` -> matches
- `chats/{chatId}/messages/*` -> chat messages
- `selfProgress/{uid}/dailyLogs/{yyyy-MM-dd}` -> daily progress
- `blocked/{uid}/blockedUsers/{otherUid}` -> blocked users
- `reports/*` -> reports

## 8. Non-Technical Explanation for Team/Clients
- App Tinder-like swipe model use karta hai, but fitness purpose ke liye.
- Matching random nahi hota, user goal and workout preference ke basis par hota hai.
- User ko profile complete karna zaroori hai tabhi meaningful matches milte hain.
- Self-progress feature user ko daily consistency track karne deta hai.

## 9. Quick Troubleshooting
- Error: `permission-denied`
  - Action: Firestore rules deploy karo.
- Match cards empty
  - Check: Goal + workout preference + users data availability.
- Location filter not working
  - Check: device location permission + profile lat/lon save.

## 10. Recommended Deployment Commands
```bash
cd c:\Users\admin\fittrine_app
firebase deploy --project fittrine --only firestore:rules,firestore:indexes
```

---
If needed, this document can be converted into a one-page PPT/handout for non-technical stakeholders.
