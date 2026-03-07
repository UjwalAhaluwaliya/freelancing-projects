import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

import 'package:image_picker/image_picker.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:intl/intl.dart';
import 'package:geolocator/geolocator.dart';

//to load profile pic thorugh cloudinary
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

Future<String?> uploadToCloudinary(File imageFile) async {
  const cloudName = "dvvjpjjdx";
  const uploadPreset = "profile_upload";

  final uri = Uri.parse(
    "https://api.cloudinary.com/v1_1/$cloudName/image/upload",
  );

  final request = http.MultipartRequest("POST", uri)
    ..fields['upload_preset'] = uploadPreset
    ..files.add(await http.MultipartFile.fromPath('file', imageFile.path));

  final response = await request.send();

  if (response.statusCode == 200) {
    final resStr = await response.stream.bytesToString();
    final jsonData = jsonDecode(resStr);
    return jsonData['secure_url']; // 👈 image URL
  }

  return null;
}
//pick image and load
Future<void> pickAndUpload() async {
  final picker = ImagePicker();
  final picked = await picker.pickImage(source: ImageSource.gallery);

  if (picked == null) return;

  File file = File(picked.path);

  String? imageUrl = await uploadToCloudinary(file);

  if (imageUrl != null) {
    print("Uploaded URL: $imageUrl");

    // Save to Firestore
    await FirebaseFirestore.instance
        .collection("users")
        .doc(FirebaseAuth.instance.currentUser!.uid)
        .set({
      "profileImage": imageUrl,
    }, SetOptions(merge: true));
  }
}

//BLOCK AND REPORT
Future<void> blockUser(String blockedUserId) async {
  final currentUser = FirebaseAuth.instance.currentUser;

  await FirebaseFirestore.instance
      .collection("blocked")
      .doc(currentUser!.uid)
      .collection("blockedUsers")
      .doc(blockedUserId)
      .set({
    "blockedAt": Timestamp.now(),
  });
}

Future<void> reportUser(String reportedUserId, String reason) async {
  final currentUser = FirebaseAuth.instance.currentUser;

  await FirebaseFirestore.instance.collection("reports").add({
    "reportedBy": currentUser!.uid,
    "reportedUser": reportedUserId,
    "reason": reason,
    "timestamp": Timestamp.now(),
  });
}
// ---------------- NOTIFICATIONS SETUP ----------------

final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
FlutterLocalNotificationsPlugin();

Future<void> setupNotifications() async {
  FirebaseMessaging messaging = FirebaseMessaging.instance;

  await messaging.requestPermission(
    alert: true,
    badge: true,
    sound: true,
  );

  const AndroidNotificationChannel channel = AndroidNotificationChannel(
    'high_importance_channel',
    'High Importance Notifications',
    importance: Importance.high,
  );

  const AndroidInitializationSettings initializationSettingsAndroid =
  AndroidInitializationSettings('@mipmap/ic_launcher');

  const InitializationSettings initializationSettings =
  InitializationSettings(android: initializationSettingsAndroid);

  await flutterLocalNotificationsPlugin.initialize(initializationSettings);

  await flutterLocalNotificationsPlugin
      .resolvePlatformSpecificImplementation<
      AndroidFlutterLocalNotificationsPlugin>()
      ?.createNotificationChannel(channel);

  FirebaseMessaging.onMessage.listen((RemoteMessage message) {
    if (message.notification != null) {
      flutterLocalNotificationsPlugin.show(
        0,
        message.notification!.title,
        message.notification!.body,
        const NotificationDetails(
          android: AndroidNotificationDetails(
            'high_importance_channel',
            'High Importance Notifications',
            importance: Importance.high,
            priority: Priority.high,
          ),
        ),
      );
    }
  });
}

Future<Position?> _getCurrentPosition() async {
  try {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return null;

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) return null;
    }
    if (permission == LocationPermission.deniedForever) return null;

    return await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );
  } catch (_) {
    return null;
  }
}

// ---------------- MAIN ----------------

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  await setupNotifications();
  runApp(const FittrineApp());
}

// ---------------- APP ----------------

class FittrineApp extends StatelessWidget {
  const FittrineApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fittrine — Find Your Fitness Partner',
      debugShowCheckedModeBanner: false,

      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: const Color(0xFF6C4DFF),
        scaffoldBackgroundColor: const Color(0xFF120A2A),

        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF6C4DFF),
          foregroundColor: Colors.white,
          elevation: 0,
        ),

        textTheme: const TextTheme(
          bodyLarge: TextStyle(color: Colors.white),
          bodyMedium: TextStyle(color: Colors.white70),
          titleLarge: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),

        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF6C4DFF),
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),

        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white10,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Colors.white24),
          ),
          labelStyle: const TextStyle(color: Colors.white70),
        ),
      ),


      home: const SplashScreen(),
    );
  }
}

// ---------------- SPLASH ----------------

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    checkLoginStatus();
  }

  void checkLoginStatus() async {
    await Future.delayed(const Duration(seconds: 2));
    User? user = FirebaseAuth.instance.currentUser;

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => user == null ? const LoginScreen() : const MatchScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Image.asset(
          "assets/images/fittrine_logo.png",
          width: 240,
        ),
      ),
    );
  }
}

