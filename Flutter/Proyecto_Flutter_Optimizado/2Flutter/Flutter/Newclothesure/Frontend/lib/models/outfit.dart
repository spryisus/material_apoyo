/// Modelo de Outfit para The Clothesure
class Outfit {
  final String id;
  final String userId;
  final String? username;
  final String? profileImage;
  final String title;
  final String description;
  final List<String> images;
  final List<String> hashtags;
  final int likesCount;
  final int commentsCount;
  final int viewsCount;
  final bool isLiked;
  final bool isSaved;
  final DateTime createdAt;
  final DateTime updatedAt;
  final Map<String, dynamic>? metadata;

  const Outfit({
    required this.id,
    required this.userId,
    this.username,
    this.profileImage,
    required this.title,
    required this.description,
    required this.images,
    required this.hashtags,
    required this.likesCount,
    required this.commentsCount,
    required this.viewsCount,
    required this.isLiked,
    required this.isSaved,
    required this.createdAt,
    required this.updatedAt,
    this.metadata,
  });

  /// Crear outfit desde JSON
  factory Outfit.fromJson(Map<String, dynamic> json) {
    return Outfit(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      username: json['username'] as String?,
      profileImage: json['profile_image'] as String?,
      title: json['title'] as String,
      description: json['description'] as String,
      images: List<String>.from(json['images'] as List),
      hashtags: List<String>.from(json['hashtags'] as List? ?? []),
      likesCount: json['likes_count'] as int? ?? 0,
      commentsCount: json['comments_count'] as int? ?? 0,
      viewsCount: json['views_count'] as int? ?? 0,
      isLiked: json['is_liked'] as bool? ?? false,
      isSaved: json['is_saved'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }

  /// Convertir outfit a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'username': username,
      'profile_image': profileImage,
      'title': title,
      'description': description,
      'images': images,
      'hashtags': hashtags,
      'likes_count': likesCount,
      'comments_count': commentsCount,
      'views_count': viewsCount,
      'is_liked': isLiked,
      'is_saved': isSaved,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'metadata': metadata,
    };
  }

  /// Crear copia con cambios
  Outfit copyWith({
    String? id,
    String? userId,
    String? username,
    String? profileImage,
    String? title,
    String? description,
    List<String>? images,
    List<String>? hashtags,
    int? likesCount,
    int? commentsCount,
    int? viewsCount,
    bool? isLiked,
    bool? isSaved,
    DateTime? createdAt,
    DateTime? updatedAt,
    Map<String, dynamic>? metadata,
  }) {
    return Outfit(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      username: username ?? this.username,
      profileImage: profileImage ?? this.profileImage,
      title: title ?? this.title,
      description: description ?? this.description,
      images: images ?? this.images,
      hashtags: hashtags ?? this.hashtags,
      likesCount: likesCount ?? this.likesCount,
      commentsCount: commentsCount ?? this.commentsCount,
      viewsCount: viewsCount ?? this.viewsCount,
      isLiked: isLiked ?? this.isLiked,
      isSaved: isSaved ?? this.isSaved,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      metadata: metadata ?? this.metadata,
    );
  }

  /// Obtener imagen principal
  String get mainImage => images.isNotEmpty ? images.first : '';

  /// Verificar si tiene hashtags
  bool get hasHashtags => hashtags.isNotEmpty;

  /// Obtener hashtags como string
  String get hashtagsString => hashtags.map((tag) => '#$tag').join(' ');

  @override
  String toString() {
    return 'Outfit(id: $id, title: $title, likes: $likesCount)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Outfit && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
