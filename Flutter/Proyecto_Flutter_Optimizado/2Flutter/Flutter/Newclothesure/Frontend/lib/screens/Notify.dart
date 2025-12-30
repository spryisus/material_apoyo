import 'package:flutter/material.dart';

// Paleta de colores de The Clothesure
class ClothesureColors {
  static const Color azul = Color(0xFF3BAEB0);
  static const Color rojo = Color(0xFFE23F58);
  static const Color amarillo = Color(0xFFF59153);
  static const Color negro = Color(0xFF000000);
}

class Notify extends StatefulWidget {
  const Notify({super.key});

  @override
  State<Notify> createState() => _NotifyState();
}

class _NotifyState extends State<Notify> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Row(
          children: [
             Text(
              'Notificaciones',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                letterSpacing: 1.2,
                fontFamily: 'Roboto',
              ),
            ),
          ],
        ),
        backgroundColor: ClothesureColors.negro,
        elevation: 0,
      ),
    );
  }
}