// ---------------- LOGIN ----------------

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  bool isLoading = false;

  Future<void> loginUser() async {
    try {
      setState(() => isLoading = true);

      final credential =
      await FirebaseAuth.instance.signInWithEmailAndPassword(
        email: emailController.text.trim(),
        password: passwordController.text.trim(),
      );

      final token = await FirebaseMessaging.instance.getToken();

      // Do not block login if Firestore rules deny token sync.
      try {
        await FirebaseFirestore.instance
            .collection("users")
            .doc(credential.user!.uid)
            .set({"fcmToken": token}, SetOptions(merge: true));
      } catch (_) {}

      // 🔥 CLEAR STACK → NO BACK ARROW
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => const MatchScreen()),
            (route) => false,
      );
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text("$e")));
    } finally {
      setState(() => isLoading = false);
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF120A2A), Color(0xFF1C1040)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset("assets/images/fittrine_logo.png", height: 120),

              const SizedBox(height: 20),

              const Text(
                "Welcome to Fittrine",
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),

              const SizedBox(height: 40),

              TextField(
                controller: emailController,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(
                  labelText: "Email",
                  hintText: "Enter email address",
                  labelStyle: TextStyle(color: Colors.white70),
                  hintStyle: TextStyle(color: Colors.white38),
                ),
              ),

              const SizedBox(height: 20),

              TextField(
                controller: passwordController,
                obscureText: true,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(
                  labelText: "Password",
                  hintText: "Enter password",
                  labelStyle: TextStyle(color: Colors.white70),
                  hintStyle: TextStyle(color: Colors.white38),
                ),
              ),


              const SizedBox(height: 30),

              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: isLoading ? null : loginUser,
                  child: isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text("Login"),
                ),
              ),

              TextButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const RegisterScreen()),
                  );
                },
                child: const Text(
                  "Create New Account",
                  style: TextStyle(color: Color(0xFF9B7CFF)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// ---------------- REGISTER ----------------

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  bool isLoading = false;

  Future<void> registerUser() async {
    try {
      setState(() => isLoading = true);

      final credential =
      await FirebaseAuth.instance.createUserWithEmailAndPassword(
        email: emailController.text.trim(),
        password: passwordController.text.trim(),
      );

      final token = await FirebaseMessaging.instance.getToken();

      await FirebaseFirestore.instance
          .collection("users")
          .doc(credential.user!.uid)
          .set({
        "uid": credential.user!.uid,
        "name": nameController.text.trim(),
        "email": emailController.text.trim(),
        "createdAt": Timestamp.now(),
        "fcmToken": token,
      });

      // 🔥 ALSO CLEAR STACK
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => const ProfileSetupScreen()),
            (route) => false,
      );
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text("$e")));
    } finally {
      setState(() => isLoading = false);
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Create Account")),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            TextField(controller: nameController, decoration: const InputDecoration(labelText: "Full Name", border: OutlineInputBorder())),
            const SizedBox(height: 15),

            TextField(controller: emailController, decoration: const InputDecoration(labelText: "Email", border: OutlineInputBorder())),
            const SizedBox(height: 15),

            TextField(controller: passwordController, obscureText: true, decoration: const InputDecoration(labelText: "Password", border: OutlineInputBorder())),
            const SizedBox(height: 25),

            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: isLoading ? null : registerUser,
                child: isLoading ? const CircularProgressIndicator(color: Colors.white) : const Text("Create Account"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------- CHAT MESSAGE NOTIFICATION ----------------

Future<void> saveChatNotification(String toUserId) async {
  await FirebaseFirestore.instance.collection("notifications").add({
    "toUser": toUserId,
    "title": "💬 New Message",
    "body": "You received a new message",
    "timestamp": Timestamp.now(),
  });
}

// ---------------- PROFILE SETUP ----------------
// ---------------- PROFILE SETUP ----------------
class ProfileSetupScreen extends StatefulWidget {
  final bool editMode;

  const ProfileSetupScreen({super.key, this.editMode = false});

  @override
  State<ProfileSetupScreen> createState() => _ProfileSetupScreenState();
}

class _ProfileSetupScreenState extends State<ProfileSetupScreen> {
  String selectedGender = "Male";

  // 🔹 LOCATION
  String selectedState = "Maharashtra";
  final cityController = TextEditingController();

  final ageController = TextEditingController();
  final heightController = TextEditingController();
  final weightController = TextEditingController();

  bool isLoading = false;

  File? profileImage;
  String? existingImageUrl;

  final List<String> states = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
  ];

  @override
  void initState() {
    super.initState();
    if (widget.editMode) loadExistingProfile();
  }

  Future<void> loadExistingProfile() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    try {
      final doc =
          await FirebaseFirestore.instance.collection("users").doc(user.uid).get();

      final data = doc.data();
      if (data == null) return;

      setState(() {
        selectedGender = data["gender"] ?? "Male";
        ageController.text = data["age"] ?? "";
        heightController.text = data["height"] ?? "";
        weightController.text = data["weight"] ?? "";
        existingImageUrl = data["profileImage"];

        // 🔹 LOCATION LOAD
        selectedState = data["state"] ?? "Maharashtra";
        cityController.text = data["city"] ?? "";
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Profile read failed: $e")),
      );
    }
  }

  Future<void> pickImage() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.gallery);
    if (picked != null) setState(() => profileImage = File(picked.path));
  }

  Future<void> saveProfile() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    if (ageController.text.isEmpty ||
        heightController.text.isEmpty ||
        weightController.text.isEmpty ||
        cityController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please fill all fields")),
      );
      return;
    }

    try {
      setState(() => isLoading = true);

      String? imageUrl = existingImageUrl;

      if (profileImage != null) {
        imageUrl = await uploadToCloudinary(profileImage!);
      }

      await FirebaseFirestore.instance.collection("users").doc(user.uid).set({
        "gender": selectedGender,
        "age": ageController.text.trim(),
        "height": heightController.text.trim(),
        "weight": weightController.text.trim(),
        "profileImage": imageUrl,

        // 🔹 LOCATION SAVE
        "state": selectedState,
        "city": cityController.text.trim(),
      }, SetOptions(merge: true));

      final pos = await _getCurrentPosition();
      if (pos != null) {
        await FirebaseFirestore.instance.collection("users").doc(user.uid).set({
          "latitude": pos.latitude,
          "longitude": pos.longitude,
        }, SetOptions(merge: true));
      }

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => FitnessGoalScreen(editMode: widget.editMode),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error saving profile: $e")),
      );
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar:
      AppBar(title: Text(widget.editMode ? "Edit Profile" : "Profile Setup")),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              GestureDetector(
                onTap: pickImage,
                child: CircleAvatar(
                  radius: 55,
                  backgroundColor: Colors.white24,
                  backgroundImage: profileImage != null
                      ? FileImage(profileImage!)
                      : existingImageUrl != null
                      ? NetworkImage(existingImageUrl!)
                      : null,
                  child: profileImage == null && existingImageUrl == null
                      ? const Icon(Icons.camera_alt,
                      size: 30, color: Colors.white)
                      : null,
                ),
              ),
              const SizedBox(height: 25),

              DropdownButtonFormField(
                value: selectedGender,
                decoration: const InputDecoration(labelText: "Gender"),
                items: ["Male", "Female", "Other"]
                    .map((e) =>
                    DropdownMenuItem(value: e, child: Text(e)))
                    .toList(),
                onChanged: (value) => setState(() => selectedGender = value!),
              ),

              const SizedBox(height: 15),

              TextField(
                controller: ageController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: "Age"),
              ),

              const SizedBox(height: 15),

              TextField(
                controller: heightController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: "Height (cm)"),
              ),

              const SizedBox(height: 15),

              TextField(
                controller: weightController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: "Weight (kg)"),
              ),

              const SizedBox(height: 15),

              // 🔹 STATE
              DropdownButtonFormField(
                value: selectedState,
                decoration: const InputDecoration(labelText: "State"),
                items: states
                    .map((e) =>
                    DropdownMenuItem(value: e, child: Text(e)))
                    .toList(),
                onChanged: (value) =>
                    setState(() => selectedState = value!),
              ),

              const SizedBox(height: 15),

              // 🔹 CITY
              TextField(
                controller: cityController,
                decoration: const InputDecoration(labelText: "City"),
              ),

              const SizedBox(height: 30),

              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: isLoading ? null : saveProfile,
                  child: isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : Text(widget.editMode
                      ? "Update Profile"
                      : "Continue"),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}


