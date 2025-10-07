import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../models/outfit.dart';
// import '../models/notification.dart'; // Archivo eliminado
import '../services/user_service.dart';
import '../services/outfit_service.dart';
import '../services/rabbitmq_service.dart';
import '../services/socket_service.dart';

/// Provider principal de la aplicación
class AppProvider with ChangeNotifier {
  final UserService _userService = UserService();
  final OutfitService _outfitService = OutfitService();
  final RabbitMQService _rabbitmqService = RabbitMQService();
  final SocketService _socketService = SocketService();

  // Estado de la aplicación
  User? _currentUser;
  List<Outfit> _feedOutfits = [];
  List<Outfit> _savedOutfits = [];
  List<Map<String, dynamic>> _notifications = [];
  bool _isLoading = false;
  String? _error;

  // Getters
  User? get currentUser => _currentUser;
  List<Outfit> get feedOutfits => _feedOutfits;
  List<Outfit> get savedOutfits => _savedOutfits;
  List<Map<String, dynamic>> get notifications => _notifications;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isLoggedIn => _currentUser != null;

  /// Establecer usuario actual
  void setCurrentUser(User? user) {
    _currentUser = user;
    notifyListeners();
  }

  /// Establecer estado de carga
  void setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  /// Establecer error
  void setError(String? error) {
    _error = error;
    notifyListeners();
  }

  /// Limpiar error
  void clearError() {
    _error = null;
    notifyListeners();
  }

  /// Cargar feed de outfits
  Future<void> loadFeedOutfits({int page = 1}) async {
    try {
      setLoading(true);
      clearError();

      // Conectar a Socket.IO si no está conectado
      if (!_socketService.isConnected) {
        await _socketService.connect();
        _setupSocketListeners();
      }

      // Por ahora usamos datos de prueba hasta que tengas el backend completo
      final outfits = _getMockOutfits();
      
      if (page == 1) {
        _feedOutfits = outfits;
      } else {
        _feedOutfits.addAll(outfits);
      }
      
      notifyListeners();
    } catch (e) {
      setError('Error cargando feed: $e');
    } finally {
      setLoading(false);
    }
  }

  /// Datos de prueba para el feed
  List<Outfit> _getMockOutfits() {
    return [
      Outfit(
        id: '1',
        userId: 'user1',
        username: 'Marina Carranza',
        profileImage: null,
        title: 'Look elegante para oficina',
        description: 'Perfecto para una reunión importante o cena de trabajo.',
        images: ['https://picsum.photos/400/600?random=1'],
        hashtags: ['Elegante', 'Oficina', 'Profesional'],
        likesCount: 414,
        commentsCount: 44,
        viewsCount: 2100,
        isLiked: false,
        isSaved: false,
        createdAt: DateTime.now().subtract(const Duration(days: 4)),
        updatedAt: DateTime.now().subtract(const Duration(days: 4)),
      ),
      Outfit(
        id: '2',
        userId: 'user2',
        username: 'Ana Isabel Borja',
        profileImage: null,
        title: 'Outfit casual de fin de semana',
        description: 'Cómodo y con estilo para pasear por la ciudad.',
        images: ['https://picsum.photos/400/600?random=2'],
        hashtags: ['Casual', 'Weekend', 'Comfort'],
        likesCount: 156,
        commentsCount: 28,
        viewsCount: 1200,
        isLiked: true,
        isSaved: false,
        createdAt: DateTime.now().subtract(const Duration(days: 2)),
        updatedAt: DateTime.now().subtract(const Duration(days: 2)),
      ),
      Outfit(
        id: '3',
        userId: 'user3',
        username: 'Carlos Mendoza',
        profileImage: null,
        title: 'Estilo minimalista nórdico',
        description: 'Menos es más. Look limpio y sofisticado.',
        images: ['https://picsum.photos/400/600?random=3'],
        hashtags: ['Minimalista', 'Nórdico', 'Clásico'],
        likesCount: 892,
        commentsCount: 67,
        viewsCount: 3400,
        isLiked: false,
        isSaved: true,
        createdAt: DateTime.now().subtract(const Duration(hours: 12)),
        updatedAt: DateTime.now().subtract(const Duration(hours: 12)),
      ),
    ];
  }

