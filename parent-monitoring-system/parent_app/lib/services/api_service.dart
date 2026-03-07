import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:parent_app/config/api_config.dart';

class ApiService {
  ApiService._();
  static final ApiService instance = ApiService._();

  static String get baseUrl => ApiConfig.baseUrl;

  String? _token;

  void setToken(String token) {
    _token = token;
  }

  void clearToken() {
    _token = null;
  }

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  Future<Map<String, dynamic>> _handleResponse(
      http.Response response) async {

    print("STATUS: ${response.statusCode}");
    print("BODY: ${response.body}");

    final body =
        response.body.isEmpty ? {} : jsonDecode(response.body);

    if (response.statusCode >= 200 &&
        response.statusCode < 300) {
      return body;
    }

    throw ApiException(
      statusCode: response.statusCode,
      message: body["detail"]?.toString() ??
          "Request Failed",
    );
  }

  Future<Map<String, dynamic>> post(
    String path, {
    Map<String, dynamic>? body,
  }) async {

    print("POST → $baseUrl$path");

    final response = await http
        .post(
          Uri.parse('$baseUrl$path'),
          headers: _headers,
          body: body != null
              ? jsonEncode(body)
              : null,
        )
        .timeout(
          const Duration(seconds: 10),
        );

    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> get(String path) async {

    print("GET → $baseUrl$path");

    final response = await http
        .get(
          Uri.parse('$baseUrl$path'),
          headers: _headers,
        )
        .timeout(
          const Duration(seconds: 10),
        );

    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> put(
    String path, {
    Map<String, dynamic>? body,
  }) async {
    print("PUT → $baseUrl$path");

    final response = await http
        .put(
          Uri.parse('$baseUrl$path'),
          headers: _headers,
          body: body != null ? jsonEncode(body) : null,
        )
        .timeout(const Duration(seconds: 10));

    return _handleResponse(response);
  }
}

class ApiException implements Exception {

  final int statusCode;
  final String message;

  ApiException({
    required this.statusCode,
    required this.message,
  });

  @override
  String toString() => message;
}
