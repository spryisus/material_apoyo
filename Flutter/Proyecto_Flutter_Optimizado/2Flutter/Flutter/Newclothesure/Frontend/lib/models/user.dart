/// Modelo de Usuario para The Clothesure
class User {
  final String id;
  final String username;
  final String email;
  final String? profileImage;
  final String? bio;
  final DateTime createdAt;
  final DateTime updatedAt;
  final Map<String, dynamic>? metadata;

  const User({
    required this.id,
    required this.username,
    required this.email,
    this.profileImage,
    this.bio,
    required this.createdAt,
    required this.updatedAt,
    this.metadata,
  });

  /// Crear usuario desde JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      username: json['username'] as String,
      email: json['email'] as String,
      profileImage: json['profile_image'] as String?,
      bio: json['bio'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }

  /// Convertir usuario a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'profile_image': profileImage,
      'bio': bio,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'metadata': metadata,
    };
  }

  /// Crear copia con cambios
  User copyWith({
    String? id,
    String? username,
    String? email,
    String? profileImage,
    String? bio,
    DateTime? createdAt,
    DateTime? updatedAt,
    Map<String, dynamic>? metadata,
  }) {
    return User(
      id: id ?? this.id,
      username: username ?? this.username,
      email: email ?? this.email,
      profileImage: profileImage ?? this.profileImage,
      bio: bio ?? this.bio,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      metadata: metadata ?? this.metadata,
    );
  }

  @override
  String toString() {
    return 'User(id: $id, username: $username, email: $email)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