  /// Cargar outfits guardados
  Future<void> loadSavedOutfits() async {
    if (_currentUser == null) return;

    try {
      setLoading(true);
      clearError();

      final outfits = await _outfitService.getSavedOutfits(_currentUser!.id);
      _savedOutfits = outfits;
      
      notifyListeners();
    } catch (e) {
      setError('Error cargando outfits guardados: $e');
    } finally {
      setLoading(false);
    }
  }

  /// Cargar notificaciones
  Future<void> loadNotifications() async {
    if (_currentUser == null) return;

    try {
      setLoading(true);
      clearError();

      final notifications = await _rabbitmqService.getNotifications(_currentUser!.id);
      _notifications = notifications;
      
      notifyListeners();
    } catch (e) {
      setError('Error cargando notificaciones: $e');
    } finally {
      setLoading(false);
    }
  }

  /// Dar like a un outfit
  Future<void> likeOutfit(String outfitId) async {
    // Usar un usuario de prueba por ahora
    const testUserId = 'test_user_123';

    try {
      // Enviar reacción via Socket.IO
      _socketService.sendReaction(
        userId: testUserId,
        outfitId: outfitId,
        action: 'like',
        metadata: {
          'source': 'mobile_app',
          'platform': 'android',
          'app_version': '1.0.0',
          'timestamp': DateTime.now().millisecondsSinceEpoch,
        },
      );

      // Actualizar el outfit en la lista local inmediatamente
      _updateOutfitInList(outfitId, (outfit) => outfit.copyWith(
        isLiked: true,
        likesCount: outfit.likesCount + 1,
      ));
      
      print('✅ Like enviado via Socket.IO para outfit $outfitId');
      print('🔄 Actualizando UI - isLiked: true, likesCount: ${_feedOutfits.firstWhere((o) => o.id == outfitId).likesCount}');
      
    } catch (e) {
      setError('Error dando like: $e');
      print('❌ Error en like: $e');
    }
  }

  /// Quitar like de un outfit
  Future<void> unlikeOutfit(String outfitId) async {
    // Usar un usuario de prueba por ahora
    const testUserId = 'test_user_123';

    try {
      // Enviar reacción via Socket.IO
      _socketService.sendReaction(
        userId: testUserId,
        outfitId: outfitId,
        action: 'unlike',
        metadata: {
          'source': 'mobile_app',
          'platform': 'android',
          'app_version': '1.0.0',
          'timestamp': DateTime.now().millisecondsSinceEpoch,
        },
      );

      // Actualizar el outfit en la lista local inmediatamente
      _updateOutfitInList(outfitId, (outfit) => outfit.copyWith(
        isLiked: false,
        likesCount: outfit.likesCount - 1,
      ));
      
      print('✅ Unlike enviado via Socket.IO para outfit $outfitId');
      
    } catch (e) {
      setError('Error quitando like: $e');
      print('❌ Error en unlike: $e');
    }
  }

  /// Guardar outfit
  Future<void> saveOutfit(String outfitId) async {
    if (_currentUser == null) return;

    try {
      final success = await _outfitService.saveOutfit(
        userId: _currentUser!.id,
        outfitId: outfitId,
      );

      if (success) {
        // Actualizar el outfit en la lista local
        _updateOutfitInList(outfitId, (outfit) => outfit.copyWith(
          isSaved: true,
        ));
      }
    } catch (e) {
      setError('Error guardando outfit: $e');
    }
  }

  /// Quitar outfit guardado
  Future<void> unsaveOutfit(String outfitId) async {
    if (_currentUser == null) return;

    try {
      final success = await _outfitService.unsaveOutfit(
        userId: _currentUser!.id,
        outfitId: outfitId,
      );

      if (success) {
        // Actualizar el outfit en la lista local
        _updateOutfitInList(outfitId, (outfit) => outfit.copyWith(
          isSaved: false,
        ));

        // Remover de la lista de guardados si está ahí
        _savedOutfits.removeWhere((outfit) => outfit.id == outfitId);
        notifyListeners();
      }
    } catch (e) {
      setError('Error quitando outfit guardado: $e');
    }
  }

