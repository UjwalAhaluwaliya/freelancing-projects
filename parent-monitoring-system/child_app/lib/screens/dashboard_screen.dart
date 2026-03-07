import 'package:flutter/material.dart';
import 'package:child_app/services/auth_service.dart';
import 'package:child_app/services/child_service.dart';
import 'package:child_app/widgets/action_card.dart';
import 'package:child_app/widgets/time_card.dart';
import 'dart:async'; 
class DashboardScreen extends StatefulWidget {
  const DashboardScreen({
    super.key,
    required this.onOpenBrowser,
    required this.onViewUsage,
    required this.onTimeLimitReached,
    this.onLogout,
  });

  final VoidCallback onOpenBrowser;
  final VoidCallback onViewUsage;
  final VoidCallback onTimeLimitReached;
  final VoidCallback? onLogout;

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {

  DashboardData? _data;
  bool _loading = true;

  Timer? _refreshTimer;

  @override
  void initState() {
    super.initState();
    _loadData();
    // Refresh dashboard every 30 seconds to update countdown
    _refreshTimer = Timer.periodic(const Duration(seconds: 30), (t) => _loadData());
  }

  @override
  void dispose() {
    _refreshTimer?.cancel(); // Clean up
    super.dispose();
  }
  Future<void> _loadData() async {

    setState(() => _loading = true);

    try {

      _data = await ChildService.instance.getDashboard();

      if (_data!.limitExceeded && mounted) {
        widget.onTimeLimitReached();
      }

    } catch (_) {
      _data = null;
    }

    if (mounted) setState(() => _loading = false);
  }

  void _openBrowser() {

    if (_data?.limitExceeded == true) {
      widget.onTimeLimitReached();
      return;
    }

    widget.onOpenBrowser();
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(

        title: const Text('Kids Zone'),

        actions: [

          if (widget.onLogout != null)

            IconButton(

              icon: const Icon(Icons.logout),

              onPressed: () async {

                await AuthService.instance.logout();

                widget.onLogout?.call();

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

                    TimeCard(

                      label: 'Remaining Time',

                      value: _data?.remainingFormatted ?? 'No Limit',

                      icon: Icons.timer_rounded,

                    ),

                    const SizedBox(height: 24),

                    ActionCard(

                      title: 'Open Browser',

                      icon: Icons.language_rounded,

                      onTap: _openBrowser,

                    ),

                    const SizedBox(height: 12),

                    ActionCard(

                      title: 'View Usage',

                      icon: Icons.analytics_rounded,

                      onTap: widget.onViewUsage,

                    ),

                  ],

                ),

              ),

            ),

    );

  }
}