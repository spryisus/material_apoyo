import 'package:flutter/foundation.dart';
import '../models/survey.dart';

class SurveyService {

  // Preguntas de la encuesta inicial (basadas en el backend real)
  static List<SurveyQuestion> getInitialSurveyQuestions() {
    return [
      SurveyQuestion(
        id: '1',
        question: '¿Cómo describirías tu estilo personal?',
        options: [
          SurveyOption(id: 'casual', text: 'Casual', value: 'casual'),
          SurveyOption(id: 'clasico', text: 'Clásico', value: 'clasico'),
          SurveyOption(id: 'bohemio', text: 'Bohemio', value: 'bohemio'),
          SurveyOption(id: 'moderno_minimalista', text: 'Moderno/Minimalista', value: 'moderno_minimalista'),
          SurveyOption(id: 'deportivo', text: 'Deportivo', value: 'deportivo'),
          SurveyOption(id: 'elegante', text: 'Elegante', value: 'elegante'),
          SurveyOption(id: 'creativo_vanguardista', text: 'Creativo/Vanguardista', value: 'creativo_vanguardista'),
          SurveyOption(id: 'otro', text: 'Otro', value: 'otro'),
        ],
        category: 'style',
      ),
      SurveyQuestion(
        id: '2',
        question: '¿Para qué ocasiones te vistes con más frecuencia?',
        options: [
          SurveyOption(id: 'dia_casual', text: 'Día a día/Casual', value: 'dia_casual'),
          SurveyOption(id: 'trabajo_oficina', text: 'Trabajo/Oficina', value: 'trabajo_oficina'),
          SurveyOption(id: 'eventos_especiales', text: 'Eventos especiales (bodas, fiestas)', value: 'eventos_especiales'),
          SurveyOption(id: 'salidas_nocturnas', text: 'Salidas nocturnas', value: 'salidas_nocturnas'),
          SurveyOption(id: 'aire_libre', text: 'Actividades al aire libre', value: 'aire_libre'),
        ],
        category: 'occasion',
      ),
      SurveyQuestion(
        id: '3',
        question: '¿Qué prendas de vestir son tus favoritas o las que más usas? (Selecciona hasta 3)',
        options: [
          SurveyOption(id: 'jeans', text: 'Jeans', value: 'jeans'),
          SurveyOption(id: 'vestidos', text: 'Vestidos', value: 'vestidos'),
          SurveyOption(id: 'faldas', text: 'Faldas', value: 'faldas'),
          SurveyOption(id: 'pantalones_vestir', text: 'Pantalones de vestir', value: 'pantalones_vestir'),
          SurveyOption(id: 'tops_blusas', text: 'Tops/Blusas', value: 'tops_blusas'),
          SurveyOption(id: 'sudaderas_hoodies', text: 'Sudaderas/Hoodies', value: 'sudaderas_hoodies'),
          SurveyOption(id: 'blazers_chaquetas', text: 'Blazers/Chaquetas', value: 'blazers_chaquetas'),
          SurveyOption(id: 'abrigos', text: 'Abrigos', value: 'abrigos'),
        ],
        category: 'clothing',
      ),
      SurveyQuestion(
        id: '4',
        question: '¿Qué forma tiene tu cuerpo?',
        options: [
          SurveyOption(id: 'reloj_arena', text: 'Reloj de arena', value: 'reloj_arena'),
          SurveyOption(id: 'triangulo_invertido', text: 'Triángulo invertido', value: 'triangulo_invertido'),
          SurveyOption(id: 'triangulo_pera', text: 'Triángulo/Pera', value: 'triangulo_pera'),
          SurveyOption(id: 'rectangulo', text: 'Rectángulo', value: 'rectangulo'),
          SurveyOption(id: 'manzana', text: 'Manzana', value: 'manzana'),
        ],
        category: 'body_type',
      ),
      SurveyQuestion(
        id: '5',
        question: '¿Cómo describirías tu tono de piel?',
        options: [
          SurveyOption(id: 'muy_claro', text: 'Muy claro/Pálido', value: 'muy_claro'),
          SurveyOption(id: 'claro', text: 'Claro', value: 'claro'),
          SurveyOption(id: 'medio', text: 'Medio', value: 'medio'),
          SurveyOption(id: 'bronceado', text: 'Bronceado', value: 'bronceado'),
          SurveyOption(id: 'oscuro', text: 'Oscuro', value: 'oscuro'),
        ],
        category: 'skin_tone',
      ),
      SurveyQuestion(
        id: '6',
        question: '¿Prefieres que las prendas sean...?',
        options: [
          SurveyOption(id: 'holgadas', text: 'Holgadas', value: 'holgadas'),
          SurveyOption(id: 'ajustadas', text: 'Ajustadas', value: 'ajustadas'),
          SurveyOption(id: 'depende_prenda', text: 'Depende de la prenda', value: 'depende_prenda'),
        ],
        category: 'fit_preference',
      ),
      SurveyQuestion(
        id: '7',
        question: '¿Qué tipo de calzado usas más a menudo? (Selecciona las que apliquen)',
        options: [
          SurveyOption(id: 'zapatillas_deportivas', text: 'Zapatillas deportivas', value: 'zapatillas_deportivas'),
          SurveyOption(id: 'botas', text: 'Botas', value: 'botas'),
          SurveyOption(id: 'tacones', text: 'Tacones', value: 'tacones'),
          SurveyOption(id: 'sandalias', text: 'Sandalias', value: 'sandalias'),
          SurveyOption(id: 'mocasines', text: 'Mocasines', value: 'mocasines'),
          SurveyOption(id: 'flats', text: 'Flats', value: 'flats'),
          SurveyOption(id: 'plataformas', text: 'Plataformas', value: 'plataformas'),
        ],
        category: 'footwear',
      ),
      SurveyQuestion(
        id: '8',
        question: '¿Te gusta usar accesorios?',
        options: [
          SurveyOption(id: 'siempre', text: 'Sí, siempre', value: 'siempre'),
          SurveyOption(id: 'ocasiones_especiales', text: 'A veces, para ocasiones especiales', value: 'ocasiones_especiales'),
          SurveyOption(id: 'raramente_nunca', text: 'Raramente o nunca', value: 'raramente_nunca'),
        ],
        category: 'accessories',
      ),
    ];
  }

  // Guardar respuestas de la encuesta
  Future<void> saveSurveyResponses(List<SurveyResponse> responses) async {
    try {
      // Aquí podrías guardar en SharedPreferences o enviar al backend
      debugPrint('Encuesta completada con ${responses.length} respuestas');
      
      // Simular guardado exitoso
      await Future.delayed(const Duration(milliseconds: 500));
      
    } catch (e) {
      debugPrint('Error guardando encuesta: $e');
      throw Exception('Error al guardar las respuestas');
    }
  }

  // Verificar si el usuario ya completó la encuesta
  Future<bool> hasCompletedSurvey() async {
    // Por ahora retornamos false para que siempre muestre la encuesta
    // En producción, esto verificaría en SharedPreferences o backend
    return false;
  }

  // Obtener preferencias del usuario
  Future<UserPreferences?> getUserPreferences() async {
    // Por ahora retornamos null
    // En producción, esto cargaría desde SharedPreferences o backend
    return null;
  }
}
