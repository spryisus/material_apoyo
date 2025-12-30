import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/outfit.dart';
import 'rabbitmq_service.dart';

/// Servicio para manejo de outfits
class OutfitService {
  static const String _baseUrl = 'https://b-e4c3889c-6ad8-4b70-a4c2-81d4f9c1fe5f.mq.us-east-2.on.aws'; // Tu RabbitMQ
  final RabbitMQService _rabbitmqService = RabbitMQService();

  // Singleton
  static final OutfitService _instance = OutfitService._internal();
  factory OutfitService() => _instance;
  OutfitService._internal();

  /// Obtener outfits del feed
  Future<List<Outfit>> getFeedOutfits({
    int page = 1,
    int limit = 20,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/outfits/feed?page=$page&limit=$limit'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Outfit.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      print('Error obteniendo outfits del feed: $e');
      return [];
    }
  }

  /// Obtener outfit por ID
  Future<Outfit?> getOutfitById(String outfitId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/outfits/$outfitId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return Outfit.fromJson(data);
      }
      
      return null;
    } catch (e) {
      print('Error obteniendo outfit: $e');
      return null;
    }
  }

  /// Buscar outfits
  Future<List<Outfit>> searchOutfits({
    required String query,
    int page = 1,
    int limit = 20,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/outfits/search?q=${Uri.encodeComponent(query)}&page=$page&limit=$limit'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Outfit.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      print('Error buscando outfits: $e');
      return [];
    }
  }

  /// Obtener outfits guardados
  Future<List<Outfit>> getSavedOutfits(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/users/$userId/saved-outfits'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Outfit.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      print('Error obteniendo outfits guardados: $e');
      return [];
    }
  }

  /// Dar like a un outfit
  Future<bool> likeOutfit({
    required String userId,
    required String outfitId,
  }) async {
    try {
      // Publicar evento de like en RabbitMQ
      final success = await _rabbitmqService.publishReaction(
        userId: userId,
        outfitId: outfitId,
        action: 'like',
        metadata: {
          'source': 'mobile_app',
          'action_type': 'like',
        },
      );

      if (success) {
        // También actualizar en la API REST
        final response = await http.post(
          Uri.parse('$_baseUrl/outfits/$outfitId/like'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'user_id': userId}),
        );

        return response.statusCode == 200;
      }

      return false;
    } catch (e) {
      print('Error dando like: $e');
      return false;
    }
  }

  /// Quitar like de un outfit
  Future<bool> unlikeOutfit({
    required String userId,
    required String outfitId,
  }) async {
    try {
      // Publicar evento de unlike en RabbitMQ
      final success = await _rabbitmqService.publishReaction(
        userId: userId,
        outfitId: outfitId,
        action: 'unlike',
        metadata: {
          'source': 'mobile_app',
          'action_type': 'unlike',
        },
      );

      if (success) {
        // También actualizar en la API REST
        final response = await http.delete(
          Uri.parse('$_baseUrl/outfits/$outfitId/like'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'user_id': userId}),
        );

        return response.statusCode == 200;
      }

      return false;
    } catch (e) {
      print('Error quitando like: $e');
      return false;
    }
  }

  /// Guardar outfit
  Future<bool> saveOutfit({
    required String userId,
    required String outfitId,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/users/$userId/saved-outfits'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'outfit_id': outfitId}),
      );

      if (response.statusCode == 200) {
        // Publicar evento de guardado
        await _rabbitmqService.publishUserEvent(
          userId: userId,
          eventType: 'outfit_saved',
          data: {
            'outfit_id': outfitId,
            'action': 'save',
          },
        );
      }

      return response.statusCode == 200;
    } catch (e) {
      print('Error guardando outfit: $e');
      return false;
    }
  }

  /// Quitar outfit guardado
  Future<bool> unsaveOutfit({
    required String userId,
    required String outfitId,
  }) async {
    try {
      final response = await http.delete(
        Uri.parse('$_baseUrl/users/$userId/saved-outfits/$outfitId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        // Publicar evento de desguardado
        await _rabbitmqService.publishUserEvent(
          userId: userId,
          eventType: 'outfit_unsaved',
          data: {
            'outfit_id': outfitId,
            'action': 'unsave',
          },
        );
      }

      return response.statusCode == 200;
    } catch (e) {
      print('Error quitando outfit guardado: $e');
      return false;
    }
  }

  /// Registrar vista de outfit
  Future<void> recordOutfitView({
    required String userId,
    required String outfitId,
    double duration = 0.0,
  }) async {
    try {
      await _rabbitmqService.publishOutfitEvent(
        outfitId: outfitId,
        eventType: 'view',
        data: {
          'user_id': userId,
          'duration': duration,
          'source': 'mobile_app',
        },
      );
    } catch (e) {
      print('Error registrando vista: $e');
    }
  }

  /// Crear nuevo outfit
  Future<Outfit?> createOutfit({
    required String userId,
    required String title,
    required String description,
    required List<String> images,
    required List<String> hashtags,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/outfits'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'user_id': userId,
          'title': title,
          'description': description,
          'images': images,
          'hashtags': hashtags,
        }),
      );

      if (response.statusCode == 201) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final outfit = Outfit.fromJson(data);

        // Publicar evento de creación
        await _rabbitmqService.publishOutfitEvent(
          outfitId: outfit.id,
          eventType: 'created',
          data: {
            'user_id': userId,
            'title': title,
            'hashtags': hashtags,
          },
        );

        return outfit;
      }
      
      return null;
    } catch (e) {
      print('Error creando outfit: $e');
      return null;
    }
  }

  /// Eliminar outfit
  Future<bool> deleteOutfit({
    required String userId,
    required String outfitId,
  }) async {
    try {
      final response = await http.delete(
        Uri.parse('$_baseUrl/outfits/$outfitId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'user_id': userId}),
      );

      if (response.statusCode == 200) {
        // Publicar evento de eliminación
        await _rabbitmqService.publishOutfitEvent(
          outfitId: outfitId,
          eventType: 'deleted',
          data: {
            'user_id': userId,
            'action': 'delete',
          },
        );
      }

      return response.statusCode == 200;
    } catch (e) {
      print('Error eliminando outfit: $e');
      return false;
    }
  }
}
