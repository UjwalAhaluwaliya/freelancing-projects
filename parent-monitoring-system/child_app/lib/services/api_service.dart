import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:child_app/config/api_config.dart';

class ApiService {
  ApiService._();
  static final ApiService instance = ApiService._();

  String? _token;

  void setToken(String token) => _token = token;
  void clearToken() => _token = null;

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  static String get baseUrl => ApiConfig.baseUrl;

  Future<Map<String, dynamic>> _handleResponse(http.Response response) async {
    final body = response.body.isEmpty ? null : jsonDecode(response.body);
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return body ?? {};
    }
    final message = body is Map ? body['detail'] : null;
    throw ApiException(
      statusCode: response.statusCode,
      message: message?.toString() ?? 'Request failed',
    );
  }

  Future<Map<String, dynamic>> post(String path, {Map<String, dynamic>? body}) async {
    final response = await http.post(
      Uri.parse('$baseUrl$path'),
      headers: _headers,
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> get(String path) async {
    final response = await http.get(
      Uri.parse('$baseUrl$path'),
      headers: _headers,
    );
    return _handleResponse(response);
  }
}

class ApiException implements Exception {
  final int statusCode;
  final String message;
  ApiException({required this.statusCode, required this.message});
  @override
  String toString() => message;
}
