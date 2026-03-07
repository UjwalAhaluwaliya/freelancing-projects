import 'package:flutter/material.dart';

class AlertCard extends StatelessWidget {
  const AlertCard({
    super.key,
    required this.message,
    required this.timestamp,
    this.alertType,
  });

  final String message;
  final String timestamp;
  final String? alertType;

  IconData get _icon {
    switch (alertType) {
      case 'blocked_website':
        return Icons.block;
      case 'toxic_message':
        return Icons.warning_amber_rounded;
      case 'screen_time_exceeded':
        return Icons.timer_off_rounded;
      default:
        return Icons.notifications_active;
    }
  }

  Color get _color {
    switch (alertType) {
      case 'blocked_website':
        return const Color(0xFFDC2626);
      case 'toxic_message':
        return const Color(0xFFF59E0B);
      case 'screen_time_exceeded':
        return const Color(0xFF2563EB);
      default:
        return const Color(0xFF64748B);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: _color.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(_icon, color: _color, size: 24),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    message,
                    style: theme.textTheme.bodyMedium,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _formatTimestamp(timestamp),
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: const Color(0xFF94A3B8),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _formatTimestamp(String ts) {
    try {
      final dt = DateTime.parse(ts);
      final now = DateTime.now();
      final diff = now.difference(dt);
      if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
      if (diff.inHours < 24) return '${diff.inHours}h ago';
      if (diff.inDays < 7) return '${diff.inDays}d ago';
      return '${dt.day}/${dt.month}/${dt.year}';
    } catch (_) {
      return ts;
    }
  }
}
