import 'package:flutter/material.dart';

// Paleta de colores de The Clothesure
class ClothesureColors {
  static const Color azul = Color(0xFF3BAEB0);
  static const Color rojo = Color(0xFFE23F58);
  static const Color amarillo = Color(0xFFF59153);
  static const Color negro = Color(0xFF000000);
}

class Progresscard extends StatefulWidget {
  final int totalHooks;
  final int hooksLeft;
  final Color progressColor;

  const Progresscard({
    Key? key,
    required this.totalHooks,
    required this.hooksLeft,
    required this.progressColor,
  }) : super(key: key);

  @override
  State<Progresscard> createState() => _ProgresscardState();
}

class _ProgresscardState extends State<Progresscard> {
  @override
  Widget build(BuildContext context) {
    final double progressValue = widget.hooksLeft / widget.totalHooks;
    
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      color: Colors.black,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Hooks restantes: ${widget.hooksLeft}',
              style: const TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            LinearProgressIndicator(
              value: progressValue,
              backgroundColor: Colors.grey[800],
              valueColor: AlwaysStoppedAnimation<Color>(widget.progressColor),
            ),
            const SizedBox(height: 8),
            Text(
              '${(progressValue * 100).toStringAsFixed(1)}% completado',
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }
}