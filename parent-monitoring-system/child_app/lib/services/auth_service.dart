import 'package:child_app/services/api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  AuthService._();
  static final AuthService instance = AuthService._();

  static const _tokenKey = 'child_token';
  static const _childIdKey = 'child_id';

  Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
  }

  Future<void> _saveChildId(String id) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_childIdKey, id);
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

  Future<LoginResult> login(
    String childId,
    String password, {
    String? parentEmail,
  }) async {
    final requestBody = <String, dynamic>{
      'child_id': childId,
      'password': password,
    };
    if (parentEmail != null && parentEmail.trim().isNotEmpty) {
      requestBody['parent_email'] = parentEmail.trim().toLowerCase();
    }

    final response = await ApiService.instance.post(
      '/login-child',
      body: requestBody,
    );
    final token = response['access_token'] as String?;
    final child = response['child'] as Map<String, dynamic>?;
    if (token == null || child == null) {
      throw ApiException(statusCode: 401, message: 'Login failed');
    }
    ApiService.instance.setToken(token);
    await _saveToken(token);
    await _saveChildId(child['id'] as String);
    return LoginResult(token: token, childId: child['id'] as String);
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_childIdKey);
    ApiService.instance.clearToken();
  }
}

class LoginResult {
  final String token;
  final String childId;
  LoginResult({required this.token, required this.childId});
}
