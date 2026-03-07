import 'package:flutter/material.dart';
import 'package:parent_app/models/app_state.dart';
import 'package:parent_app/services/data_service.dart';
import 'package:parent_app/services/parent_service.dart';
import 'package:parent_app/widgets/alert_card.dart';

class AlertsScreen extends StatefulWidget {
  const AlertsScreen({
    super.key,
    required this.appState,
  });

  final AppState appState;

  @override
  State<AlertsScreen> createState() => _AlertsScreenState();
}

class _AlertsScreenState extends State<AlertsScreen> {
  List<AlertModel> _alerts = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadAlerts();
  }

  Future<void> _loadAlerts() async {
    setState(() => _loading = true);
    try {
      final children = await ParentService.instance.getChildren();
      List<AlertModel> all = [];
      for (final c in children) {
        final alerts = await DataService.instance.getAlerts(c.id);
        for (final a in alerts) {
          all.add(AlertModel(
            id: a.id,
            childId: a.childId,
            message: a.message,
            timestamp: a.timestamp,
            alertType: a.alertType,
          ));
        }
      }
      all.sort((a, b) => b.timestamp.compareTo(a.timestamp));
      _alerts = all;
    } catch (_) {}
    if (mounted) setState(() => _loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alerts'),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadAlerts,
              child: _alerts.isEmpty
                  ? ListView(
                      children: [
                        const SizedBox(height: 80),
                        Icon(
                          Icons.notifications_off_rounded,
                          size: 80,
                          color: Colors.grey[400],
                        ),
                        const SizedBox(height: 24),
                        Text(
                          'No alerts',
                          style: Theme.of(context).textTheme.titleLarge,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'You\'ll see alerts here when they occur',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: const Color(0xFF64748B),
                              ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.all(20),
                      itemCount: _alerts.length,
                      itemBuilder: (context, i) {
                        final a = _alerts[i];
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 12),
                          child: AlertCard(
                            message: a.message,
                            timestamp: a.timestamp,
                            alertType: a.alertType,
                          ),
                        );
                      },
                    ),
            ),
    );
  }
}
