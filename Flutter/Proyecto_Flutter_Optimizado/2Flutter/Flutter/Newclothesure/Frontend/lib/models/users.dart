
class User {
  final int? userId;
  final String? fullName;
  final String? email;
  final String? accessToken;
  final String? sessionToken;

  User({
    this.userId,
    this.fullName,
    this.email,
    this.accessToken,
    this.sessionToken,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      userId: json['user_id'],
      fullName: json['full_name'],
      email: json['email'],
      accessToken: json['access_token'],
      sessionToken: json['session_token'],
    );
  }

  Map<String, dynamic> toJson() => {
        'user_id': userId,
        'full_name': fullName,
        'email': email,
        'access_token': accessToken,
        'session_token': sessionToken,
      };
}