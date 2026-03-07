import 'package:child_app/services/api_service.dart';

class ChildService {
  ChildService._();
  static final ChildService instance = ChildService._();

  Future<DashboardData> getDashboard() async {
    final response = await ApiService.instance.get('/child/dashboard');
    return DashboardData.fromJson(response);
  }

  Future<UsageData> getUsage() async {
    final response = await ApiService.instance.get('/child/usage');
    return UsageData.fromJson(response);
  }

  Future<UrlCheckResult> checkUrl(String url) async {
    final rawUrl = url.trim();
    final response = await ApiService.instance.post('/child/check-url', body: {
      'url': rawUrl,
    });
    return UrlCheckResult.fromJson(response);
  }

  /// Normalize URL for WebView loading (add https if missing).
  String normalizeUrlForWebView(String input) {
    var url = input.trim();
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://$url';
    }
    return url;
  }
}

class UrlCheckResult {
  final bool allowed;
  final String? reason;

  UrlCheckResult({required this.allowed, this.reason});

  factory UrlCheckResult.fromJson(Map<String, dynamic> json) => UrlCheckResult(
        allowed: json['allowed'] as bool? ?? false,
        reason: json['reason'] as String?,
      );
}

class DashboardData {
  final String childId;
  final int? dailyLimit;
  final int todayUsageMinutes;
  final int? remainingMinutes;
  final bool limitExceeded;

  DashboardData({
    required this.childId,
    this.dailyLimit,
    required this.todayUsageMinutes,
    this.remainingMinutes,
    required this.limitExceeded,
  });

  factory DashboardData.fromJson(Map<String, dynamic> json) => DashboardData(
        childId: json['child_id'] as String? ?? '',
        dailyLimit: json['daily_limit'] as int?,
        todayUsageMinutes: json['today_usage_minutes'] as int? ?? 0,
        remainingMinutes: json['remaining_minutes'] as int?,
        limitExceeded: json['limit_exceeded'] as bool? ?? false,
      );

  String get remainingFormatted {
    if (remainingMinutes == null) return 'No limit set';
    final h = remainingMinutes! ~/ 60;
    final m = remainingMinutes! % 60;
    if (h > 0) return '${h}h ${m}m';
    return '${m}m';
  }
}

class UsageData {
  final String childId;
  final List<DailyUsage> dailyUsage;
  final int totalUsageMinutes;

  UsageData({
    required this.childId,
    required this.dailyUsage,
    required this.totalUsageMinutes,
  });

  factory UsageData.fromJson(Map<String, dynamic> json) {
    final list = json['daily_usage'] as List? ?? [];
    return UsageData(
      childId: json['child_id'] as String? ?? '',
      dailyUsage: list
          .map((e) => DailyUsage.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalUsageMinutes: json['total_usage_minutes'] as int? ?? 0,
    );
  }

  String get todayFormatted {
    final today = DateTime.now().toIso8601String().split('T')[0];
    for (final d in dailyUsage) {
      if (d.date.startsWith(today)) {
        final m = d.usageTime;
        final h = m ~/ 60;
        final min = m % 60;
        if (h > 0) return '${h}h ${min}m';
        return '${min}m';
      }
    }
    return '0m';
  }
}

class DailyUsage {
  final String date;
  final int usageTime;

  DailyUsage({required this.date, required this.usageTime});

  factory DailyUsage.fromJson(Map<String, dynamic> json) => DailyUsage(
        date: json['date'] as String? ?? '',
        usageTime: json['usage_time'] as int? ?? 0,
      );
}
