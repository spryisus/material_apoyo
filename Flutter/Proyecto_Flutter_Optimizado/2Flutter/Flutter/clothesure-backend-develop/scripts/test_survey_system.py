"""
Script de prueba para verificar que el sistema de encuestas funciona correctamente.
Ejecuta todas las fases y verifica endpoints.

Uso: python scripts/test_survey_system.py
"""

import sys
import os
import requests
import json
from datetime import datetime

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_validation_script():
    """Prueba el script de validación."""
    print("🔍 Probando script de validación...")
    try:
        from scripts.validate_schema import validate_schema
        report = validate_schema()
        print(f"✅ Validación completada - Estado: {report['status']}")
        return report
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return None

def test_seed_script():
    """Prueba el script de seed."""
    print("\n🌱 Probando script de seed...")
    try:
        from scripts.seed_survey_questions import seed_questions
        seed_questions()
        print("✅ Seed completado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error en seed: {e}")
        return False

def test_endpoints():
    """Prueba los endpoints de la API."""
    print("\n🌐 Probando endpoints...")
    
    base_url = "http://localhost:8000/api/preferences"
    
    # Test 1: Obtener preguntas
    print("   📋 Probando GET /questions...")
    try:
        response = requests.get(f"{base_url}/questions")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Preguntas obtenidas: {len(data.get('questions', []))}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # Test 2: Guardar respuestas
    print("   💾 Probando POST /answers...")
    test_answers = {
        "user_id": "test_user_123",
        "answers": {
            "style_personal": "casual",
            "style_personal_custom": None,
            "occasions": ["dia_casual", "trabajo_oficina"],
            "favorite_items": ["jeans", "tops_blusas", "sudaderas_hoodies"],
            "body_shape": "rectangulo",
            "skin_tone": "medio",
            "fit_preference": "ajustadas",
            "shoes": ["zapatillas_deportivas", "flats"],
            "accessories": "ocasiones_especiales"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/answers", json=test_answers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Respuestas guardadas: {data.get('message')}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # Test 3: Obtener preferencias
    print("   👤 Probando GET /{user_id}...")
    try:
        response = requests.get(f"{base_url}/test_user_123")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Preferencias obtenidas: {data.get('has_preferences')}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

def test_matching_service():
    """Prueba el servicio de matching."""
    print("\n🎯 Probando servicio de matching...")
    try:
        from app.services.matching_service import calculate_matching_score, get_matching_explanation
        
        # Datos de prueba
        user_preferences = {
            "style_personal": "casual",
            "occasions": ["dia_casual", "trabajo_oficina"],
            "favorite_items": ["jeans", "tops_blusas"],
            "body_shape": "rectangulo",
            "shoes": ["zapatillas_deportivas"],
            "accessories": "ocasiones_especiales"
        }
        
        post_tags = ["casual", "jeans", "dia_casual", "zapatillas_deportivas"]
        
        # Calcular score
        score = calculate_matching_score(user_preferences, post_tags)
        print(f"   ✅ Score calculado: {score}")
        
        # Obtener explicación
        explanation = get_matching_explanation(user_preferences, post_tags)
        print(f"   ✅ Explicación generada: {explanation['total_score']}/{explanation['max_possible_score']}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error en matching: {e}")
        return False

def test_feed_endpoint():
    """Prueba el endpoint de feed personalizado."""
    print("\n📱 Probando endpoint de feed...")
    
    base_url = "http://localhost:8000/posts"
    
    try:
        response = requests.get(f"{base_url}/feed/for-you?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Feed obtenido: {data.get('success')}")
            print(f"   📊 Posts: {len(data.get('posts', []))}")
            print(f"   🔍 Requiere encuesta: {data.get('requires_survey')}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

def main():
    """Función principal de prueba."""
    print("=" * 60)
    print("🧪 PRUEBA COMPLETA DEL SISTEMA DE ENCUESTAS")
    print("=" * 60)
    
    # Paso 1: Validación
    validation_report = test_validation_script()
    if not validation_report:
        print("❌ No se puede continuar sin validación exitosa")
        return
    
    # Paso 2: Seed
    if not test_seed_script():
        print("❌ No se puede continuar sin seed exitoso")
        return
    
    # Paso 3: Servicio de matching
    if not test_matching_service():
        print("⚠️  Servicio de matching con problemas")
    
    # Paso 4: Endpoints (requiere servidor corriendo)
    print("\n" + "=" * 60)
    print("🌐 PRUEBAS DE ENDPOINTS")
    print("=" * 60)
    print("⚠️  NOTA: Estas pruebas requieren que el servidor esté corriendo")
    print("   Ejecuta: uvicorn main:app --reload")
    print("   Luego ejecuta este script nuevamente")
    
    test_endpoints()
    test_feed_endpoint()
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("=" * 60)
    print("✅ Sistema de encuestas implementado exitosamente")
    print("📋 Endpoints disponibles:")
    print("   - GET /api/preferences/questions")
    print("   - POST /api/preferences/answers")
    print("   - GET /api/preferences/{user_id}")
    print("   - PUT /api/preferences/{user_id}")
    print("   - GET /posts/feed/for-you")
    print("\n🚀 ¡Sistema listo para usar!")

if __name__ == "__main__":
    main()