// ---------------- FITNESS GOAL ----------------

class FitnessGoalScreen extends StatefulWidget {
  final bool editMode;

  const FitnessGoalScreen({super.key, this.editMode = false});

  @override
  State<FitnessGoalScreen> createState() => _FitnessGoalScreenState();
}

class _FitnessGoalScreenState extends State<FitnessGoalScreen> {
  String selectedGoal = "Weight Loss";
  bool isLoading = false;

  final Map<String, String> goalImages = {
    "Weight Loss": "assets/goals/weight_loss.png",
    "Muscle Gain": "assets/goals/muscle_gain.png",
    "Endurance": "assets/goals/endurance.png",
    "General Fitness": "assets/goals/general_fitness.png",
  };

  Future<void> saveGoal() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    setState(() => isLoading = true);

    await FirebaseFirestore.instance
        .collection("users")
        .doc(user.uid)
        .set({"fitnessGoal": selectedGoal}, SetOptions(merge: true));

    if (widget.editMode) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
            builder: (_) => WorkoutPreferenceScreen(editMode: true)),
      );
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => WorkoutPreferenceScreen()),
      );
    }
  }

  Widget goalTile(String title, String imagePath) {
    bool selected = selectedGoal == title;

    return GestureDetector(
      onTap: () => setState(() => selectedGoal = title),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        margin: const EdgeInsets.symmetric(vertical: 10),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(22),
          gradient: selected
              ? const LinearGradient(
            colors: [Color(0xFF7F5AF0), Color(0xFF2CB67D)],
          )
              : const LinearGradient(
            colors: [Color(0xFF1B103A), Color(0xFF24124D)],
          ),
          boxShadow: selected
              ? [
            BoxShadow(
              color: Colors.purple.withOpacity(0.6),
              blurRadius: 18,
              offset: const Offset(0, 6),
            )
          ]
              : [],
        ),
        child: Row(
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 250),
              height: 70,
              width: 70,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                boxShadow: selected
                    ? [
                  BoxShadow(
                    color: const Color(0xFF7F5AF0).withOpacity(0.8),
                    blurRadius: 25,
                    spreadRadius: 3,
                  ),
                  BoxShadow(
                    color: const Color(0xFF2CB67D).withOpacity(0.5),
                    blurRadius: 35,
                    spreadRadius: 6,
                  ),
                ]
                    : [],
              ),

              // ✅ CLEAN CIRCLE LOGO (NO SQUARE)
              child: Center(
                child: ClipOval(
                  child: Image.asset(
                    imagePath,
                    height: 48,
                    width: 48,
                    fit: BoxFit.contain,
                  ),
                ),
              ),
            ),

            const SizedBox(width: 18),

            Expanded(
              child: Text(
                title,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),

            Icon(
              selected ? Icons.check_circle : Icons.arrow_forward_ios,
              color: selected ? Colors.greenAccent : Colors.white54,
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0628),
      appBar: AppBar(
        title: const Text("Fitness Goals"),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            goalTile("Weight Loss", goalImages["Weight Loss"]!),
            goalTile("Muscle Gain", goalImages["Muscle Gain"]!),
            goalTile("Endurance", goalImages["Endurance"]!),
            goalTile("General Fitness", goalImages["General Fitness"]!),

            const Spacer(),

            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                onPressed: saveGoal,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF7F5AF0),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
                child: const Text(
                  "Continue",
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
// ---------------- WORKOUT PREF ----------------

// ---------------- WORKOUT PREFERENCE ----------------

class WorkoutPreferenceScreen extends StatefulWidget {
  final bool editMode;

  const WorkoutPreferenceScreen({super.key, this.editMode = false});

  @override
  State<WorkoutPreferenceScreen> createState() =>
      _WorkoutPreferenceScreenState();
}

class _WorkoutPreferenceScreenState extends State<WorkoutPreferenceScreen> {
  String selectedPreference = "Gym Workout";
  bool isLoading = false;

  final Map<String, String> workoutImages = {
    "Gym Workout": "assets/workouts/gym.png",
    "Home Workout": "assets/workouts/home.png",
    "Yoga": "assets/workouts/yoga.png",
    "Running": "assets/workouts/running.png",
    "CrossFit": "assets/workouts/crossfit.png",
  };

  @override
  void initState() {
    super.initState();
    if (widget.editMode) loadExistingPreference();
  }

  // ---------------- LOAD EXISTING ----------------
  Future<void> loadExistingPreference() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    try {
      final doc =
          await FirebaseFirestore.instance.collection("users").doc(user.uid).get();

      final data = doc.data();
      if (data == null) return;

      setState(() {
        selectedPreference = data["workoutPreference"] ?? "Gym Workout";
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Preference read failed: $e")),
      );
    }
  }

  // ---------------- SAVE ----------------
  Future<void> savePreference() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    setState(() => isLoading = true);

    await FirebaseFirestore.instance
        .collection("users")
        .doc(user.uid)
        .set({
      "workoutPreference": selectedPreference,
    }, SetOptions(merge: true));

    if (widget.editMode) {
      Navigator.pop(context);
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const MatchScreen()),
      );
    }

    setState(() => isLoading = false);
  }

  // ---------------- TILE ----------------
  Widget preferenceTile(String title, String imagePath) {
    bool selected = selectedPreference == title;

    return GestureDetector(
      onTap: () => setState(() => selectedPreference = title),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        margin: const EdgeInsets.symmetric(vertical: 10),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(22),
          gradient: selected
              ? const LinearGradient(
            colors: [Color(0xFF7F5AF0), Color(0xFF2CB67D)],
          )
              : const LinearGradient(
            colors: [Color(0xFF1B103A), Color(0xFF24124D)],
          ),
          boxShadow: selected
              ? [
            BoxShadow(
              color: Colors.purple.withOpacity(0.6),
              blurRadius: 18,
              offset: const Offset(0, 6),
            )
          ]
              : [],
        ),
        child: Row(
          children: [
            // ICON (fitness style)
            AnimatedContainer(
              duration: const Duration(milliseconds: 250),
              height: 70,
              width: 70,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                boxShadow: selected
                    ? [
                  BoxShadow(
                    color: const Color(0xFF7F5AF0).withOpacity(0.8),
                    blurRadius: 25,
                    spreadRadius: 3,
                  ),
                  BoxShadow(
                    color: const Color(0xFF2CB67D).withOpacity(0.5),
                    blurRadius: 35,
                    spreadRadius: 6,
                  ),
                ]
                    : [],
              ),
              child: ClipOval(
                child: SizedBox(
                  height: 50,
                  width: 50, // IMPORTANT — forces circle
                  child: Image.asset(
                    imagePath,
                    fit: BoxFit.cover,
                  ),
                ),
              ),
            ),

            const SizedBox(width: 18),

            Expanded(
              child: Text(
                title,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),

            Icon(
              selected ? Icons.check_circle : Icons.arrow_forward_ios,
              color: selected ? Colors.greenAccent : Colors.white54,
            ),
          ],
        ),
      ),
    );
  }

  // ---------------- UI ----------------
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0628),
      appBar: AppBar(
        title: Text(widget.editMode
            ? "Edit Workout Preference"
            : "Workout Preferences"),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            preferenceTile("Gym Workout", workoutImages["Gym Workout"]!),
            preferenceTile("Home Workout", workoutImages["Home Workout"]!),
            preferenceTile("Yoga", workoutImages["Yoga"]!),
            preferenceTile("Running", workoutImages["Running"]!),
            preferenceTile("CrossFit", workoutImages["CrossFit"]!),

            const Spacer(),

            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                onPressed: isLoading ? null : savePreference,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF7F5AF0),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
                child: isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Text(
                  widget.editMode ? "Update Preference" : "Find Match",
                  style: const TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
// ---------------- MATCH ENGINE ----------------



class MatchScreen extends StatefulWidget {
  const MatchScreen({super.key});

  @override
  State<MatchScreen> createState() => _MatchScreenState();
}

class _MatchScreenState extends State<MatchScreen> {
  List<Map<String, dynamic>> matches = [];
  int index = 0;
  bool isLoading = true;
  double maxDistanceKm = 0;

  @override
  void initState() {
    super.initState();
    loadMatches();
  }

  // ---------------- LOAD MATCHES ----------------
  Future<void> loadMatches() async {
    final currentUser = FirebaseAuth.instance.currentUser;
    if (currentUser == null) {
      if (!mounted) return;
      setState(() => isLoading = false);
      return;
    }

    if (!mounted) return;
    setState(() => isLoading = true);

    try {
      final myDoc = await FirebaseFirestore.instance
          .collection("users")
          .doc(currentUser.uid)
          .get();

      final data = myDoc.data();

      if (data == null ||
          !data.containsKey("fitnessGoal") ||
          !data.containsKey("workoutPreference")) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Please complete your profile first"),
          ),
        );

        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const FitnessGoalScreen()),
        );
        return;
      }

      final String myGoal = data["fitnessGoal"];
      final String myPref = data["workoutPreference"];
      final double? myLat = (data["latitude"] as num?)?.toDouble();
      final double? myLon = (data["longitude"] as num?)?.toDouble();

      List<String> blockedIds = [];
      List<String> swipedIds = [];

      try {
        final blockedSnapshot = await FirebaseFirestore.instance
            .collection("blocked")
            .doc(currentUser.uid)
            .collection("blockedUsers")
            .get();
        blockedIds = blockedSnapshot.docs.map((e) => e.id).toList();
      } catch (_) {}

      try {
        final swipedSnapshot = await FirebaseFirestore.instance
            .collection("swipes")
            .doc(currentUser.uid)
            .collection("swipedUsers")
            .get();
        swipedIds = swipedSnapshot.docs.map((e) => e.id).toList();
      } catch (_) {}

      // Use a single-field query to avoid composite-index dependency.
      final snapshot = await FirebaseFirestore.instance
          .collection("users")
          .where("fitnessGoal", isEqualTo: myGoal)
          .get();

      final loadedMatches = snapshot.docs
          .where((doc) =>
              doc.id != currentUser.uid &&
              doc.data()["workoutPreference"] == myPref &&
              !blockedIds.contains(doc.id) &&
              !swipedIds.contains(doc.id))
          .map((doc) {
            final d = doc.data();
            d["uid"] = doc.id;
            return d;
          })
          .where((d) {
            if (maxDistanceKm <= 0) return true;
            if (myLat == null || myLon == null) return true;

            final otherLat = (d["latitude"] as num?)?.toDouble();
            final otherLon = (d["longitude"] as num?)?.toDouble();
            if (otherLat == null || otherLon == null) return false;

            final distanceMeters = Geolocator.distanceBetween(
              myLat,
              myLon,
              otherLat,
              otherLon,
            );
            return distanceMeters <= (maxDistanceKm * 1000);
          })
          .toList();

      if (!mounted) return;
      setState(() {
        matches = loadedMatches;
        index = 0;
      });
    } on FirebaseException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Firestore error: ${e.code}")),
      );
      setState(() {
        matches = [];
        index = 0;
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Failed to load matches: $e")),
      );
      setState(() {
        matches = [];
        index = 0;
      });
    } finally {
      if (mounted) {
        setState(() => isLoading = false);
      }
    }
  }

  void nextCard() {
    setState(() => index++);
  }

  // ---------------- OPEN PROFILE EDIT ----------------
  void openEditProfile() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => const MyProfilePreviewScreen(),
      ),
    ).then((_) {
      matches.clear();
      index = 0;
      loadMatches(); // 🔥 refresh after coming back
    });
  }

  void openDailyProgress() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const DailyProgressScreen()),
    );
  }

  void _showLocationFilterDialog() {
    double tempRadius = maxDistanceKm;

    showDialog(
      context: context,
      builder: (_) => StatefulBuilder(
        builder: (dialogContext, setDialogState) => AlertDialog(
          title: const Text("Filter by distance"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                tempRadius == 0
                    ? "Distance filter: Off"
                    : "Within ${tempRadius.toStringAsFixed(0)} km",
              ),
              Slider(
                min: 0,
                max: 200,
                divisions: 20,
                value: tempRadius,
                onChanged: (value) {
                  setDialogState(() => tempRadius = value);
                },
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(dialogContext),
              child: const Text("Cancel"),
            ),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  maxDistanceKm = tempRadius;
                });
                Navigator.pop(dialogContext);
                loadMatches();
              },
              child: const Text("Apply"),
            ),
          ],
        ),
      ),
    );
  }

  // ---------------- UI ----------------
  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (matches.isEmpty || index >= matches.length) {
      return Scaffold(
        appBar: AppBar(
          title: const Text("Matches"),
          actions: [
            IconButton(
              icon: const Icon(Icons.edit),
              onPressed: openEditProfile,
            ),
            IconButton(
              icon: const Icon(Icons.location_on),
              onPressed: _showLocationFilterDialog,
            ),
            IconButton(
              icon: const Icon(Icons.insights),
              onPressed: openDailyProgress,
            ),
            IconButton(
              icon: const Icon(Icons.people),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (_) => const MatchesListScreen()),
                );
              },
            ),
            IconButton(
              icon: const Icon(Icons.logout),
              onPressed: () async {
                await FirebaseAuth.instance.signOut();
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (_) => const LoginScreen()),
                );
              },
            ),
          ],
        ),
        body: const Center(
          child: Text(
            "No matches found 😢",
            style: TextStyle(color: Colors.white70),
          ),
        ),
      );
    }

    var user = matches[index];

    return Scaffold(
      appBar: AppBar(
        title: const Text("Find Your Match"),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit),
            onPressed: openEditProfile,
          ),
          IconButton(
            icon: const Icon(Icons.location_on),
            onPressed: _showLocationFilterDialog,
          ),
          IconButton(
            icon: const Icon(Icons.insights),
            onPressed: openDailyProgress,
          ),
          IconButton(
            icon: const Icon(Icons.people),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const MatchesListScreen(),
                ),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await FirebaseAuth.instance.signOut();
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (_) => const LoginScreen()),
              );
            },
          ),
        ],
      ),
      body: Center(
        child: Dismissible(
          key: UniqueKey(),
          direction: DismissDirection.horizontal,
          onDismissed: (direction) async {
            final currentUser = FirebaseAuth.instance.currentUser;
            if (currentUser == null) return;

            final swipedUser = Map<String, dynamic>.from(user);

            // Show next user immediately even if network write fails.
            nextCard();

            try {
              await FirebaseFirestore.instance
                  .collection("swipes")
                  .doc(currentUser.uid)
                  .collection("swipedUsers")
                  .doc(swipedUser["uid"])
                  .set({"swipedAt": Timestamp.now()});
            } catch (e) {
              if (!mounted) return;
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text("Swipe write failed: $e")),
              );
              return;
            }

            if (direction == DismissDirection.startToEnd) {
              try {
                await FirebaseFirestore.instance
                    .collection("likes")
                    .doc(currentUser.uid)
                    .collection("likedUsers")
                    .doc(swipedUser["uid"])
                    .set({"likedAt": Timestamp.now()});
              } catch (e) {
                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text("Like write failed: $e")),
                );
                return;
              }

              DocumentSnapshot<Map<String, dynamic>> likedBack;
              try {
                likedBack = await FirebaseFirestore.instance
                    .collection("likes")
                    .doc(swipedUser["uid"])
                    .collection("likedUsers")
                    .doc(currentUser.uid)
                    .get();
              } catch (e) {
                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text("Mutual-check read failed: $e")),
                );
                return;
              }

              if (likedBack.exists) {
                try {
                  await FirebaseFirestore.instance
                      .collection("matches")
                      .doc(currentUser.uid)
                      .collection("matchedUsers")
                      .doc(swipedUser["uid"])
                      .set({"matchedAt": Timestamp.now()});

                  await FirebaseFirestore.instance
                      .collection("matches")
                      .doc(swipedUser["uid"])
                      .collection("matchedUsers")
                      .doc(currentUser.uid)
                      .set({"matchedAt": Timestamp.now()});
                } catch (e) {
                  if (!mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text("Match write failed: $e")),
                  );
                  return;
                }

                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text("Its a Match with ${swipedUser["name"]}!"),
                  ),
                );
              }
            }
          },
          child: GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => UserProfileScreen(user: user),
                ),
              );
            },
            child: Card(
              color: const Color(0xFF1F1344),
              elevation: 8,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
              child: Container(
                width: 300,
                height: 400,
                padding: const EdgeInsets.all(20),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CircleAvatar(
                      radius: 50,
                      backgroundColor: Colors.white24,
                      backgroundImage: user["profileImage"] != null &&
                          user["profileImage"] != ""
                          ? NetworkImage(user["profileImage"])
                          : null,
                      child: user["profileImage"] == null
                          ? Text(
                        (user["name"] ?? "U")[0],
                        style: const TextStyle(
                            fontSize: 26, color: Colors.white),
                      )
                          : null,
                    ),
                    const SizedBox(height: 20),
                    Text(
                      user["name"] ?? "Unknown",
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      user["fitnessGoal"] ?? "No Goal",
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 16,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      user["workoutPreference"] ?? "No Preference",
                      style: const TextStyle(
                        color: Colors.white54,
                        fontSize: 14,
                      ),
                    ),
                    const SizedBox(height: 20),
                    const Text(
                      "Swipe Right = Like 💘\nSwipe Left = Skip ❌",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white60,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}




//success match screen
class MatchSuccessScreen extends StatelessWidget {
  final String name;

  const MatchSuccessScreen({super.key, required this.name});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.favorite, color: Colors.red, size: 90),
            const SizedBox(height: 20),
            const Text(
              "IT'S A MATCH!",
              style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text(
              "You and $name liked each other 💘",
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 30),

            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Continue Swiping"),
            ),
          ],
        ),
      ),
    );
  }
}
// profile screen after tap
class UserProfileScreen extends StatelessWidget {
  final Map<String, dynamic> user;

