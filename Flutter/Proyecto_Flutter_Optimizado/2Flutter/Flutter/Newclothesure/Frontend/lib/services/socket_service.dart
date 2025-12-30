import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:flutter/foundation.dart';

/// Servicio para comunicación en tiempo real con Socket.IO
class SocketService {
  // URL automática: desarrollo local vs producción AWS
  static String get _serverUrl => kDebugMode 
    ? 'http://192.168.118.1:3000'  // Desarrollo (servidor local - IP de red)
    : 'http://18.224.141.231:3000'; // Producción (AWS)
  
  // Singleton
  static final SocketService _instance = SocketService._internal();
  factory SocketService() => _instance;
  SocketService._internal();
  
  IO.Socket? _socket;
  bool _isConnected = false;
  
  // Getters
  bool get isConnected => _isConnected;
  IO.Socket? get socket => _socket;
  
  /// Conectar al servidor
  Future<void> connect() async {
    try {
      if (_socket != null && _socket!.connected) {
        print('🔌 Socket ya conectado');
        return;
      }
      
      print('🔄 Conectando a Socket.IO...');
      print('🌐 URL del servidor: $_serverUrl');
      print('🔧 Modo: ${kDebugMode ? "DESARROLLO" : "PRODUCCIÓN"}');
      
      _socket = IO.io(_serverUrl, IO.OptionBuilder()
        .setTransports(['websocket', 'polling'])
        .enableAutoConnect()
        .enableReconnection()
        .setReconnectionAttempts(10)
        .setReconnectionDelay(1000)
        .setTimeout(5000)
        .build());
      
      // Event listeners
      _socket!.onConnect((_) {
        _isConnected = true;
        print('✅ Conectado a Socket.IO: ${_socket!.id}');
      });
      
      _socket!.onDisconnect((_) {
        _isConnected = false;
        print('❌ Desconectado de Socket.IO');
      });
      
      _socket!.onConnectError((error) {
        _isConnected = false;
        print('❌ Error conectando a Socket.IO: $error');
      });
      
      _socket!.onReconnect((_) {
        _isConnected = true;
        print('🔄 Reconectado a Socket.IO: ${_socket!.id}');
      });
      
      _socket!.onReconnectError((error) {
        print('❌ Error reconectando a Socket.IO: $error');
      });
      
      _socket!.onReconnectFailed((_) {
        print('❌ Falló la reconexión a Socket.IO');
      });
      
    } catch (e) {
      print('❌ Error inicializando Socket.IO: $e');
    }
  }
  
  /// Desconectar del servidor
  void disconnect() {
    if (_socket != null) {
      _socket!.disconnect();
      _socket = null;
      _isConnected = false;
      print('🔌 Desconectado de Socket.IO');
    }
  }
  
  /// Enviar reacción (like/unlike)
  void sendReaction({
    required String userId,
    required String outfitId,
    required String action,
    Map<String, dynamic>? metadata,
  }) {
    if (!_isConnected || _socket == null) {
      print('❌ Socket no conectado, no se puede enviar reacción');
      return;
    }
    
    final data = {
      'userId': userId,
      'outfitId': outfitId,
      'action': action,
      'metadata': metadata ?? {},
    };
    
    print('📤 [SocketService] Enviando reacción via Socket.IO: $data');
    print('🔌 [SocketService] Socket conectado: ${_socket!.connected}');
    print('🆔 [SocketService] Socket ID: ${_socket!.id}');
    print('📡 [SocketService] Emitiendo evento: reaction');
    
    _socket!.emit('reaction', data);
    print('✅ [SocketService] Reacción emitida exitosamente');
  }
  
  /// Enviar evento de usuario
  void sendUserEvent({
    required String userId,
    required String eventType,
    required Map<String, dynamic> eventData,
  }) {
    if (!_isConnected || _socket == null) {
      print('❌ [SocketService] Socket no conectado, no se puede enviar evento de usuario');
      return;
    }
    
    final data = {
      'userId': userId,
      'eventType': eventType,
      'eventData': eventData,
    };
    
    print('📤 [SocketService] Enviando evento de usuario via Socket.IO: $data');
    print('🔌 [SocketService] Socket conectado: ${_socket!.connected}');
    print('🆔 [SocketService] Socket ID: ${_socket!.id}');
    print('📡 [SocketService] Emitiendo evento: user_event');
    
    _socket!.emit('user_event', data);
    print('✅ [SocketService] Evento de usuario emitido exitosamente');
  }
  
  /// Escuchar confirmación de reacción
  void onReactionSuccess(Function(Map<String, dynamic>) callback) {
    _socket?.on('reaction_success', (data) {
      print('✅ [SocketService] Reacción exitosa recibida: $data');
      callback(data);
    });
  }
  
  /// Escuchar error de reacción
  void onReactionError(Function(Map<String, dynamic>) callback) {
    _socket?.on('reaction_error', (data) {
      print('❌ [SocketService] Error en reacción recibido: $data');
      callback(data);
    });
  }
  
  /// Escuchar actualizaciones de outfit en tiempo real
  void onOutfitUpdated(Function(Map<String, dynamic>) callback) {
    _socket?.on('outfit_updated', (data) {
      print('🔄 [SocketService] Outfit actualizado en tiempo real: $data');
      callback(data);
    });
  }
  
  /// Escuchar confirmación de evento de usuario
  void onUserEventSuccess(Function(Map<String, dynamic>) callback) {
    _socket?.on('user_event_success', (data) {
      print('✅ [SocketService] Evento de usuario exitoso recibido: $data');
      callback(data);
    });
  }
  
  /// Escuchar error de evento de usuario
  void onUserEventError(Function(Map<String, dynamic>) callback) {
    _socket?.on('user_event_error', (data) {
      print('❌ [SocketService] Error en evento de usuario recibido: $data');
      callback(data);
    });
  }
  
  /// Limpiar todos los listeners
  void clearListeners() {
    _socket?.clearListeners();
  }
}

