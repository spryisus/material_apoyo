import 'package:flutter/material.dart';
import 'package:the_clothesure_app/main.dart';
import 'package:the_clothesure_app/services/AuthService.dart';
import 'package:the_clothesure_app/services/survey_service.dart';
import 'package:the_clothesure_app/screens/InitialSurveyScreen.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final AuthService _authService = AuthService();
  final SurveyService _surveyService = SurveyService();
  bool _isLoading = false;

  Future<void> _Login() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);

      try {
        await _authService.login(
          _emailController.text,
          _passwordController.text,
        );

        setState(() => _isLoading = false);

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Sesión iniciada correctamente')),
        );

        // Verificar si el usuario ya completó la encuesta
        final hasCompletedSurvey = await _surveyService.hasCompletedSurvey();
        
        if (hasCompletedSurvey) {
          // Si ya completó la encuesta, ir al feed principal
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => const HomeScreen()),
          );
        } else {
          // Si no ha completado la encuesta, mostrar la encuesta inicial
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => const InitialSurveyScreen()),
          );
        }
      } catch (e) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Credenciales incorrectas')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Iniciar Sesion')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(10.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                const SizedBox(height: 5),
                Container(
                  padding: const EdgeInsets.all(10),
                  child: Image.asset(
                    'assets/images/logon.png',
                    width: 200,
                    height: 150,
                  ),
                ),
                const Text(
                  'Bienvenido a The Clothesure',
                  style: TextStyle(fontSize: 20),
                ),
                const SizedBox(height: 20),
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: 'Correo Electronico',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.email),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) return 'Ingrese su correo';
                    if (!value.contains('@')) return 'Ingrese un correo valido';
                    return null;
                  },
                ),
                const SizedBox(height: 16.0),
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Contraseña',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.lock),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) return 'Ingrese su contraseña';
                    if (value.length < 3) return 'La contraseña debe tener al menos 3 caracteres';
                    return null;
                  },
                ),
                const SizedBox(height: 24.0),
                ElevatedButton(
                  onPressed: _isLoading ? null : _Login,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16.0, horizontal: 80),
                    textStyle: const TextStyle(fontSize: 18),
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.blue)
                      : const Text('Iniciar Sesion'),
                ),
                const SizedBox(height: 15),
                const Text(
                  'Olvide mi contraseña',
                  style: TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 15),
                const Text(
                  'Crear cuenta',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