  const UserProfileScreen({super.key, required this.user});



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("User Profile")),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            CircleAvatar(
              radius: 60,
              backgroundImage: user["profileImage"] != null && user["profileImage"] != ""
                  ? NetworkImage(user["profileImage"])
                  : null,
              child: user["profileImage"] == null
                  ? Text((user["name"] ?? "U")[0])
                  : null,
            ),

            const SizedBox(height: 20),

            Text(
              user["name"] ?? "Unknown",
              style: const TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),

            const SizedBox(height: 12),

            Text("Goal: ${user["fitnessGoal"] ?? "N/A"}",
                style: const TextStyle(color: Colors.white70)),

            Text("Workout: ${user["workoutPreference"] ?? "N/A"}",
                style: const TextStyle(color: Colors.white70)),

            Text("Gender: ${user["gender"] ?? "N/A"}",
                style: const TextStyle(color: Colors.white70)),

            Text("Age: ${user["age"] ?? "N/A"}",
                style: const TextStyle(color: Colors.white70)),

            Text("Height: ${user["height"] ?? "N/A"} cm",
                style: const TextStyle(color: Colors.white70)),

            Text("Weight: ${user["weight"] ?? "N/A"} kg",
                style: const TextStyle(color: Colors.white70)),


            const SizedBox(height: 25),

            // 🚫 BLOCK BUTTON
            ElevatedButton.icon(
              onPressed: () async {
                await blockUser(user["uid"]);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("User Blocked 🚫")),
                );
                Navigator.pop(context);
              },
              icon: const Icon(Icons.block),
              label: const Text("Block User"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                minimumSize: const Size(double.infinity, 50),
              ),
            ),

            const SizedBox(height: 10),

            // ⚠️ REPORT BUTTON
            ElevatedButton.icon(
              onPressed: () async {
                await reportUser(user["uid"], "Inappropriate behavior");
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("User Reported ⚠️")),
                );
              },
              icon: const Icon(Icons.flag),
              label: const Text("Report User"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.orange,
                minimumSize: const Size(double.infinity, 50),
              ),
            ),
          ],
        ),
      ),
    );
  }
}




 // CHAT SCREEN
