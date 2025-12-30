import 'package:flutter/material.dart';

class ClothesureIcon extends StatelessWidget {
  final double size;
  final Color? color;

  const ClothesureIcon({
    super.key,
    this.size = 24.0,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size),
      painter: ClothesureIconPainter(
        color: color ?? const Color.fromARGB(255, 0, 0, 0),
      ),
    );
  }
}

class ClothesureIconPainter extends CustomPainter {
  final Color color;

  ClothesureIconPainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final centerX = size.width / 2;
    final centerY = size.height / 2;
    final radius = size.width * 0.35;

    // Fondo circular morado oscuro
    final circlePaint = Paint()
      ..color = const Color.fromARGB(255, 2, 2, 2);
    canvas.drawCircle(Offset(centerX, centerY), radius, circlePaint);

    // Colores para las perchas (crema/beige claro)
    final perchColor = const Color(0xFFF5F5DC);
    final strokePaint = Paint()
      ..color = perchColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = size.width * 0.06
      ..strokeCap = StrokeCap.round;

    final fillPaint = Paint()
      ..color = perchColor
      ..style = PaintingStyle.fill;

    // Dibujar el corazón (parte superior de la percha central)
    final heartPath = Path();
    final heartSize = radius * 0.25;
    heartPath.moveTo(centerX, centerY - heartSize * 0.6);
    heartPath.cubicTo(
      centerX - heartSize * 0.3, centerY - heartSize * 0.9,
      centerX - heartSize * 0.6, centerY - heartSize * 0.6,
      centerX - heartSize * 0.6, centerY - heartSize * 0.3,
    );
    heartPath.cubicTo(
      centerX - heartSize * 0.6, centerY - heartSize * 0.1,
      centerX - heartSize * 0.3, centerY - heartSize * 0.1,
      centerX, centerY - heartSize * 0.3,
    );
    heartPath.cubicTo(
      centerX + heartSize * 0.3, centerY - heartSize * 0.1,
      centerX + heartSize * 0.6, centerY - heartSize * 0.1,
      centerX + heartSize * 0.6, centerY - heartSize * 0.3,
    );
    heartPath.cubicTo(
      centerX + heartSize * 0.6, centerY - heartSize * 0.6,
      centerX + heartSize * 0.3, centerY - heartSize * 0.9,
      centerX, centerY - heartSize * 0.6,
    );
    heartPath.close();

    canvas.drawPath(heartPath, fillPaint);

    // Dibujar las perchas
    // Percha central (con corazón)
    canvas.drawLine(
      Offset(centerX, centerY - heartSize * 0.3),
      Offset(centerX, centerY + radius * 0.4),
      strokePaint,
    );
    canvas.drawLine(
      Offset(centerX - radius * 0.25, centerY + radius * 0.2),
      Offset(centerX + radius * 0.25, centerY + radius * 0.2),
      strokePaint,
    );

    // Percha izquierda (más atrás)
    final leftPerchX = centerX - radius * 0.4;
    final leftPerchY = centerY - radius * 0.1;
    canvas.drawLine(
      Offset(leftPerchX, leftPerchY),
      Offset(leftPerchX, leftPerchY + radius * 0.3),
      strokePaint,
    );
    canvas.drawLine(
      Offset(leftPerchX - radius * 0.15, leftPerchY + radius * 0.15),
      Offset(leftPerchX + radius * 0.15, leftPerchY + radius * 0.15),
      strokePaint,
    );

    // Percha derecha (más atrás)
    final rightPerchX = centerX + radius * 0.4;
    final rightPerchY = centerY - radius * 0.1;
    canvas.drawLine(
      Offset(rightPerchX, rightPerchY),
      Offset(rightPerchX, rightPerchY + radius * 0.3),
      strokePaint,
    );
    canvas.drawLine(
      Offset(rightPerchX - radius * 0.15, rightPerchY + radius * 0.15),
      Offset(rightPerchX + radius * 0.15, rightPerchY + radius * 0.15),
      strokePaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
