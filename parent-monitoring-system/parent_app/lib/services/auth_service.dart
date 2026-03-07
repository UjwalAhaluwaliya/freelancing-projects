import 'package:parent_app/services/api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  AuthService._();
  static final AuthService instance = AuthService._();

  static const _tokenKey = 'parent_token';
  static const _parentIdKey = 'parent_id';
  static const _parentNameKey = 'parent_name';

  Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
  }

  Future<void> _saveParentInfo(String id, String name) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_parentIdKey, id);
    await prefs.setString(_parentNameKey, name);
  }

  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(_tokenKey);
    if (token != null && token.isNotEmpty) {
      ApiService.instance.setToken(token);
      return true;
    }
    return false;
  }

  Future<LoginResult> login(String email, String password) async {
    final response = await ApiService.instance.post('/login-parent', body: {
      'email': email,
      'password': password,
    });
    final token = response['access_token'] as String?;
    final parent = response['parent'] as Map<String, dynamic>?;
    if (token == null || parent == null) {
      throw ApiException(statusCode: 401, message: 'Login failed');
    }
    ApiService.instance.setToken(token);
    await _saveToken(token);
    await _saveParentInfo(
      parent['id'] as String,
      parent['name'] as String? ?? '',
    );
    return LoginResult(
      token: token,
      parentId: parent['id'] as String,
      parentName: parent['name'] as String? ?? '',
    );
  }

  Future<void> forgotPassword({
    required String email,
    required String newPassword,
  }) async {
    await ApiService.instance.post('/forgot-parent-password', body: {
      'email': email.trim(),
      'new_password': newPassword,
    });
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_parentIdKey);
    await prefs.remove(_parentNameKey);
    ApiService.instance.clearToken();
  }
}

class LoginResult {
  final String token;
  final String parentId;
  final String parentName;

  LoginResult({
    required this.token,
    required this.parentId,
    required this.parentName,
  });
}