class ChatScreen extends StatefulWidget {
  final String name;
  final String otherUserId;

  const ChatScreen({
    super.key,
    required this.name,
    required this.otherUserId,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController messageController = TextEditingController();

  bool isBlocked = false;
  bool checkingBlock = true;

  String getChatId(String myId, String otherId) {
    return myId.compareTo(otherId) < 0
        ? "${myId}_$otherId"
        : "${otherId}_$myId";
  }

  @override
  void dispose() {
    messageController.dispose();
    super.dispose();
  }

  // ---------------- CHECK BLOCK ----------------
  Future<void> checkIfBlocked() async {
    final me = FirebaseAuth.instance.currentUser;
    if (me == null) return;

    final doc = await FirebaseFirestore.instance
        .collection("blocked")
        .doc(me.uid)
        .collection("blockedUsers")
        .doc(widget.otherUserId)
        .get();

    setState(() {
      isBlocked = doc.exists;
      checkingBlock = false;
    });
  }

  Future<void> blockThisUser() async {
    await blockUser(widget.otherUserId);
    setState(() => isBlocked = true);

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("User blocked 🚫")),
    );
  }

  Future<void> reportThisUser() async {
    await reportUser(widget.otherUserId, "Inappropriate behavior");

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("User reported ⚠️")),
    );
  }

  // ---------------- PICK SCHEDULE ----------------
  Future<void> pickSchedule() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    DateTime? date = await showDatePicker(
      context: context,
      firstDate: DateTime.now(),
      lastDate: DateTime(2100),
      initialDate: DateTime.now(),
    );

    if (date == null) return;

    TimeOfDay? time =
    await showTimePicker(context: context, initialTime: TimeOfDay.now());

    if (time == null) return;

    final scheduled = DateTime(
      date.year,
      date.month,
      date.day,
      time.hour,
      time.minute,
    );

    final chatId = getChatId(user.uid, widget.otherUserId);

    await FirebaseFirestore.instance
        .collection("chats")
        .doc(chatId)
        .collection("schedule")
        .doc("workout")
        .set({
      "time": Timestamp.fromDate(scheduled),
      "status": "pending",
      "createdBy": user.uid,
    });
  }

  // ---------------- SEND MESSAGE ----------------
  Future<void> sendMessage() async {
    if (isBlocked) return;

    final user = FirebaseAuth.instance.currentUser;
    if (user == null || messageController.text.trim().isEmpty) return;

    final chatId = getChatId(user.uid, widget.otherUserId);

    await FirebaseFirestore.instance
        .collection("chats")
        .doc(chatId)
        .collection("messages")
        .add({
      "senderId": user.uid,
      "text": messageController.text.trim(),
      "timestamp": FieldValue.serverTimestamp(),
    });

    messageController.clear();
  }

  @override
  void initState() {
    super.initState();
    checkIfBlocked();
  }

  @override
  Widget build(BuildContext context) {
    if (checkingBlock) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      return const Scaffold(body: Center(child: Text("Not Logged In")));
    }

    final chatId = getChatId(user.uid, widget.otherUserId);

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.name),
        actions: [
          IconButton(
            icon: const Icon(Icons.calendar_today),
            onPressed: pickSchedule,
          ),
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == "block") blockThisUser();
              if (value == "report") reportThisUser();
            },
            itemBuilder: (context) => const [
              PopupMenuItem(value: "block", child: Text("Block User")),
              PopupMenuItem(value: "report", child: Text("Report User")),
            ],
          ),
        ],
      ),

      body: Column(
        children: [

          // 🔥 REALTIME SCHEDULE BANNER
          StreamBuilder<DocumentSnapshot>(
            stream: FirebaseFirestore.instance
                .collection("chats")
                .doc(chatId)
                .collection("schedule")
                .doc("workout")
                .snapshots(),
            builder: (context, snapshot) {
              if (!snapshot.hasData || !snapshot.data!.exists) {
                return const SizedBox();
              }

              final data =
              snapshot.data!.data() as Map<String, dynamic>;

              final time = (data["time"] as Timestamp).toDate();
              final status = data["status"];
              final createdBy = data["createdBy"];

              return Container(
                margin: const EdgeInsets.all(12),
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: const Color(0xFF24124D),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    Text(
                      "📅 ${DateFormat("dd MMM • hh:mm a").format(time)}",
                      style: const TextStyle(color: Colors.white),
                    ),

                    if (status == "pending" && createdBy != user.uid)
                      Row(
                        children: [
                          Expanded(
                            child: ElevatedButton(
                              onPressed: () async {
                                await FirebaseFirestore.instance
                                    .collection("chats")
                                    .doc(chatId)
                                    .collection("schedule")
                                    .doc("workout")
                                    .update({"status": "accepted"});
                              },
                              child: const Text("Accept"),
                            ),
                          ),
                          const SizedBox(width: 10),
                          Expanded(
                            child: ElevatedButton(
                              onPressed: () async {
                                await FirebaseFirestore.instance
                                    .collection("chats")
                                    .doc(chatId)
                                    .collection("schedule")
                                    .doc("workout")
                                    .update({"status": "rejected"});
                              },
                              child: const Text("Reject"),
                            ),
                          ),
                        ],
                      ),

                    if (status == "accepted")
                      const Text("✅ Accepted",
                          style: TextStyle(color: Colors.green)),

                    if (status == "rejected")
                      const Text("❌ Rejected",
                          style: TextStyle(color: Colors.red)),
                  ],
                ),
              );
            },
          ),

          if (isBlocked)
            const Expanded(
              child: Center(
                child: Text(
                  "🚫 You blocked this user",
                  style: TextStyle(color: Colors.red, fontSize: 18),
                ),
              ),
            )
          else ...[
            // 🔥 REALTIME CHAT
            Expanded(
              child: StreamBuilder<QuerySnapshot>(
                stream: FirebaseFirestore.instance
                    .collection("chats")
                    .doc(chatId)
                    .collection("messages")
                    .orderBy("timestamp")
                    .snapshots(),
                builder: (context, snapshot) {
                  if (!snapshot.hasData) {
                    return const Center(
                        child: CircularProgressIndicator());
                  }

                  final messages = snapshot.data!.docs;

                  return ListView.builder(
                    padding: const EdgeInsets.all(12),
                    itemCount: messages.length,
                    itemBuilder: (context, index) {
                      var msg =
                      messages[index].data() as Map<String, dynamic>;
                      bool isMe = msg["senderId"] == user.uid;
                      return chatBubble(msg["text"] ?? "", isMe);
                    },
                  );
                },
              ),
            ),

            Padding(
              padding: const EdgeInsets.all(8),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(controller: messageController),
                  ),
                  IconButton(
                    icon: const Icon(Icons.send),
                    onPressed: sendMessage,
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget chatBubble(String text, bool isMe) {
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isMe ? Colors.blue : Colors.grey.shade300,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Text(
          text,
          style: TextStyle(color: isMe ? Colors.white : Colors.black),
        ),
      ),
    );
  }
}


