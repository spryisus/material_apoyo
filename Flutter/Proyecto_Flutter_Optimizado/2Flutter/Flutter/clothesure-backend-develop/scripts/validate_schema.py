"""
Script de validación de schema antes de implementar sistema de encuestas.
Verifica tablas existentes y documenta cambios necesarios.

Uso: python scripts/validate_schema.py
"""

from sqlalchemy import inspect, text
from app.core.db import engine, get_db
from datetime import datetime
import json
import sys
import os

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def validate_schema():
    """
    Valida el schema actual y documenta cambios necesarios.
    NO MODIFICA NADA, solo reporta.
    """
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": "OK",
        "existing_tables": existing_tables,
        "required_tables": [],
        "missing_tables": [],
        "existing_columns": {},
        "missing_columns": {},
        "recommendations": []
    }
    
    print("=" * 60)
    print("🔍 VALIDACIÓN DE SCHEMA PARA SISTEMA DE ENCUESTAS")
    print("=" * 60)
    
    # Tabla 1: preference_questions
    print("\n📋 Verificando tabla: preference_questions")
    if "preference_questions" in existing_tables:
        print("   ✅ Tabla existe")
        columns = [col['name'] for col in inspector.get_columns('preference_questions')]
        report["existing_columns"]["preference_questions"] = columns
        
        required_cols = [
            "id", "question_text", "question_type", "order",
            "max_selections", "has_illustrations", "has_color_circles",
            "created_at", "updated_at"
        ]
        missing = [col for col in required_cols if col not in columns]
        
        if missing:
            print(f"   ⚠️  Columnas faltantes: {missing}")
            report["missing_columns"]["preference_questions"] = missing
            report["recommendations"].append({
                "table": "preference_questions",
                "action": "ALTER_TABLE",
                "columns": missing
            })
        else:
            print("   ✅ Todas las columnas necesarias existen")
    else:
        print("   ❌ Tabla NO existe - Necesita crearse")
        report["missing_tables"].append("preference_questions")
        report["recommendations"].append({
            "table": "preference_questions",
            "action": "CREATE_TABLE",
            "priority": "HIGH"
        })
    
    # Tabla 2: preference_options
    print("\n📋 Verificando tabla: preference_options")
    if "preference_options" in existing_tables:
        print("   ✅ Tabla existe")
        columns = [col['name'] for col in inspector.get_columns('preference_options')]
        report["existing_columns"]["preference_options"] = columns
        
        required_cols = [
            "id", "question_id", "text", "value", "requires_text",
            "created_at", "updated_at"
        ]
        missing = [col for col in required_cols if col not in columns]
        
        if missing:
            print(f"   ⚠️  Columnas faltantes: {missing}")
            report["missing_columns"]["preference_options"] = missing
            report["recommendations"].append({
                "table": "preference_options",
                "action": "ALTER_TABLE",
                "columns": missing
            })
        else:
            print("   ✅ Todas las columnas necesarias existen")
    else:
        print("   ❌ Tabla NO existe - Necesita crearse")
        report["missing_tables"].append("preference_options")
        report["recommendations"].append({
            "table": "preference_options",
            "action": "CREATE_TABLE",
            "priority": "HIGH"
        })
    
    # Tabla 3: user_preferences
    print("\n📋 Verificando tabla: user_preferences")
    if "user_preferences" in existing_tables:
        print("   ✅ Tabla existe")
        columns = [col['name'] for col in inspector.get_columns('user_preferences')]
        report["existing_columns"]["user_preferences"] = columns
        
        required_cols = [
            "id", "user_id", "style_personal", "style_personal_custom",
            "occasions", "favorite_items", "body_shape", "skin_tone",
            "fit_preference", "shoes", "accessories", "completed_survey",
            "created_at", "updated_at"
        ]
        missing = [col for col in required_cols if col not in columns]
        
        if missing:
            print(f"   ⚠️  Columnas faltantes: {missing}")
            report["missing_columns"]["user_preferences"] = missing
            report["recommendations"].append({
                "table": "user_preferences",
                "action": "ALTER_TABLE",
                "columns": missing
            })
        else:
            print("   ✅ Todas las columnas necesarias existen")
            
        # Verificar índices críticos
        indexes = inspector.get_indexes('user_preferences')
        has_user_id_index = any(
            'user_id' in idx.get('column_names', []) 
            for idx in indexes
        )
        if not has_user_id_index:
            print("   ⚠️  Falta índice en user_id (crítico para performance)")
            report["recommendations"].append({
                "table": "user_preferences",
                "action": "CREATE_INDEX",
                "column": "user_id",
                "priority": "MEDIUM"
            })
    else:
        print("   ❌ Tabla NO existe - Necesita crearse")
        report["missing_tables"].append("user_preferences")
        report["recommendations"].append({
            "table": "user_preferences",
            "action": "CREATE_TABLE",
            "priority": "HIGH"
        })
    
    # Verificar foreign keys
    print("\n🔗 Verificando relaciones (Foreign Keys)")
    if "preference_options" in existing_tables:
        fks = inspector.get_foreign_keys('preference_options')
        has_question_fk = any(
            fk.get('referred_table') == 'preference_questions' 
            for fk in fks
        )
        if not has_question_fk:
            print("   ⚠️  Falta FK: preference_options -> preference_questions")
            report["recommendations"].append({
                "table": "preference_options",
                "action": "ADD_FOREIGN_KEY",
                "column": "question_id",
                "references": "preference_questions(id)"
            })
        else:
            print("   ✅ FK preference_options -> preference_questions existe")
    
    if "user_preferences" in existing_tables:
        fks = inspector.get_foreign_keys('user_preferences')
        has_user_fk = any(
            fk.get('referred_table') == 'users' 
            for fk in fks
        )
        if not has_user_fk:
            print("   ⚠️  Falta FK: user_preferences -> users")
            report["recommendations"].append({
                "table": "user_preferences",
                "action": "ADD_FOREIGN_KEY",
                "column": "user_id",
                "references": "users(id)"
            })
        else:
            print("   ✅ FK user_preferences -> users existe")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    if report["missing_tables"]:
        print(f"❌ Tablas faltantes: {len(report['missing_tables'])}")
        for table in report["missing_tables"]:
            print(f"   - {table}")
        report["status"] = "NEEDS_MIGRATION"
    
    if report["missing_columns"]:
        print(f"⚠️  Columnas faltantes en {len(report['missing_columns'])} tabla(s)")
        for table, cols in report["missing_columns"].items():
            print(f"   - {table}: {cols}")
        report["status"] = "NEEDS_MIGRATION"
    
    if report["recommendations"]:
        print(f"\n💡 Recomendaciones: {len(report['recommendations'])}")
        for rec in report["recommendations"]:
            priority = rec.get('priority', 'MEDIUM')
            action = rec['action']
            table = rec['table']
            print(f"   [{priority}] {action} en {table}")
    
    if report["status"] == "OK":
        print("\n✅ Schema correcto - Puedes proceder con Fase 1 (Seed)")
    else:
        print("\n⚠️  Se necesita migración - Ejecuta scripts/migrate_schema.py")
    
    # Guardar reporte
    with open("schema_validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n📄 Reporte guardado en: schema_validation_report.json")
    
    return report

if __name__ == "__main__":
    validate_schema()
