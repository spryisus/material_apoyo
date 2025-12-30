import 'package:flutter/material.dart';

// Paleta de colores de The Clothesure
class ClothesureColors {
  static const Color azul = Color(0xFF3BAEB0);
  static const Color rojo = Color(0xFFE23F58);
  static const Color amarillo = Color(0xFFF59153);
  static const Color negro = Color(0xFF000000);
}

//Perfil
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'Perfil',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
            fontFamily: 'Roboto',
          ),
        ),
        backgroundColor: ClothesureColors.negro,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.close, color: Colors.white),
            onPressed: () {},
          ),
        ],
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color.fromARGB(255, 255, 255, 255), // Vino
              Color.fromARGB(255, 255, 255, 255), // Vino más oscuro
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              children: [
                const CircleAvatar(
                  radius: 50,
                  backgroundColor: Color.fromARGB(255, 145, 145, 145),
                  child: Icon(
                    Icons.person,
                    size: 50,
                    color: Color(0xFF8B1538),
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  '[Perfil]',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.location_on,
                      color: Colors.white70,
                      size: 16,
                    ),
                    const SizedBox(width: 5),
                    Text(
                      'Ubicación',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white.withOpacity(0.8),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 40),
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Column(
                      children: [
                        const SizedBox(height: 20),
                        _buildMenuItem(
                          icon: Icons.person_outline,
                          title: 'Información personal',
                        ),
                        _buildMenuItem(
                          icon: Icons.notifications_outlined,
                          title: 'Notificaciones',
                        ),
                        _buildMenuItem(
                          icon: Icons.list_alt_outlined,
                          title: 'Lista de deseos',
                        ),
                        _buildMenuItem(
                          icon: Icons.favorite_outline,
                          title: 'Guardado',
                        ),
                        _buildMenuItem(
                          icon: Icons.logout,
                          title: 'Cerrar sesión',
                          isLogout: true,
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String title,
    bool isLogout = false,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 5),
      child: ListTile(
        leading: Icon(
          icon,
          color: isLogout ? Colors.red : const Color(0xFF8B1538),
        ),
        title: Text(
          title,
          style: TextStyle(
            color: isLogout ? Colors.red : Colors.black,
            fontWeight: FontWeight.w500,
          ),
        ),
        trailing: const Icon(
          Icons.arrow_forward_ios,
          size: 16,
          color: Colors.grey,
        ),
        onTap: () {},
      ),
    );
  }
}