// match list screen
class MatchesListScreen extends StatefulWidget {
  const MatchesListScreen({super.key});

  @override
  State<MatchesListScreen> createState() => _MatchesListScreenState();
}

class _MatchesListScreenState extends State<MatchesListScreen> {
  @override
  Widget build(BuildContext context) {
    final currentUser = FirebaseAuth.instance.currentUser;

    if (currentUser == null) {
      return const Scaffold(
        body: Center(child: Text("Not logged in")),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text("Your Matches"),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await FirebaseAuth.instance.signOut();
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                    (route) => false,
              );
            },
          ),
        ],
      ),

      // 🔥 REALTIME STREAM
      body: StreamBuilder<QuerySnapshot>(
        stream: FirebaseFirestore.instance
            .collection("matches")
            .doc(currentUser.uid)
            .collection("matchedUsers")
            .orderBy("matchedAt", descending: true)
            .snapshots(),

        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    "Could not load profile from Firestore.",
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    "${snapshot.error}",
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white70, fontSize: 12),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const ProfileSetupScreen(editMode: true),
                          ),
                        );
                      },
                      child: const Text("Open Profile Editor"),
                    ),
                  ),
                ],
              ),
            );
          }

          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final matchDocs = snapshot.data!.docs;

          if (matchDocs.isEmpty) {
            return const Center(child: Text("No matches yet 😢"));
          }

          return ListView.builder(
            itemCount: matchDocs.length,
            itemBuilder: (context, index) {
              final otherUserId = matchDocs[index].id;

              // 🔥 load user profile realtime
              return StreamBuilder<DocumentSnapshot>(
                stream: FirebaseFirestore.instance
                    .collection("users")
                    .doc(otherUserId)
                    .snapshots(),

                builder: (context, userSnapshot) {
                  if (!userSnapshot.hasData) {
                    return const SizedBox();
                  }

                  final user =
                  userSnapshot.data!.data() as Map<String, dynamic>?;

                  if (user == null) return const SizedBox();

                  return Padding(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 12, vertical: 6),
                    child: Container(
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [
                            Color(0xFF1B103A),
                            Color(0xFF24124D),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.4),
                            blurRadius: 6,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),

                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 8),

                        // 🔥 PROFILE IMAGE
                        leading: CircleAvatar(
                          radius: 26,
                          backgroundColor: Colors.white24,
                          backgroundImage: user["profileImage"] != null &&
                              user["profileImage"] != ""
                              ? NetworkImage(user["profileImage"])
                              : null,
                          child: user["profileImage"] == null
                              ? Text(
                            user["name"] != null
                                ? user["name"][0]
                                : "?",
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          )
                              : null,
                        ),

                        title: Text(
                          user["name"] ?? "Unknown User",
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 17,
                          ),
                        ),

                        subtitle: Padding(
                          padding: const EdgeInsets.only(top: 4),
                          child: Text(
                            user["fitnessGoal"] ?? "No goal set",
                            style: const TextStyle(
                              color: Colors.white70,
                              fontSize: 13,
                            ),
                          ),
                        ),

                        trailing: Container(
                          decoration: BoxDecoration(
                            color: const Color(0xFF6C4DFF),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          padding: const EdgeInsets.all(8),
                          child: const Icon(
                            Icons.chat,
                            color: Colors.white,
                          ),
                        ),

                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => ChatScreen(
                                name: user["name"],
                                otherUserId: otherUserId,
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                  );
                },
              );
            },
          );
        },
      ),
    );
  }
}

 // update profile
