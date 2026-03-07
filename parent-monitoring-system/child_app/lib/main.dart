import 'package:flutter/material.dart';

import 'screens/browser_screen.dart';
import 'screens/dashboard_screen.dart';
import 'screens/login_screen.dart';
import 'screens/time_limit_screen.dart';
import 'screens/usage_screen.dart';
import 'services/auth_service.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const ChildControlApp());
}

class ChildControlApp extends StatelessWidget {
  const ChildControlApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Kids Zone',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const AuthWrapper(),
    );
  }
}

class AuthWrapper extends StatefulWidget {
  const AuthWrapper({super.key});

  @override
  State<AuthWrapper> createState() => _AuthWrapperState();
}

class _AuthWrapperState extends State<AuthWrapper> {
  bool _isLoggedIn = false;
  bool _checking = true;

  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    final loggedIn = await AuthService.instance.isLoggedIn();
    if (mounted) {
      setState(() {
        _isLoggedIn = loggedIn;
        _checking = false;
      });
    }
  }

  void _logout() {
    AuthService.instance.logout();
    setState(() => _isLoggedIn = false);
  }

  @override
  Widget build(BuildContext context) {
    if (_checking) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    if (!_isLoggedIn) {
      return LoginScreen(
        onLoginSuccess: () => setState(() => _isLoggedIn = true),
      );
    }
    return MainShell(onLogout: _logout);
  }
}

class MainShell extends StatelessWidget {
  const MainShell({super.key, required this.onLogout});

  final VoidCallback onLogout;

  @override
  Widget build(BuildContext context) {
    return Navigator(
      initialRoute: '/',
      onGenerateRoute: (settings) {
        if (settings.name != '/') return null;
        return MaterialPageRoute(
          builder: (_) => DashboardScreen(
            onLogout: onLogout,
            onOpenBrowser: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => BrowserScreen(
                  onBlocked: () {
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(
                        builder: (_) => TimeLimitScreen(
                          onBack: () => Navigator.pop(context),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
            onViewUsage: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const UsageScreen(),
              ),
            ),
            onTimeLimitReached: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => TimeLimitScreen(
                  onBack: () => Navigator.pop(context),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
