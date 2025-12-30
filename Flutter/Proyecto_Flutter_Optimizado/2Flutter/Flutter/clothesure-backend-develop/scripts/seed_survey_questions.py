"""
Script de seed para insertar las 8 preguntas de la encuesta inicial.
Modo síncrono, sin async/await.

Uso: python scripts/seed_survey_questions.py
"""

import sys
import os
from datetime import datetime

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.db import get_db
from app.models.preference_questions_model import PreferenceQuestion
from app.models.preference_options_model import PreferenceOption

# Las 8 preguntas de la encuesta
SURVEY_QUESTIONS = [
    {
        "question_text": "¿Cómo describirías tu estilo personal?",
        "question_type": "single",
        "order": 1,
        "options": [
            {"text": "Casual", "value": "casual"},
            {"text": "Clásico", "value": "clasico"},
            {"text": "Bohemio", "value": "bohemio"},
            {"text": "Moderno/Minimalista", "value": "moderno_minimalista"},
            {"text": "Deportivo", "value": "deportivo"},
            {"text": "Elegante", "value": "elegante"},
            {"text": "Creativo/Vanguardista", "value": "creativo_vanguardista"},
            {"text": "Otro", "value": "otro", "requires_text": True}
        ]
    },
    {
        "question_text": "¿Para qué ocasiones te vistes con más frecuencia?",
        "question_type": "multiple",
        "order": 2,
        "options": [
            {"text": "Día a día/Casual", "value": "dia_casual"},
            {"text": "Trabajo/Oficina", "value": "trabajo_oficina"},
            {"text": "Eventos especiales (bodas, fiestas)", "value": "eventos_especiales"},
            {"text": "Salidas nocturnas", "value": "salidas_nocturnas"},
            {"text": "Actividades al aire libre", "value": "aire_libre"}
        ]
    },
    {
        "question_text": "¿Qué prendas de vestir son tus favoritas o las que más usas? (Selecciona hasta 3)",
        "question_type": "multiple",
        "max_selections": 3,
        "order": 3,
        "options": [
            {"text": "Jeans", "value": "jeans"},
            {"text": "Vestidos", "value": "vestidos"},
            {"text": "Faldas", "value": "faldas"},
            {"text": "Pantalones de vestir", "value": "pantalones_vestir"},
            {"text": "Tops/Blusas", "value": "tops_blusas"},
            {"text": "Sudaderas/Hoodies", "value": "sudaderas_hoodies"},
            {"text": "Blazers/Chaquetas", "value": "blazers_chaquetas"},
            {"text": "Abrigos", "value": "abrigos"}
        ]
    },
    {
        "question_text": "¿Qué forma tiene tu cuerpo?",
        "question_type": "single",
        "order": 4,
        "has_illustrations": True,
        "options": [
            {"text": "Reloj de arena", "value": "reloj_arena"},
            {"text": "Triángulo invertido", "value": "triangulo_invertido"},
            {"text": "Triángulo/Pera", "value": "triangulo_pera"},
            {"text": "Rectángulo", "value": "rectangulo"},
            {"text": "Manzana", "value": "manzana"}
        ]
    },
    {
        "question_text": "¿Cómo describirías tu tono de piel?",
        "question_type": "single",
        "order": 5,
        "has_color_circles": True,
        "options": [
            {"text": "Muy claro/Pálido", "value": "muy_claro"},
            {"text": "Claro", "value": "claro"},
            {"text": "Medio", "value": "medio"},
            {"text": "Bronceado", "value": "bronceado"},
            {"text": "Oscuro", "value": "oscuro"}
        ]
    },
    {
        "question_text": "¿Prefieres que las prendas sean...?",
        "question_type": "single",
        "order": 6,
        "options": [
            {"text": "Holgadas", "value": "holgadas"},
            {"text": "Ajustadas", "value": "ajustadas"},
            {"text": "Depende de la prenda", "value": "depende_prenda"}
        ]
    },
    {
        "question_text": "¿Qué tipo de calzado usas más a menudo? (Selecciona las que apliquen)",
        "question_type": "multiple",
        "order": 7,
        "options": [
            {"text": "Zapatillas deportivas", "value": "zapatillas_deportivas"},
            {"text": "Botas", "value": "botas"},
            {"text": "Tacones", "value": "tacones"},
            {"text": "Sandalias", "value": "sandalias"},
            {"text": "Mocasines", "value": "mocasines"},
            {"text": "Flats", "value": "flats"},
            {"text": "Plataformas", "value": "plataformas"}
        ]
    },
    {
        "question_text": "¿Te gusta usar accesorios?",
        "question_type": "single",
        "order": 8,
        "options": [
            {"text": "Sí, siempre", "value": "siempre"},
            {"text": "A veces, para ocasiones especiales", "value": "ocasiones_especiales"},
            {"text": "Raramente o nunca", "value": "raramente_nunca"}
        ]
    }
]

def seed_questions():
    """
    Inserta las 8 preguntas de la encuesta en la base de datos.
    Modo síncrono, sin async/await.
    """
    print("=" * 60)
    print("🌱 SEED DE PREGUNTAS DE ENCUESTA")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        questions_created = 0
        options_created = 0
        
        for q_data in SURVEY_QUESTIONS:
            # Verificar si ya existe
            existing = db.query(PreferenceQuestion).filter_by(
                order=q_data["order"]
            ).first()
            
            if existing:
                print(f"⏭️  Pregunta {q_data['order']} ya existe, saltando...")
                continue
            
            # Crear pregunta
            question = PreferenceQuestion(
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                order=q_data["order"],
                max_selections=q_data.get("max_selections"),
                has_illustrations=q_data.get("has_illustrations", False),
                has_color_circles=q_data.get("has_color_circles", False)
            )
            db.add(question)
            db.flush()  # Para obtener el ID
            
            # Crear opciones
            for opt_data in q_data["options"]:
                option = PreferenceOption(
                    question_id=question.id,
                    text=opt_data["text"],
                    value=opt_data["value"],
                    requires_text=opt_data.get("requires_text", False)
                )
                db.add(option)
                options_created += 1
            
            questions_created += 1
            print(f"✅ Pregunta {q_data['order']}: '{q_data['question_text'][:50]}...' creada")
        
        db.commit()
        print("\n" + "=" * 60)
        print("🎉 SEED COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📊 Preguntas creadas: {questions_created}")
        print(f"📊 Opciones creadas: {options_created}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante seed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()