class MyProfilePreviewScreen extends StatelessWidget {
  const MyProfilePreviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final user = FirebaseAuth.instance.currentUser;

    if (user == null) {
      return const Scaffold(
        body: Center(child: Text("Not Logged In")),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text("My Profile")),

      // 🔥 REALTIME PROFILE STREAM
      body: StreamBuilder<DocumentSnapshot>(
        stream: FirebaseFirestore.instance
            .collection("users")
            .doc(user.uid)
            .snapshots(),

        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final data = snapshot.data!.data() as Map<String, dynamic>?;

          if (data == null) {
            return const Center(child: Text("No profile found"));
          }

          return Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                Card(
                  color: const Color(0xFF1F1344),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      children: [
                        CircleAvatar(
                          radius: 50,
                          backgroundColor: Colors.white24,
                          backgroundImage:
                          data["profileImage"] != null &&
                              data["profileImage"] != ""
                              ? NetworkImage(data["profileImage"])
                              : null,
                          child: data["profileImage"] == null ||
                              data["profileImage"] == ""
                              ? Text(
                            (data["name"] ?? "U")[0],
                            style: const TextStyle(
                                fontSize: 26, color: Colors.white),
                          )
                              : null,
                        ),

                        const SizedBox(height: 15),

                        Text(
                          data["name"] ?? "Unknown",
                          style: const TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),

                        const SizedBox(height: 10),

                        infoRow("Goal", data["fitnessGoal"]),
                        infoRow("Workout", data["workoutPreference"]),
                        infoRow("Gender", data["gender"]),
                        infoRow("Age", data["age"]),
                        infoRow("Height", "${data["height"]} cm"),
                        infoRow("Weight", "${data["weight"]} kg"),

                        // 🔥 NEW LOCATION
                        infoRow("State", data["state"]),
                        infoRow("City", data["city"]),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 30),

                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    child: const Text("My Daily Progress"),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const DailyProgressScreen(),
                        ),
                      );
                    },
                  ),
                ),

                const SizedBox(height: 12),

                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    child: const Text("Update Profile"),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) =>
                          const ProfileSetupScreen(editMode: true),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  // 🔥 helper widget for clean rows
  Widget infoRow(String label, dynamic value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Text(
        "$label: ${value ?? "-"}",
        style: const TextStyle(color: Colors.white70),
      ),
    );
  }
}

