import 'package:flutter/material.dart';
import 'package:parent_app/models/app_state.dart';
import 'package:parent_app/services/data_service.dart';
import 'package:parent_app/services/auth_service.dart';
import 'package:parent_app/services/parent_service.dart';
import 'package:parent_app/screens/profile_screen.dart';
import 'package:parent_app/widgets/alert_card.dart';
import 'package:parent_app/widgets/child_card.dart';
import 'package:parent_app/widgets/stat_card.dart';
import '../main.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({
    super.key,
    required this.appState,
  });

  final AppState appState;

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List<ChildModel> _children = [];
  List<AlertModel> _alerts = [];
  int _todayUsage = 0;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }
  @override
void didChangeDependencies() {
  super.didChangeDependencies();
  _loadData();
}

  Future<void> _loadData() async {
    setState(() => _loading = true);
    try {
      final children = await ParentService.instance.getChildren();
      _children = children;

      int totalToday = 0;
      List<AlertModel> allAlerts = [];
      final todayStr = DateTime.now().toIso8601String().split('T')[0];
      for (final c in children) {
        final usage = await DataService.instance.getUsage(c.id);
        DailyUsage? todayEntry;
        for (final d in usage.dailyUsage) {
          if (d.date.startsWith(todayStr)) {
            todayEntry = d;
            break;
          }
        }
        if (todayEntry != null) totalToday += todayEntry.usageTime;
        final alerts = await DataService.instance.getAlerts(c.id);
        allAlerts.addAll(alerts);
      }
      allAlerts.sort((a, b) => b.timestamp.compareTo(a.timestamp));
      _alerts = allAlerts.take(5).toList();
      _todayUsage = totalToday;
    } catch (_) {}
    if (mounted) setState(() => _loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person_outline),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const ProfileScreen(),
                ),
              );
            },
          ),
          IconButton(
  icon: const Icon(Icons.logout),
  onPressed: () async {

    await AuthService.instance.logout();

    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(
        builder: (_) => const AuthWrapper(),
      ),
      (route) => false,
    );

  },
),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadData,
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Overview',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 16),
                    StatCard(
                      title: "Today's Usage",
                      value: '$_todayUsage min',
                      icon: Icons.timer_rounded,
                      subtitle: 'Across all children',
                    ),
                    const SizedBox(height: 12),
                    StatCard(
                      title: 'Children',
                      value: '${_children.length}',
                      icon: Icons.people_rounded,
                    ),
                    const SizedBox(height: 24),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Your Children',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.w600,
                              ),
                        ),
                        TextButton.icon(
                          onPressed: () =>
                              widget.appState.navigateToChildManagement(),
                          icon: const Icon(Icons.add, size: 18),
                          label: const Text('Add'),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    if (_children.isEmpty)
                      Card(
                        child: Padding(
                          padding: const EdgeInsets.all(32),
                          child: Center(
                            child: Column(
                              children: [
                                Icon(
                                  Icons.person_add_alt_1,
                                  size: 48,
                                  color: Colors.grey[400],
                                ),
                                const SizedBox(height: 16),
                                Text(
                                  'No children added yet',
                                  style: Theme.of(context).textTheme.bodyLarge,
                                ),
                                const SizedBox(height: 8),
                                ElevatedButton.icon(
                                  onPressed: () =>
                                      widget.appState.navigateToChildManagement(),
                                  icon: const Icon(Icons.add),
                                  label: const Text('Add Child'),
                                ),
                              ],
                            ),
                          ),
                        ),
                      )
                    else
                      ..._children.map(
                        (c) => Padding(
                          padding: const EdgeInsets.only(bottom: 12),
                          child: ChildCard(
                            name: c.name,
                            age: c.age,
                            onTap: () =>
                                widget.appState.navigateToReports(c.id),
                          ),
                        ),
                      ),
                    const SizedBox(height: 24),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Recent Alerts',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.w600,
                              ),
                        ),
                        if (_alerts.isNotEmpty)
                          TextButton(
                            onPressed: () =>
                                widget.appState.navigateToAlerts(),
                            child: const Text('View all'),
                          ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    if (_alerts.isEmpty)
                      Card(
                        child: Padding(
                          padding: const EdgeInsets.all(24),
                          child: Row(
                            children: [
                              Icon(Icons.check_circle, color: Colors.green[400]),
                              const SizedBox(width: 16),
                              Text(
                                'No alerts',
                                style: Theme.of(context).textTheme.bodyLarge,
                              ),
                            ],
                          ),
                        ),
                      )
                    else
                      ..._alerts.take(3).map(
                            (a) => Padding(
                              padding: const EdgeInsets.only(bottom: 12),
                              child: AlertCard(
                                message: a.message,
                                timestamp: a.timestamp,
                                alertType: a.alertType,
                              ),
                            ),
                          ),
                  ],
                ),
              ),
            ),
    );
  }
}
