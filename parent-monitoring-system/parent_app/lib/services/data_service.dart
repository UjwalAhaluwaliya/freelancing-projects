import 'package:parent_app/services/api_service.dart';

class DataService {
  DataService._();
  static final DataService instance = DataService._();

  Future<UsageData> getUsage(String childId) async {
    try {
      final response = await ApiService.instance.get('/usage/$childId');
      return UsageData.fromJson(response);
    } catch (_) {
      return UsageData(childId: childId, dailyUsage: [], totalMinutes: 0);
    }
  }

  Future<void> setScreenLimit(String childId, int minutes) async {

  await ApiService.instance.post(
    '/set-limit',
    body: {
      "child_id": childId,
      "daily_limit": minutes
    },
  );

}

  Future<void> resetTodayUsage(String childId) async {
    await ApiService.instance.post(
      '/reset-usage',
      body: {
        "child_id": childId,
      },
    );
  }

  Future<List<AlertModel>> getAlerts(String childId) async {
    try {
      final response = await ApiService.instance.get('/alerts/$childId');
      final list = response['alerts'] as List? ?? [];
      return list
          .map((e) => AlertModel.fromJson(e as Map<String, dynamic>))
          .toList();
    } catch (_) {
      return [];
    }
  }

  Future<ReportData> getReport(String childId) async {
    try {
      final response = await ApiService.instance.get('/reports/$childId');
      return ReportData.fromJson(response);
    } catch (_) {
      return ReportData.empty(childId);
    }
  }
}

class UsageData {
  final String childId;
  final List<DailyUsage> dailyUsage;
  final int totalMinutes;

  UsageData({
    required this.childId,
    required this.dailyUsage,
    required this.totalMinutes,
  });

  factory UsageData.fromJson(Map<String, dynamic> json) {
    final list = json['daily_usage'] as List? ?? [];
    return UsageData(
      childId: json['child_id'] as String? ?? '',
      dailyUsage: list
          .map((e) => DailyUsage.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalMinutes: json['total_usage_minutes'] as int? ?? 0,
    );
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

class AlertModel {
  final String id;
  final String childId;
  final String message;
  final String timestamp;
  final String? alertType;

  AlertModel({
    required this.id,
    required this.childId,
    required this.message,
    required this.timestamp,
    this.alertType,
  });

  factory AlertModel.fromJson(Map<String, dynamic> json) => AlertModel(
        id: json['id'] as String? ?? '',
        childId: json['child_id'] as String? ?? '',
        message: json['message'] as String? ?? '',
        timestamp: json['timestamp'] as String? ?? '',
        alertType: json['alert_type'] as String?,
      );
}

class ReportData {
  final String childId;
  final List<DailyUsage> dailyUsage;
  final int totalUsageMinutes;
  final int blockedAttempts;
  final int? dailyLimit;

  ReportData({
    required this.childId,
    required this.dailyUsage,
    required this.totalUsageMinutes,
    required this.blockedAttempts,
    this.dailyLimit,
  });

  factory ReportData.fromJson(Map<String, dynamic> json) {
    final screenTime = json['screen_time'] as Map<String, dynamic>?;
    final list = json['daily_usage'] as List? ?? [];
    return ReportData(
      childId: json['child_id'] as String? ?? '',
      dailyUsage: list
          .map((e) => DailyUsage.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalUsageMinutes: json['total_usage_minutes'] as int? ?? 0,
      blockedAttempts: json['blocked_attempts'] as int? ?? 0,
      dailyLimit: screenTime?['daily_limit'] as int?,
    );
  }

  factory ReportData.empty(String childId) => ReportData(
        childId: childId,
        dailyUsage: [],
        totalUsageMinutes: 0,
        blockedAttempts: 0,
      );
}
