import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'models/app_state.dart';
import 'screens/alerts_screen.dart';
import 'screens/child_management_screen.dart';
import 'screens/dashboard_screen.dart';
import 'screens/login_screen.dart';
import 'screens/reports_screen.dart';
import 'services/auth_service.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const ParentControlApp());
}

class ParentControlApp extends StatelessWidget {
  const ParentControlApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AppState(),
      child: MaterialApp(
        title: 'Parent Control',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        home: const AuthWrapper(),
      ),
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

  @override
Widget build(BuildContext context) {

  if (_checking) {
    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }

  if (!_isLoggedIn) {
    return LoginScreen(

      onLoginSuccess: () async {

        final loggedIn =
            await AuthService.instance.isLoggedIn();

        if (mounted) {
          setState(() {
            _isLoggedIn = loggedIn;
          });
        }

      },

    );
  }

  return const MainShell();

}
}

class MainShell extends StatelessWidget {
  const MainShell({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<AppState>(
      builder: (context, appState, _) {
        return Scaffold(
          body: IndexedStack(
            index: appState.currentIndex,
            children: const [
              DashboardScreenWrapper(),
              ChildManagementScreenWrapper(),
              AlertsScreenWrapper(),
              ReportsScreenWrapper(),
            ],
          ),
          bottomNavigationBar: Container(
            decoration: BoxDecoration(
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.08),
                  blurRadius: 20,
                  offset: const Offset(0, -4),
                ),
              ],
            ),
            child: BottomNavigationBar(
              currentIndex: appState.currentIndex,
              onTap: (i) => appState.setIndex(i),
              items: const [
                BottomNavigationBarItem(
                  icon: Icon(Icons.dashboard_rounded),
                  label: 'Dashboard',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.people_rounded),
                  label: 'Children',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.notifications_rounded),
                  label: 'Alerts',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.analytics_rounded),
                  label: 'Reports',
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class DashboardScreenWrapper extends StatefulWidget {
  const DashboardScreenWrapper({super.key});

  @override
  State<DashboardScreenWrapper> createState() =>
      _DashboardScreenWrapperState();
}

class _DashboardScreenWrapperState
    extends State<DashboardScreenWrapper> {

  @override
  Widget build(BuildContext context) {
    return DashboardScreen(
      key: UniqueKey(),
      appState: context.read<AppState>(),
    );
  }
}

class ChildManagementScreenWrapper extends StatelessWidget {
  const ChildManagementScreenWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return ChildManagementScreen(appState: context.read<AppState>());
  }
}

class AlertsScreenWrapper extends StatelessWidget {
  const AlertsScreenWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return AlertsScreen(appState: context.read<AppState>());
  }
}

class ReportsScreenWrapper extends StatelessWidget {
  const ReportsScreenWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return ReportsScreen(appState: context.read<AppState>());
  }
}
