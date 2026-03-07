import 'package:parent_app/services/api_service.dart';

class ParentService {
  ParentService._();
  static final ParentService instance = ParentService._();

  Future<List<ChildModel>> getChildren() async {
    try {
      final response = await ApiService.instance.get('/children');
      final list = response['children'] as List? ?? [];
      return list
          .map((e) => ChildModel.fromJson(e as Map<String, dynamic>))
          .toList();
    } catch (_) {
      return [];
    }
  }

  Future<ChildModel> addChild({
    required String name,
    required int age,
    required String password,
  }) async {
    final response = await ApiService.instance.post('/add-child', body: {
      'name': name,
      'age': age,
      'password': password,
    });
    final child = response['child'] as Map<String, dynamic>;
    return ChildModel.fromJson(child);
  }

  Future<ParentProfile?> getProfile() async {
    try {
      final response = await ApiService.instance.get('/parent-profile');
      final parent = response['parent'] as Map<String, dynamic>?;
      if (parent == null) return null;
      return ParentProfile.fromJson(
        parent,
        childCount: response['child_count'] as int? ?? 0,
      );
    } catch (_) {
      return null;
    }
  }

  Future<ParentProfile> updateProfile({
    required String name,
    required String email,
    String? phone,
  }) async {
    final response = await ApiService.instance.put('/parent-profile', body: {
      'name': name.trim(),
      'email': email.trim(),
      'phone': (phone ?? '').trim(),
    });

    final parent = response['parent'] as Map<String, dynamic>;
    return ParentProfile.fromJson(
      parent,
      childCount: response['child_count'] as int? ?? 0,
    );
  }
}

class ChildModel {
  final String id;
  final String parentId;
  final String name;
  final int age;

  ChildModel({
    required this.id,
    required this.parentId,
    required this.name,
    required this.age,
  });

  factory ChildModel.fromJson(Map<String, dynamic> json) => ChildModel(
        id: json['id'] as String,
        parentId: json['parent_id'] as String,
        name: json['name'] as String,
        age: json['age'] as int,
      );
}

class ParentProfile {
  final String id;
  final String name;
  final String email;
  final String? phone;
  final int childCount;

  ParentProfile({
    required this.id,
    required this.name,
    required this.email,
    required this.phone,
    required this.childCount,
  });

  factory ParentProfile.fromJson(
    Map<String, dynamic> json, {
    required int childCount,
  }) =>
      ParentProfile(
        id: json['id'] as String? ?? '',
        name: json['name'] as String? ?? '',
        email: json['email'] as String? ?? '',
        phone: json['phone'] as String?,
        childCount: childCount,
      );
}
