import 'package:flutter/material.dart';
import '../models/survey.dart';
import '../services/survey_service.dart';
import '../main.dart';

// Paleta de colores de The Clothesure
class ClothesureColors {
  static const Color azul = Color(0xFF3BAEB0);
  static const Color rojo = Color(0xFFE23F58);
  static const Color amarillo = Color(0xFFF59153);
  static const Color negro = Color(0xFF000000);
}

class InitialSurveyScreen extends StatefulWidget {
  const InitialSurveyScreen({super.key});

  @override
  State<InitialSurveyScreen> createState() => _InitialSurveyScreenState();
}

class _InitialSurveyScreenState extends State<InitialSurveyScreen> {
  final SurveyService _surveyService = SurveyService();
  List<SurveyQuestion> _questions = [];
  int _currentQuestionIndex = 0;
  Map<String, List<String>> _responses = {};
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadQuestions();
  }

  void _loadQuestions() {
    setState(() {
      _questions = SurveyService.getInitialSurveyQuestions();
    });
  }

  void _selectOption(String questionId, String optionId, String? value) {
    setState(() {
      final currentQuestion = _questions[_currentQuestionIndex];
      final selectedValue = value ?? optionId;
      
      if (!_responses.containsKey(questionId)) {
        _responses[questionId] = [];
      }
      
      // Determinar si es selección única o múltiple basado en el tipo de pregunta
      if (currentQuestion.id == '2' || currentQuestion.id == '3' || currentQuestion.id == '7') {
        // Selección múltiple
        if (_responses[questionId]!.contains(selectedValue)) {
          _responses[questionId]!.remove(selectedValue);
        } else {
          // Verificar límite máximo para pregunta 3 (máximo 3 selecciones)
          if (currentQuestion.id == '3' && _responses[questionId]!.length >= 3) {
            return; // No permitir más de 3 selecciones
          }
          _responses[questionId]!.add(selectedValue);
        }
      } else {
        // Selección única
        _responses[questionId] = [selectedValue];
      }
    });
  }

  void _nextQuestion() {
    if (_currentQuestionIndex < _questions.length - 1) {
      setState(() {
        _currentQuestionIndex++;
      });
    } else {
      _completeSurvey();
    }
  }

  void _previousQuestion() {
    if (_currentQuestionIndex > 0) {
      setState(() {
        _currentQuestionIndex--;
      });
    }
  }

  Future<void> _completeSurvey() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Convertir respuestas al formato correcto
      final surveyResponses = <SurveyResponse>[];
      for (final entry in _responses.entries) {
        for (final value in entry.value) {
          surveyResponses.add(SurveyResponse(
            questionId: entry.key,
            selectedOptionId: value,
            selectedValue: value,
            timestamp: DateTime.now(),
          ));
        }
      }

      // Guardar respuestas
      await _surveyService.saveSurveyResponses(surveyResponses);

      // Navegar al feed principal
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const HomeScreen()),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error al completar encuesta: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  bool get _canContinue {
    final currentQuestion = _questions[_currentQuestionIndex];
    final hasResponse = _responses.containsKey(currentQuestion.id) && 
                       _responses[currentQuestion.id]!.isNotEmpty;
    
    // Para pregunta 3, verificar que tenga al menos 1 selección
    if (currentQuestion.id == '3') {
      return hasResponse && _responses[currentQuestion.id]!.length >= 1;
    }
    
    return hasResponse;
  }

  @override
  Widget build(BuildContext context) {
    if (_questions.isEmpty) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final currentQuestion = _questions[_currentQuestionIndex];
    final isLastQuestion = _currentQuestionIndex == _questions.length - 1;

    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: Stack(
        children: [
          // Fondo con blur (simulando el feed)
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [ClothesureColors.azul, ClothesureColors.rojo],
              ),
            ),
            child: const Center(
              child: Text(
                'Posts',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'Roboto',
                ),
              ),
            ),
          ),
          
          // Modal de encuesta
          Center(
            child: Container(
              margin: const EdgeInsets.all(20),
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.85,
              ),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 20,
                    offset: const Offset(0, 10),
                  ),
                ],
              ),
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Indicador de progreso
                    Row(
                      children: [
                        Expanded(
                          child: LinearProgressIndicator(
                            value: (_currentQuestionIndex + 1) / _questions.length,
                            backgroundColor: Colors.grey[300],
                            valueColor: const AlwaysStoppedAnimation<Color>(ClothesureColors.azul),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Text(
                          '${_currentQuestionIndex + 1}/${_questions.length}',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[600],
                            fontWeight: FontWeight.w500,
                            fontFamily: 'Roboto',
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    
                    // Pregunta
                    Text(
                      currentQuestion.question,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                        fontFamily: 'Roboto',
                      ),
                      textAlign: TextAlign.center,
                    ),
                    
                    // Información adicional para selecciones múltiples
                    if (currentQuestion.id == '2' || currentQuestion.id == '3' || currentQuestion.id == '7')
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: Text(
                          currentQuestion.id == '3' 
                              ? 'Selecciona hasta 3 opciones'
                              : 'Puedes seleccionar múltiples opciones',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[600],
                            fontStyle: FontStyle.italic,
                            fontFamily: 'Roboto',
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ),
                    
                    const SizedBox(height: 24),
                    
                    // Opciones (con scroll si es necesario)
                    Flexible(
                      child: SingleChildScrollView(
                        child: Column(
                          children: currentQuestion.options.map((option) {
                            final isSelected = _responses[currentQuestion.id]?.contains(option.value) ?? false;
                            return Container(
                              margin: const EdgeInsets.only(bottom: 12),
                              child: InkWell(
                                onTap: () => _selectOption(
                                  currentQuestion.id,
                                  option.id,
                                  option.value,
                                ),
                                borderRadius: BorderRadius.circular(8),
                                child: Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 16,
                                    vertical: 12,
                                  ),
                                  decoration: BoxDecoration(
                                    color: isSelected ? ClothesureColors.azul.withOpacity(0.1) : Colors.grey[50],
                                    borderRadius: BorderRadius.circular(8),
                                    border: Border.all(
                                      color: isSelected ? ClothesureColors.azul : Colors.grey[300]!,
                                      width: isSelected ? 2 : 1,
                                    ),
                                  ),
                                  child: Row(
                                    children: [
                                      Icon(
                                        // Cambiar icono según tipo de selección
                                        (currentQuestion.id == '2' || currentQuestion.id == '3' || currentQuestion.id == '7')
                                            ? (isSelected ? Icons.check_box : Icons.check_box_outline_blank)
                                            : (isSelected ? Icons.radio_button_checked : Icons.radio_button_unchecked),
                                        color: isSelected ? ClothesureColors.azul : Colors.grey[400],
                                      ),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              option.text,
                                              style: TextStyle(
                                                fontSize: 16,
                                                color: isSelected ? ClothesureColors.azul : Colors.black87,
                                                fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                                                fontFamily: 'Roboto',
                                              ),
                                            ),
                                            // Mostrar contador para pregunta 3
                                            if (currentQuestion.id == '3' && isSelected)
                                              Text(
                                                '${_responses[currentQuestion.id]?.length ?? 0}/3',
                                                style: TextStyle(
                                                  fontSize: 12,
                                                  color: ClothesureColors.azul,
                                                  fontWeight: FontWeight.w500,
                                                  fontFamily: 'Roboto',
                                                ),
                                              ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Botones de navegación
                    Row(
                      children: [
                        // Botón Atrás
                        if (_currentQuestionIndex > 0)
                          Expanded(
                            child: OutlinedButton(
                              onPressed: _previousQuestion,
                              style: OutlinedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(vertical: 12),
                                side: BorderSide(color: Colors.grey[400]!),
                              ),
                              child: const Text(
                                'Atrás',
                                style: TextStyle(
                                  color: Colors.grey,
                                  fontFamily: 'Roboto',
                                ),
                              ),
                            ),
                          ),
                        
                        if (_currentQuestionIndex > 0) const SizedBox(width: 12),
                        
                        // Botón Continuar
                        Expanded(
                          child: ElevatedButton(
                            onPressed: _canContinue && !_isLoading
                                ? _nextQuestion
                                : null,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: ClothesureColors.azul,
                              padding: const EdgeInsets.symmetric(vertical: 12),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: _isLoading
                                ? const SizedBox(
                                    height: 20,
                                    width: 20,
                                    child: CircularProgressIndicator(
                                      color: Colors.white,
                                      strokeWidth: 2,
                                    ),
                                  )
                                : Text(
                                    isLastQuestion ? 'Personalizar' : 'Continuar',
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w600,
                                      fontFamily: 'Roboto',
                                    ),
                                  ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
          
        ],
      ),
    );
  }
}
