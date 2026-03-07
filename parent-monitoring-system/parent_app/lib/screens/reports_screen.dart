import 'package:flutter/material.dart';
import 'package:parent_app/models/app_state.dart';
import 'package:parent_app/services/data_service.dart';
import 'package:parent_app/services/parent_service.dart';
import 'package:parent_app/services/api_service.dart';
import 'package:parent_app/widgets/stat_card.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key, required this.appState});
  final AppState appState;

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  List<ChildModel> _children = [];
  ChildModel? _selectedChild;
  ReportData? _report;
  bool _loading = true;
  bool _refreshInProgress = false;
  int _lastKnownTabIndex = 0;

  @override
  void initState() {
    super.initState();
    _lastKnownTabIndex = widget.appState.currentIndex;
    widget.appState.addListener(_onAppStateChanged);
    _loadInitialData(preferredChildId: widget.appState.selectedChildId);
  }

  @override
  void dispose() {
    widget.appState.removeListener(_onAppStateChanged);
    super.dispose();
  }

  Future<void> _onAppStateChanged() async {
    if (!mounted || _refreshInProgress) return;
    final currentIndex = widget.appState.currentIndex;
    final enteredReportsTab = _lastKnownTabIndex != 3 && currentIndex == 3;
    _lastKnownTabIndex = currentIndex;
    if (currentIndex != 3) return;

    final preferredChildId = widget.appState.selectedChildId;
    final selectedMissing = _children.isEmpty;
    final selectedDifferent = preferredChildId != null &&
        preferredChildId.isNotEmpty &&
        preferredChildId != _selectedChild?.id;

    if (enteredReportsTab || selectedMissing || selectedDifferent) {
      _refreshInProgress = true;
      try {
        await _loadInitialData(preferredChildId: preferredChildId);
      } finally {
        _refreshInProgress = false;
      }
    }
  }

  /// Initial load of children and the first report
  Future<void> _loadInitialData({String? preferredChildId}) async {
    setState(() => _loading = true);
    try {
      final list = await ParentService.instance.getChildren();
      ChildModel? nextSelected;
      if (list.isNotEmpty) {
        if (preferredChildId != null && preferredChildId.isNotEmpty) {
          for (final c in list) {
            if (c.id == preferredChildId) {
              nextSelected = c;
              break;
            }
          }
        }
        nextSelected ??= list.first;
      }

      if (mounted) {
        setState(() {
          _children = list;
          _selectedChild = nextSelected;
          _report = null;
        });

        if (_selectedChild != null) {
          await _fetchReport(_selectedChild!.id);
        }
      }
    } catch (e) {
      debugPrint("Error loading children: $e");
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  /// Specifically fetch/refresh the report for the selected child
  Future<void> _fetchReport(String childId) async {
    try {
      final reportData = await DataService.instance.getReport(childId);
      if (mounted) {
        setState(() => _report = reportData);
      }
    } catch (e) {
      debugPrint("Error fetching report: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Reports'),
        actions: [
          // If more than 1 child exists, show selection dropdown in AppBar
          if (_children.length > 1)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: DropdownButton<String>(
                value: _selectedChild?.id,
                icon: const Icon(Icons.arrow_drop_down, color: Colors.white),
                dropdownColor: Theme.of(context).primaryColor,
                underline: const SizedBox(),
                onChanged: (String? newId) {
                  if (newId != null) {
                    final nextChild = _children.firstWhere((c) => c.id == newId);
                    setState(() {
                      _selectedChild = nextChild;
                      _report = null; // Clear old report to show loading
                    });
                    widget.appState.setSelectedChild(newId);
                    _fetchReport(newId);
                  }
                },
                items: _children.map((child) {
                  return DropdownMenuItem(
                    value: child.id,
                    child: Text(child.name, style: const TextStyle(color: Colors.white)),
                  );
                }).toList(),
              ),
            ),
        ],
      ),
      body: _loading 
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadInitialData,
              child: _children.isEmpty 
                  ? const Center(child: Text("No children linked to this account"))
                  : _buildReportContent(),
            ),
    );
  }

  Widget _buildReportContent() {
    return SingleChildScrollView(
      physics: const AlwaysScrollableScrollPhysics(),
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "Report for ${_selectedChild?.name}",
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          
          StatCard(
            title: 'Screen Time',
            value: '${_report?.totalUsageMinutes ?? 0} min',
            icon: Icons.timer,
            subtitle: _report?.dailyLimit != null 
                ? 'Limit: ${_report!.dailyLimit} min' 
                : 'No limit set',
          ),
          
          const SizedBox(height: 15),
          
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _setLimitDialog,
              child: const Text("Set Screen Time Limit"),
            ),
          ),
          const SizedBox(height: 10),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton(
              onPressed: _removeLimitDialog,
              child: const Text("Remove Screen Time Limit"),
            ),
          ),
          const SizedBox(height: 10),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton(
              onPressed: _resetTodayUsageDialog,
              child: const Text("Reset Today's Usage"),
            ),
          ),

          const SizedBox(height: 30),
          const Text("Recent Usage", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const Divider(),

          if (_report == null)
            const Center(child: LinearProgressIndicator())
          else if (_report!.dailyUsage.isEmpty)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 20),
              child: Text("No usage data found for this child."),
            )
          else
            ..._report!.dailyUsage.map((d) => Card(
              child: ListTile(
                title: Text(d.date),
                trailing: Text("${d.usageTime} min"),
              ),
            )),
        ],
      ),
    );
  }

  // Simplified Dialog with Mounted checks
  Future<void> _setLimitDialog() async {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text("Set Daily Limit"),
        content: TextField(
          controller: controller,
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(hintText: "Minutes"),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text("Cancel")),
          ElevatedButton(
            onPressed: () async {
              final mins = int.tryParse(controller.text);
              if (mins == null || _selectedChild == null) return;
              Navigator.pop(ctx);
              
              try {
                await ApiService.instance.post('/set-limit', body: {
                  "child_id": _selectedChild!.id,
                  "daily_limit": mins
                });
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Limit Updated")));
                  _fetchReport(_selectedChild!.id);
                }
              } catch (e) {
                if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Error setting limit")));
              }
            },
            child: const Text("Save"),
          )
        ],
      ),
    );
  }

  Future<void> _resetTodayUsageDialog() async {
    if (_selectedChild == null) return;
    final childName = _selectedChild!.name;

    final shouldReset = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text("Reset Today's Usage"),
        content: Text(
          "Reset today's usage for $childName to 0 minutes?",
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text("Reset"),
          ),
        ],
      ),
    );

    if (shouldReset != true) return;

    try {
      await DataService.instance.resetTodayUsage(_selectedChild!.id);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Today's usage reset successfully")),
      );
      await _fetchReport(_selectedChild!.id);
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to reset usage")),
      );
    }
  }

  Future<void> _removeLimitDialog() async {
    if (_selectedChild == null) return;
    final childName = _selectedChild!.name;

    final shouldRemove = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text("Remove Limit"),
        content: Text(
          "Remove screen time limit for $childName?",
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text("Remove"),
          ),
        ],
      ),
    );

    if (shouldRemove != true) return;

    try {
      await ApiService.instance.post('/set-limit', body: {
        "child_id": _selectedChild!.id,
        "daily_limit": 0,
      });
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Screen time limit removed")),
      );
      await _fetchReport(_selectedChild!.id);
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to remove limit")),
      );
    }
  }
}
