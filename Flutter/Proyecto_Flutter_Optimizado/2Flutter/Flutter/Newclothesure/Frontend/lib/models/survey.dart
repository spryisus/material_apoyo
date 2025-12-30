class SurveyQuestion {
  final String id;
  final String question;
  final List<SurveyOption> options;
  final String? category;
  final bool isRequired;

  SurveyQuestion({
    required this.id,
    required this.question,
    required this.options,
    this.category,
    this.isRequired = true,
  });
}

class SurveyOption {
  final String id;
  final String text;
  final String? value;
  final bool isSelected;

  SurveyOption({
    required this.id,
    required this.text,
    this.value,
    this.isSelected = false,
  });

  SurveyOption copyWith({
    String? id,
    String? text,
    String? value,
    bool? isSelected,
  }) {
    return SurveyOption(
      id: id ?? this.id,
      text: text ?? this.text,
      value: value ?? this.value,
      isSelected: isSelected ?? this.isSelected,
    );
  }
}

class SurveyResponse {
  final String questionId;
  final String selectedOptionId;
  final String? selectedValue;
  final DateTime timestamp;

  SurveyResponse({
    required this.questionId,
    required this.selectedOptionId,
    this.selectedValue,
    required this.timestamp,
  });
}

class UserPreferences {
  final List<SurveyResponse> responses;
  final DateTime completedAt;
  final bool isCompleted;

  UserPreferences({
    required this.responses,
    required this.completedAt,
    this.isCompleted = false,
  });

  // Método para obtener preferencias específicas
  String? getStylePreference() {
    final styleResponse = responses.firstWhere(
      (response) => response.questionId == 'style_preference',
      orElse: () => SurveyResponse(
        questionId: '',
        selectedOptionId: '',
        timestamp: DateTime.now(),
      ),
    );
    return styleResponse.selectedValue;
  }

  List<String> getSelectedStyles() {
    return responses
        .where((response) => response.questionId == 'style_preference')
        .map((response) => response.selectedValue ?? '')
        .where((value) => value.isNotEmpty)
        .toList();
  }
}

