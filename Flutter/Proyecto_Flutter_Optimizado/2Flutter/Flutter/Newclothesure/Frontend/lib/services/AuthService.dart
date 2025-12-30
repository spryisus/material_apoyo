import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter/foundation.dart';
import '../models/users.dart';

class AuthService {
  static const String _baseUrl = 'http://192.168.1.86:8000'; 

  final _secureStorage = const FlutterSecureStorage();
  static const String _tokenKey = 'auth_token';

  Future<User> login(String email, String password) async {
    debugPrint('Enviando login request: email=$email');

    final url = Uri.parse('$_baseUrl/login/');
    try {
      final response = await http.post(
        url,
        body: {
          'email': email,
          'password': password,
        },
      );

      debugPrint('Login response status: ${response.statusCode}');
      debugPrint('Login response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        debugPrint('Tokens en login response: '
            'access_token=${data['access_token']}, session_token=${data['session_token']}');

        final user = User.fromJson(data);

        // Guardar accessToken en secure storage
        if (user.accessToken != null) {
          await _saveToken(user.accessToken!);
        }

        debugPrint('User creado desde JSON: '
            'id=${user.userId}, fullName=${user.fullName}, email=${user.email}, '
            'accessToken=${user.accessToken}, sessionToken=${user.sessionToken}');

        return user;
      } else {
        throw Exception('Login failed: ${response.body}');
      }
    } catch (e) {
      debugPrint('Error en la autenticación: $e');
      throw Exception('Error en la autenticación: $e');
    }
  }

  Future<void> logout() async {
    await _secureStorage.delete(key: _tokenKey);
  }

  Future<String?> getToken() async {
    return await _secureStorage.read(key: _tokenKey);
  }

  Future<void> _saveToken(String token) async {
    await _secureStorage.write(key: _tokenKey, value: token);
  }
}