/// Modelo de Reacción para The Clothesure
class Reaction {
  final String id;
  final String userId;
  final String outfitId;
  final String action; // 'like' o 'unlike'
  final DateTime timestamp;
  final Map<String, dynamic>? metadata;

  const Reaction({
    required this.id,
    required this.userId,
    required this.outfitId,
    required this.action,
    required this.timestamp,
    this.metadata,
  });

  /// Crear reacción desde JSON
  factory Reaction.fromJson(Map<String, dynamic> json) {
    return Reaction(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      outfitId: json['outfit_id'] as String,
      action: json['action'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }

  /// Convertir reacción a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'outfit_id': outfitId,
      'action': action,
      'timestamp': timestamp.toIso8601String(),
      'metadata': metadata,
    };
  }

  /// Crear reacción para RabbitMQ
  factory Reaction.forRabbitMQ({
    required String userId,
    required String outfitId,
    required String action,
    Map<String, dynamic>? metadata,
  }) {
    return Reaction(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      userId: userId,
      outfitId: outfitId,
      action: action,
      timestamp: DateTime.now(),
      metadata: metadata,
    );
  }

  /// Convertir a mensaje RabbitMQ
  Map<String, dynamic> toRabbitMQMessage() {
    return {
      'tipo': 'reaccion',
      'usuario_id': userId,
      'outfit_id': outfitId,
      'accion': action,
      'timestamp': timestamp.millisecondsSinceEpoch / 1000.0,
      'metadata': metadata ?? {},
    };
  }

  /// Verificar si es like
  bool get isLike => action == 'like';

  /// Verificar si es unlike
  bool get isUnlike => action == 'unlike';

  @override
  String toString() {
    return 'Reaction(user: $userId, outfit: $outfitId, action: $action)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Reaction && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
