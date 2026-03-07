import 'package:flutter/material.dart';
import 'package:parent_app/models/app_state.dart';
import 'package:parent_app/services/api_service.dart';
import 'package:parent_app/services/parent_service.dart';
import 'package:parent_app/widgets/child_card.dart';

class ChildManagementScreen extends StatefulWidget {
  const ChildManagementScreen({
    super.key,
    required this.appState,
  });

  final AppState appState;

  @override
  State<ChildManagementScreen> createState() => _ChildManagementScreenState();
}

class _ChildManagementScreenState extends State<ChildManagementScreen> {
  List<ChildModel> _children = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadChildren();
  }

  Future<void> _loadChildren() async {
    setState(() => _loading = true);
    try {
      _children = await ParentService.instance.getChildren();
    } catch (_) {}
    if (mounted) setState(() => _loading = false);
  }

  Future<void> _showAddChildDialog() async {
    final nameController = TextEditingController();
    final ageController = TextEditingController();
    final passwordController = TextEditingController();

    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Add Child'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: const InputDecoration(
                  labelText: 'Name',
                  hintText: "Child's name",
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: ageController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Age',
                  hintText: 'Age (0-18)',
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  hintText: 'Child login password',
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Add'),
          ),
        ],
      ),
    );

    if (result != true || !mounted) return;

    final name = nameController.text.trim();
    final age = int.tryParse(ageController.text) ?? 0;
    final password = passwordController.text;

    if (name.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Name is required')),
      );
      return;
    }
    if (age < 0 || age > 18) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Age must be 0-18')),
      );
      return;
    }
    if (password.length < 6) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Password must be at least 6 characters')),
      );
      return;
    }

    try {
      await ParentService.instance.addChild(
        name: name,
        age: age,
        password: password,
      );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Child added successfully'),
            backgroundColor: Color(0xFF16A34A),
          ),
        );
        _loadChildren();
      }
    } on ApiException catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message)),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Children'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: _showAddChildDialog,
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadChildren,
              child: _children.isEmpty
                  ? ListView(
                      children: [
                        const SizedBox(height: 80),
                        Icon(
                          Icons.person_add_alt_1_rounded,
                          size: 80,
                          color: Colors.grey[400],
                        ),
                        const SizedBox(height: 24),
                        Text(
                          'No children yet',
                          style: Theme.of(context).textTheme.titleLarge,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Add your first child to get started',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: const Color(0xFF64748B),
                              ),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 32),
                        Center(
                          child: ElevatedButton.icon(
                            onPressed: _showAddChildDialog,
                            icon: const Icon(Icons.add),
                            label: const Text('Add Child'),
                          ),
                        ),
                      ],
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.all(20),
                      itemCount: _children.length,
                      itemBuilder: (context, i) {
                        final c = _children[i];
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 12),
                          child: ChildCard(
                            name: c.name,
                            age: c.age,
                            onTap: () =>
                                widget.appState.navigateToReports(c.id),
                          ),
                        );
                      },
                    ),
            ),
    );
  }
}
