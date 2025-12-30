import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

/// Servicio para comunicación con RabbitMQ
class RabbitMQService {
  // URL automática: desarrollo local vs producción AWS
  static String get _baseUrl => kDebugMode 
    ? 'http://192.168.118.1:3000'  // Desarrollo (servidor local - IP de red)
    : 'http://18.224.141.231:3000'; // Producción (AWS)
  static const String _exchange = 'events_exchange';
  static const String _reactionsQueue = 'reacciones_cola';
  static const String _persistenceQueue = 'persistencia_cola';

  /// Publicar reacción (like/unlike)
  Future<bool> publishReaction({
    required String userId,
    required String outfitId,
    required String action,
    Map<String, dynamic>? metadata,
  }) async {
    try {
      final message = {
        'usuarioId': userId,
        'outfitId': outfitId,
        'accion': action,
        'metadata': {
          ...metadata ?? {},
          'device_type': 'mobile',
          'platform': 'android',
          'app_version': '1.0.0',
          'timestamp': DateTime.now().millisecondsSinceEpoch,
        },
      };

      final response = await http.post(
        Uri.parse('$_baseUrl/publish'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'exchange': _exchange,
          'queue': _reactionsQueue,
          'message': message,
        }),
      );

      if (response.statusCode == 200) {
        print('✅ Reacción $action enviada a RabbitMQ para outfit $outfitId');
        return true;
      } else {
        print('❌ Error enviando reacción: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('❌ Error publicando reacción: $e');
      return false;
    }
  }

  /// Publicar evento de usuario
  Future<bool> publishUserEvent({
    required String userId,
    required String eventType,
    required Map<String, dynamic> data,
  }) async {
    try {
      final message = {
        'usuarioId': userId,
        'evento': eventType,
        'datos': {
          ...data,
          'device_type': 'mobile',
          'platform': 'android',
          'timestamp': DateTime.now().millisecondsSinceEpoch,
        },
      };

      final response = await http.post(
        Uri.parse('$_baseUrl/publish'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'exchange': _exchange,
          'queue': _persistenceQueue,
          'message': message,
        }),
      );

      if (response.statusCode == 200) {
        print('✅ Evento de usuario $eventType enviado a RabbitMQ');
        return true;
      } else {
        print('❌ Error enviando evento de usuario: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('❌ Error publicando evento de usuario: $e');
      return false;
    }
  }

  /// Publicar evento de outfit
  Future<bool> publishOutfitEvent({
    required String outfitId,
    required String eventType,
    required Map<String, dynamic> data,
  }) async {
    try {
      final message = {
        'outfitId': outfitId,
        'evento': eventType,
        'datos': {
          ...data,
          'device_type': 'mobile',
          'platform': 'android',
          'timestamp': DateTime.now().millisecondsSinceEpoch,
        },
      };

      final response = await http.post(
        Uri.parse('$_baseUrl/publish'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'exchange': _exchange,
          'queue': _persistenceQueue,
          'message': message,
        }),
      );

      if (response.statusCode == 200) {
        print('✅ Evento de outfit $eventType enviado a RabbitMQ');
        return true;
      } else {
        print('❌ Error enviando evento de outfit: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('❌ Error publicando evento de outfit: $e');
      return false;
    }
  }

  /// Obtener notificaciones
  Future<List<Map<String, dynamic>>> getNotifications(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/notifications/$userId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.cast<Map<String, dynamic>>();
      }
      
      return [];
    } catch (e) {
      print('Error obteniendo notificaciones: $e');
      return [];
    }
  }

  /// Marcar notificación como leída
  Future<bool> markNotificationAsRead(String notificationId) async {
    try {
      final response = await http.put(
        Uri.parse('$_baseUrl/notifications/$notificationId/read'),
        headers: {'Content-Type': 'application/json'},
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error marcando notificación como leída: $e');
      return false;
    }
  }

  /// Verificar conexión con RabbitMQ
  Future<bool> checkConnection() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/health'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['rabbitmq'] == 'connected';
      }
      
      return false;
    } catch (e) {
      print('Error verificando conexión: $e');
      return false;
    }
  }

  /// Obtener información de cola
  Future<Map<String, dynamic>?> getQueueInfo(String queueName) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/queue-info/$queueName'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      
      return null;
    } catch (e) {
      print('Error obteniendo info de cola: $e');
      return null;
    }
  }

  /// Limpiar cola
  Future<bool> purgeQueue(String queueName) async {
    try {
      final response = await http.delete(
        Uri.parse('$_baseUrl/queue/$queueName/purge'),
        headers: {'Content-Type': 'application/json'},
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error limpiando cola: $e');
      return false;
    }
  }
}