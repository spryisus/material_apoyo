import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user.dart';
import 'rabbitmq_service.dart';

/// Servicio para manejo de usuarios
class UserService {
  static const String _baseUrl = 'https://b-e4c3889c-6ad8-4b70-a4c2-81d4f9c1fe5f.mq.us-east-2.on.aws'; // Tu RabbitMQ
  final RabbitMQService _rabbitmqService = RabbitMQService();

  // Singleton
  static final UserService _instance = UserService._internal();
  factory UserService() => _instance;
  UserService._internal();

  /// Obtener usuario por ID
  Future<User?> getUserById(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/$userId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return User.fromJson(data);
      }
      
      return null;
    } catch (e) {
      print('Error obteniendo usuario: $e');
      return null;
    }
  }

  /// Obtener usuario por email
  Future<User?> getUserByEmail(String email) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/email/$email'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return User.fromJson(data);
      }
      
      return null;
    } catch (e) {
      print('Error obteniendo usuario por email: $e');
      return null;
    }
  }

  /// Crear nuevo usuario
  Future<User?> createUser({
    required String username,
    required String email,
    String? profileImage,
    String? bio,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/users'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'email': email,
          'profile_image': profileImage,
          'bio': bio,
        }),
      );

      if (response.statusCode == 201) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final user = User.fromJson(data);

        // Publicar evento de registro
        await _rabbitmqService.publishUserEvent(
          userId: user.id,
          eventType: 'registration',
          data: {
            'username': username,
            'email': email,
            'source': 'mobile_app',
          },
        );

        return user;
      }
      
      return null;
    } catch (e) {
      print('Error creando usuario: $e');
      return null;
    }
  }

  /// Actualizar perfil de usuario
  Future<User?> updateUserProfile({
    required String userId,
    String? username,
    String? email,
    String? profileImage,
    String? bio,
  }) async {
    try {
      final Map<String, dynamic> updateData = {};
      if (username != null) updateData['username'] = username;
      if (email != null) updateData['email'] = email;
      if (profileImage != null) updateData['profile_image'] = profileImage;
      if (bio != null) updateData['bio'] = bio;

      final response = await http.put(
        Uri.parse('$_baseUrl/users/$userId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(updateData),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final user = User.fromJson(data);

        // Publicar evento de actualización
        await _rabbitmqService.publishUserEvent(
          userId: userId,
          eventType: 'profile_update',
          data: {
            'updated_fields': updateData.keys.toList(),
            'source': 'mobile_app',
          },
        );

        return user;
      }
      
      return null;
    } catch (e) {
      print('Error actualizando perfil: $e');
      return null;
    }
  }

  /// Seguir usuario
  Future<bool> followUser({
    required String userId,
    required String targetUserId,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/users/$userId/follow'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'target_user_id': targetUserId}),
      );

      if (response.statusCode == 200) {
        // Publicar evento de seguimiento
        await _rabbitmqService.publishUserEvent(
          userId: userId,
          eventType: 'follow',
          data: {
            'target_user_id': targetUserId,
            'action': 'follow',
          },
        );
      }

      return response.statusCode == 200;
    } catch (e) {
      print('Error siguiendo usuario: $e');
      return false;
    }
  }

  /// Dejar de seguir usuario
  Future<bool> unfollowUser({
    required String userId,
    required String targetUserId,
  }) async {
    try {
      final response = await http.delete(
        Uri.parse('$_baseUrl/users/$userId/follow/$targetUserId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        // Publicar evento de dejar de seguir
        await _rabbitmqService.publishUserEvent(
          userId: userId,
          eventType: 'unfollow',
          data: {
            'target_user_id': targetUserId,
            'action': 'unfollow',
          },
        );
      }

      return response.statusCode == 200;
    } catch (e) {
      print('Error dejando de seguir usuario: $e');
      return false;
    }
  }

  /// Obtener seguidores
  Future<List<User>> getFollowers(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/$userId/followers'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => User.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      print('Error obteniendo seguidores: $e');
      return [];
    }
  }

  /// Obtener seguidos
  Future<List<User>> getFollowing(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/$userId/following'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => User.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      print('Error obteniendo seguidos: $e');
      return [];
    }
  }

  /// Verificar si un usuario sigue a otro
  Future<bool> isFollowing({
    required String userId,
    required String targetUserId,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/$userId/following/$targetUserId'),
        headers: {'Content-Type': 'application/json'},
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error verificando seguimiento: $e');
      return false;
    }
  }

  /// Obtener estadísticas del usuario
  Future<Map<String, int>?> getUserStats(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/$userId/stats'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return {
          'followers': data['followers'] as int? ?? 0,
          'following': data['following'] as int? ?? 0,
          'outfits': data['outfits'] as int? ?? 0,
          'likes': data['likes'] as int? ?? 0,
        };
      }
      
      return null;
    } catch (e) {
      print('Error obteniendo estadísticas: $e');
      return null;
    }
  }

  /// Buscar usuarios
  Future<List<User>> searchUsers({
    required String query,
    int page = 1,
    int limit = 20,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/search?q=${Uri.encodeComponent(query)}&page=$page&limit=$limit'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => User.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      print('Error buscando usuarios: $e');
      return [];
    }
  }

  /// Eliminar usuario
  Future<bool> deleteUser(String userId) async {
    try {
      final response = await http.delete(
        Uri.parse('$_baseUrl/users/$userId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        // Publicar evento de eliminación
        await _rabbitmqService.publishUserEvent(
          userId: userId,
          eventType: 'deleted',
          data: {
            'action': 'delete',
            'source': 'mobile_app',
          },
        );
      }

      return response.statusCode == 200;
    } catch (e) {
      print('Error eliminando usuario: $e');
      return false;
    }
  }
}