class DailyProgressScreen extends StatefulWidget {
  const DailyProgressScreen({super.key});

  @override
  State<DailyProgressScreen> createState() => _DailyProgressScreenState();
}

class _DailyProgressScreenState extends State<DailyProgressScreen> {
  DateTime selectedDate = DateTime.now();
  bool isSaving = false;

  final workoutCountController = TextEditingController();
  final workoutHoursController = TextEditingController();
  final goalsAchievedController = TextEditingController();
  final notesController = TextEditingController();

  User? get _user => FirebaseAuth.instance.currentUser;

  CollectionReference<Map<String, dynamic>>? get _logsRef {
    final user = _user;
    if (user == null) return null;
    return FirebaseFirestore.instance
        .collection("selfProgress")
        .doc(user.uid)
        .collection("dailyLogs");
  }

  String _docId(DateTime date) => DateFormat("yyyy-MM-dd").format(date);

  @override
  void initState() {
    super.initState();
    _loadForDate(selectedDate);
  }

  @override
  void dispose() {
    workoutCountController.dispose();
    workoutHoursController.dispose();
    goalsAchievedController.dispose();
    notesController.dispose();
    super.dispose();
  }

  Future<void> _loadForDate(DateTime date) async {
    final logsRef = _logsRef;
    if (logsRef == null) return;

    try {
      final snapshot = await logsRef.doc(_docId(date)).get();
      final data = snapshot.data();

      if (data == null) {
        workoutCountController.clear();
        workoutHoursController.clear();
        goalsAchievedController.clear();
        notesController.clear();
        return;
      }

      // Backward compatible: supports both old and new field keys.
      workoutCountController.text =
          (data["workoutCount"] ?? data["durationMinutes"] ?? "").toString();
      workoutHoursController.text =
          (data["workoutHours"] ?? data["caloriesBurned"] ?? "").toString();
      goalsAchievedController.text =
          (data["goalsAchieved"] ?? data["weightKg"] ?? "").toString();
      notesController.text = (data["notes"] ?? "").toString();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Could not load daily log: $e")),
      );
    }
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: selectedDate,
      firstDate: DateTime(2020),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );

    if (picked == null) return;

    setState(() => selectedDate = picked);
    await _loadForDate(picked);
  }

  Future<void> _saveLog() async {
    final logsRef = _logsRef;
    if (logsRef == null) return;

    setState(() => isSaving = true);
    try {
      await logsRef.doc(_docId(selectedDate)).set({
        "date": Timestamp.fromDate(
          DateTime(selectedDate.year, selectedDate.month, selectedDate.day),
        ),
        "workoutCount": int.tryParse(workoutCountController.text.trim()) ?? 0,
        "workoutHours":
            double.tryParse(workoutHoursController.text.trim()) ?? 0,
        "goalsAchieved": goalsAchievedController.text.trim(),
        "notes": notesController.text.trim(),
        "updatedAt": Timestamp.now(),
      }, SetOptions(merge: true));

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Daily progress saved")),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Save failed: $e")),
      );
    } finally {
      if (mounted) setState(() => isSaving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_user == null) {
      return const Scaffold(
        body: Center(child: Text("Not logged in")),
      );
    }

    final logsRef = _logsRef!;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Self Progress"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Self Progress Feature (Fittrine)",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              "Daily workout data add karo aur niche previous history dekho.",
              style: TextStyle(color: Colors.white70, fontSize: 13),
            ),
            const SizedBox(height: 16),
            const Divider(color: Colors.white30),
            const SizedBox(height: 16),
            const Text(
              "Add Daily Progress",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            InkWell(
              onTap: _pickDate,
              borderRadius: BorderRadius.circular(16),
              child: Container(
                width: double.infinity,
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                decoration: BoxDecoration(
                  color: const Color(0xFF2A1F52),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white38),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: Text(
                        "Date: ${DateFormat("dd MMM yyyy").format(selectedDate)}",
                        style: const TextStyle(fontSize: 14),
                      ),
                    ),
                    const Icon(Icons.calendar_month),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: workoutCountController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(hintText: "Workout count"),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: workoutHoursController,
              keyboardType:
                  const TextInputType.numberWithOptions(decimal: true),
              decoration: const InputDecoration(hintText: "Workout hours"),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: goalsAchievedController,
              decoration: const InputDecoration(hintText: "Goals achieved"),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: notesController,
              maxLines: 2,
              decoration: const InputDecoration(hintText: "Notes (optional)"),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 54,
              child: ElevatedButton(
                onPressed: isSaving ? null : _saveLog,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6F4CFF),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                child: isSaving
                    ? const SizedBox(
                        height: 18,
                        width: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text(
                        "Save Daily Entry",
                        style: TextStyle(fontSize: 16),
                      ),
              ),
            ),
            const SizedBox(height: 20),
            const Divider(color: Colors.white30),
            const SizedBox(height: 16),
            const Text(
              "Previous Data",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
              stream: logsRef.orderBy("date", descending: true).snapshots(),
              builder: (context, snapshot) {
                if (snapshot.hasError) {
                  return Text("Error: ${snapshot.error}");
                }
                if (!snapshot.hasData) {
                  return const Center(child: CircularProgressIndicator());
                }

                final docs = snapshot.data!.docs;
                if (docs.isEmpty) {
                  return const Padding(
                    padding: EdgeInsets.only(top: 8),
                    child: Text(
                      "No previous entries yet.",
                      style: TextStyle(color: Colors.white70),
                    ),
                  );
                }

                return ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: docs.length,
                  itemBuilder: (context, i) {
                    final data = docs[i].data();
                    final ts = data["date"] as Timestamp?;
                    final date = ts?.toDate();

                    final workoutCount =
                        data["workoutCount"] ?? data["durationMinutes"] ?? 0;
                    final workoutHours =
                        data["workoutHours"] ?? data["caloriesBurned"] ?? 0;
                    final goalsAchieved =
                        data["goalsAchieved"] ?? data["weightKg"] ?? "-";

                    return Card(
                      color: const Color(0xFF24124D),
                      child: ListTile(
                        title: Text(
                          date == null
                              ? docs[i].id
                              : DateFormat("dd MMM yyyy").format(date),
                        ),
                        subtitle: Text(
                          "Count: $workoutCount, Hours: $workoutHours, Goals: $goalsAchieved",
                        ),
                        onTap: () async {
                          final selected = date ??
                              DateTime.tryParse(docs[i].id) ??
                              selectedDate;
                          setState(() => selectedDate = selected);
                          await _loadForDate(selectedDate);
                        },
                      ),
                    );
                  },
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
