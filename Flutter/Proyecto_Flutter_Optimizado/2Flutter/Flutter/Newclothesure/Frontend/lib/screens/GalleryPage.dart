import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io'; //para el tipo de archivo

// Paleta de colores de The Clothesure
class ClothesureColors {
  static const Color azul = Color(0xFF3BAEB0);
  static const Color rojo = Color(0xFFE23F58);
  static const Color amarillo = Color(0xFFF59153);
  static const Color negro = Color(0xFF000000);
}

//Subir outfit
class GalleryPage extends StatefulWidget {
  const GalleryPage({super.key});

  @override
  State<GalleryPage> createState() => _GalleryPageState();
}

class _GalleryPageState extends State<GalleryPage> {
  final ImagePicker _picker = ImagePicker(); 
  List<File> _imagenesSeleccionadas = [];//enlista todas las imagenes
  Set<File> _selectImages = {}; //conjunto de imagenes seleccionadas

  Future<void> getImagesFromGallery() async {
    final List<XFile> imagenes = await _picker.pickMultiImage();
    if (imagenes.isNotEmpty) {
      setState(() {
        // Limita a un máximo de 3 imágenes
        _imagenesSeleccionadas =
            imagenes.take(3).map((xFile) => File(xFile.path)).toList();
            _selectImages.clear(); //Limpia la seccion anterior
      });
    }
  }

  // Widget para mostrar las imágenes según la cantidad
  Widget _buildImageContainer() {
    if (_imagenesSeleccionadas.isEmpty) {
      return const Center(child: Text('No hay imágenes seleccionadas'));
    }

    // Caso 1: Una sola imagen
    if (_imagenesSeleccionadas.length == 1) {
      return Image.file(
        _imagenesSeleccionadas.first,
        fit: BoxFit.cover,
      );
    }

    // Caso 2: Dos imágenes
    if (_imagenesSeleccionadas.length == 2) {
      return Row(
        children: _imagenesSeleccionadas.map((imageFile) {
          return Expanded(
            child: Padding(
              padding: const EdgeInsets.all(4.0),
              child: Image.file(imageFile, fit: BoxFit.cover),
            ),
          );
        }).toList(),
      );
    }

    // Caso 3: Tres imágenes (o más, pero limitadas a 3)
    if (_imagenesSeleccionadas.length >= 3) {
      return Row(
        children: [
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(4.0),
              child:
                  Image.file(_imagenesSeleccionadas.first, fit: BoxFit.cover),
            ),
          ),
          Expanded(
            child: Column(
              children: [
                Expanded(
                  flex: 1,
                  child: Padding(
                    padding: const EdgeInsets.all(4.0),
                    child: Image.file(_imagenesSeleccionadas[1],
                        fit: BoxFit.cover),
                  ),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(4.0),
                    child: Image.file(_imagenesSeleccionadas[2],
                        fit: BoxFit.cover),
                  ),
                ),
              ],
            ),
          ),
        ],
      );
    }

    // Alternativa por defecto
    return const SizedBox.shrink();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'Subir Outfit',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white,
            fontFamily: 'Roboto',
          ),
        ),
        backgroundColor: ClothesureColors.negro,
        elevation: 0,
        actions: [
          TextButton(
            onPressed: () {
              // Lógica para subir el outfit
            },
            child: const Text(
              'Subir',
              style: TextStyle(
                color: ClothesureColors.azul,
                fontWeight: FontWeight.bold,
                fontSize: 16,
                fontFamily: 'Roboto',
              ),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start, // Alinea el contenido a la izquierda
          children: [
            // Área de carga de imagen
            Container(
              height: 300,
              width: double.infinity,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(10),
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: _buildImageContainer(),
              ),
            ),
            const SizedBox(height: 10),
            Center(
              child: Text('Imágenes seleccionadas: ${_imagenesSeleccionadas.length}/3'),
            ),
            const SizedBox(height: 10),
            Center(
              child: ElevatedButton.icon(
                onPressed: getImagesFromGallery,
                icon: const Icon(Icons.photo_library),
                label: const Text('Seleccionar imágenes'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: ClothesureColors.azul,
                  foregroundColor: Colors.white,
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Título del post
            const Text(
              'Título del outfit',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              decoration: InputDecoration(
                hintText: 'Ej: Look elegante para oficina',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(
                    color: ClothesureColors.azul,
                    width: 2,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Descripción
            const Text(
              'Descripción',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'Describe tu outfit, dónde lo usarías, etc.',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(
                    color: ClothesureColors.azul,
                    width: 2,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Hashtags
            const Text(
              'Hashtags',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              decoration: InputDecoration(
                hintText: '#Elegante #Oficina #Profesional',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(
                    color: ClothesureColors.azul,
                    width: 2,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 30),

            // Botón de compartir
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  backgroundColor: ClothesureColors.azul,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  'Subir Outfit',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}