  /// Buscar outfits
  Future<List<Outfit>> searchOutfits(String query) async {
    try {
      clearError();
      return await _outfitService.searchOutfits(query: query);
    } catch (e) {
      setError('Error buscando outfits: $e');
      return [];
    }
  }

  /// Registrar vista de outfit
  Future<void> recordOutfitView(String outfitId, {double duration = 0.0}) async {
    if (_currentUser == null) return;

    try {
      await _outfitService.recordOutfitView(
        userId: _currentUser!.id,
        outfitId: outfitId,
        duration: duration,
      );
    } catch (e) {
      // No mostrar error para las vistas, solo log
      debugPrint('Error registrando vista: $e');
    }
  }

  /// Actualizar perfil de usuario
  Future<void> updateUserProfile({
    String? username,
    String? email,
    String? profileImage,
    String? bio,
  }) async {
    if (_currentUser == null) return;

    try {
      setLoading(true);
      clearError();

      final updatedUser = await _userService.updateUserProfile(
        userId: _currentUser!.id,
        username: username,
        email: email,
        profileImage: profileImage,
        bio: bio,
      );

      if (updatedUser != null) {
        _currentUser = updatedUser;
        notifyListeners();
      }
    } catch (e) {
      setError('Error actualizando perfil: $e');
    } finally {
      setLoading(false);
    }
  }

  /// Marcar notificación como leída
  Future<void> markNotificationAsRead(String notificationId) async {
    try {
      final success = await _rabbitmqService.markNotificationAsRead(notificationId);
      
      if (success) {
        // Actualizar la notificación en la lista local
        final index = _notifications.indexWhere((n) => n['id'] == notificationId);
        if (index != -1) {
          _notifications[index]['isRead'] = true;
          notifyListeners();
        }
      }
    } catch (e) {
      setError('Error marcando notificación como leída: $e');
    }
  }

  /// Verificar conexión con RabbitMQ
  Future<bool> checkConnection() async {
    try {
      return await _rabbitmqService.checkConnection();
    } catch (e) {
      setError('Error verificando conexión: $e');
      return false;
    }
  }

  /// Actualizar outfit en las listas locales
  void _updateOutfitInList(String outfitId, Outfit Function(Outfit) updateFunction) {
    // Actualizar en feed
    final feedIndex = _feedOutfits.indexWhere((outfit) => outfit.id == outfitId);
    if (feedIndex != -1) {
      _feedOutfits[feedIndex] = updateFunction(_feedOutfits[feedIndex]);
    }

    // Actualizar en guardados
    final savedIndex = _savedOutfits.indexWhere((outfit) => outfit.id == outfitId);
    if (savedIndex != -1) {
      _savedOutfits[savedIndex] = updateFunction(_savedOutfits[savedIndex]);
    }

    notifyListeners();
  }

  /// Configurar listeners de Socket.IO
  void _setupSocketListeners() {
    // Escuchar confirmación de reacción exitosa
    _socketService.onReactionSuccess((data) {
      print('✅ Reacción confirmada por servidor: $data');
    });
    
    // Escuchar error de reacción
    _socketService.onReactionError((data) {
      print('❌ Error en reacción: $data');
      setError('Error en reacción: ${data['error']}');
    });
    
    // Escuchar actualizaciones de outfit en tiempo real
    _socketService.onOutfitUpdated((data) {
      print('🔄 Outfit actualizado en tiempo real: $data');
      // Aquí podrías actualizar la UI si otros usuarios interactúan
      // Por ahora solo logueamos, pero podrías sincronizar el estado
    });
  }

  /// Limpiar datos al cerrar sesión
  void logout() {
    _currentUser = null;
    _feedOutfits.clear();
    _savedOutfits.clear();
    _notifications.clear();
    _error = null;
    _isLoading = false;
    _socketService.disconnect();
    notifyListeners();
  }
}