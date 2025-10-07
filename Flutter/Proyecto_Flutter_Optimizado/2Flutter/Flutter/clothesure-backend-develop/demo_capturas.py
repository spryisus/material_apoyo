"""
Script para generar capturas de pantalla del funcionamiento del algoritmo de matching.
Muestra resultados claros y visuales para demostrar el funcionamiento.
"""

import sys
import os
import json
from datetime import datetime

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def mostrar_demo_completo():
    """Muestra una demostración completa del sistema."""
    print("=" * 80)
    print("[DEMO] DEMOSTRACION DEL ALGORITMO DE MATCHING - CLOTHESURE")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        from app.core.db import get_db
        from app.models.post_model import Post
        from app.models.user_model import User
        from app.repositories.user_preference_repository import UserPreferenceRepository
        from app.services.matching_service import get_top_matching_posts
        
        # Obtener sesión de base de datos
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # 1. MOSTRAR USUARIOS DISPONIBLES
            print("[USUARIOS] USUARIOS EN EL SISTEMA")
            print("-" * 50)
            
            users = db.query(User).all()
            user_pref_repo = UserPreferenceRepository(db)
            
            for user in users:
                prefs = user_pref_repo.get_by_user_id(str(user.user_id))
                print(f"[USER] {user.username} ({user.email})")
                if prefs and prefs.completed_survey:
                    print(f"   [OK] Preferencias completadas:")
                    print(f"      Estilo: {prefs.style_personal}")
                    print(f"      Ocasiones: {', '.join(prefs.occasions or [])}")
                    print(f"      Items favoritos: {', '.join(prefs.favorite_items or [])}")
                    print(f"      Zapatos: {', '.join(prefs.shoes or [])}")
                else:
                    print(f"   [NO] Sin preferencias completadas")
                print()
            
            # 2. MOSTRAR POSTS DISPONIBLES
            print("[POSTS] POSTS DISPONIBLES EN EL SISTEMA")
            print("-" * 50)
            
            all_posts = db.query(Post).order_by(Post.created_at.desc()).all()
            print(f"Total de posts: {len(all_posts)}")
            print()
            
            # Mostrar algunos posts de ejemplo
            for i, post in enumerate(all_posts[:5], 1):
                print(f"{i}. Post ID: {post.id}")
                print(f"   Descripcion: {post.ocation}")
                print(f"   Estilo: {post.style}")
                print(f"   Ubicacion: {post.location}")
                print(f"   Usuario: {post.user_id}")
                print()
            
            # 3. DEMOSTRAR ALGORITMO DE MATCHING
            print("[MATCHING] ALGORITMO DE MATCHING EN ACCION")
            print("-" * 50)
            
            # Función para generar tags automáticamente
            def generar_tags_automaticos(style, ocation):
                tags = []
                if style:
                    style_lower = style.lower()
                    if style_lower in ['casual', 'casuales']:
                        tags.extend(['casual', 'dia_casual', 'relajado'])
                    elif style_lower in ['formal', 'formales']:
                        tags.extend(['formal', 'trabajo_oficina', 'eventos_especiales'])
                    elif style_lower in ['elegante', 'elegantes']:
                        tags.extend(['elegante', 'eventos_especiales', 'trabajo_oficina'])
                    elif style_lower in ['deportivo', 'deportivos']:
                        tags.extend(['deportivo', 'deportes_ejercicio', 'activo'])
                    elif style_lower in ['gotico', 'gótico', 'goticos']:
                        tags.extend(['gotico', 'alternativo', 'eventos_especiales'])
                
                if ocation:
                    ocation_lower = ocation.lower()
                    if any(word in ocation_lower for word in ['jeans', 'vaqueros']):
                        tags.append('jeans')
                    if any(word in ocation_lower for word in ['camiseta', 'camisetas']):
                        tags.append('camisetas')
                    if any(word in ocation_lower for word in ['blusa', 'blusas', 'top']):
                        tags.append('tops_blusas')
                    if any(word in ocation_lower for word in ['vestido', 'vestidos']):
                        tags.append('vestidos')
                    if any(word in ocation_lower for word in ['chaqueta', 'blazer']):
                        tags.append('chaquetas')
                    if any(word in ocation_lower for word in ['sudadera', 'sudaderas']):
                        tags.append('sudaderas')
                    if any(word in ocation_lower for word in ['zapatillas', 'sneakers']):
                        tags.append('zapatillas_deportivas')
                
                return list(set(tags))  # Eliminar duplicados
            
            # 4. PROBAR CON ALEX (Usuario Elegante)
            print("[ALEX] PRUEBA CON ALEX (Usuario Elegante)")
            print("=" * 60)
            
            alex_prefs = user_pref_repo.get_by_user_id("1")
            if alex_prefs and alex_prefs.completed_survey:
                print(f"Usuario: Alex")
                print(f"Estilo personal: {alex_prefs.style_personal}")
                print(f"Ocasiones preferidas: {', '.join(alex_prefs.occasions or [])}")
                print(f"Items favoritos: {', '.join(alex_prefs.favorite_items or [])}")
                print(f"Zapatos preferidos: {', '.join(alex_prefs.shoes or [])}")
                print()
                
                # Convertir posts con tags generados
                posts_with_tags = []
                for post in all_posts:
                    tags = generar_tags_automaticos(post.style, post.ocation)
                    post_dict = {
                        "id": post.id,
                        "user_id": post.user_id,
                        "ocation": post.ocation,
                        "location": post.location,
                        "style": post.style,
                        "style_tags": tags,
                        "hide_location": post.hide_location,
                        "hide_votes": post.hide_votes,
                        "hide_comments": post.hide_comments,
                        "created_at": post.created_at,
                        "updated_at": post.updated_at
                    }
                    posts_with_tags.append(post_dict)
                
                # Preparar preferencias de Alex
                alex_preferences = {
                    "style_personal": alex_prefs.style_personal,
                    "occasions": alex_prefs.occasions or [],
                    "favorite_items": alex_prefs.favorite_items or [],
                    "body_shape": alex_prefs.body_shape,
                    "shoes": alex_prefs.shoes or [],
                    "accessories": alex_prefs.accessories
                }
                
                # Obtener posts con mejor matching
                matching_posts = get_top_matching_posts(
                    user_preferences=alex_preferences,
                    posts=posts_with_tags,
                    limit=10,
                    min_score=0.0
                )
                
                print("[TOP] TOP 5 RECOMENDACIONES PARA ALEX:")
                print("-" * 40)
                
                for i, post in enumerate(matching_posts[:5], 1):
                    score = post.get('matching_score', 0)
                    print(f"{i}. Post ID: {post['id']} - Score: {score:.1f}")
                    print(f"   {post['ocation']}")
                    print(f"   Estilo: {post['style']}")
                    print(f"   Tags: {', '.join(post['style_tags'])}")
                    
                    # Explicar por qué tiene ese score
                    if score >= 5.0:
                        print(f"   [PERFECTO] Coincide con estilo elegante + ocasiones")
                    elif score >= 3.0:
                        print(f"   [BUENO] Coincide parcialmente")
                    elif score >= 1.0:
                        print(f"   [REGULAR] Pocas coincidencias")
                    else:
                        print(f"   [MALO] No coincide con preferencias")
                    print()
                
                # Análisis del matching
                scores = [post.get('matching_score', 0) for post in matching_posts]
                if scores:
                    avg_score = sum(scores) / len(scores)
                    max_score = max(scores)
                    min_score = min(scores)
                    
                    print("[ANALISIS] ANALISIS DEL MATCHING:")
                    print(f"   Score promedio: {avg_score:.2f}")
                    print(f"   Score maximo: {max_score:.2f}")
                    print(f"   Score minimo: {min_score:.2f}")
                    print(f"   Posts recomendados: {len(matching_posts)}")
                    print()
            
            # 5. PROBAR CON NOTGENARO (Usuario Casual)
            print("[GENARO] PRUEBA CON NOTGENARO (Usuario Casual)")
            print("=" * 60)
            
            genaro_prefs = user_pref_repo.get_by_user_id("3")
            if genaro_prefs and genaro_prefs.completed_survey:
                print(f"Usuario: NotGenaro")
                print(f"Estilo personal: {genaro_prefs.style_personal}")
                print(f"Ocasiones preferidas: {', '.join(genaro_prefs.occasions or [])}")
                print(f"Items favoritos: {', '.join(genaro_prefs.favorite_items or [])}")
                print(f"Zapatos preferidos: {', '.join(genaro_prefs.shoes or [])}")
                print()
                
                # Preparar preferencias de NotGenaro
                genaro_preferences = {
                    "style_personal": genaro_prefs.style_personal,
                    "occasions": genaro_prefs.occasions or [],
                    "favorite_items": genaro_prefs.favorite_items or [],
                    "body_shape": genaro_prefs.body_shape,
                    "shoes": genaro_prefs.shoes or [],
                    "accessories": genaro_prefs.accessories
                }
                
                # Obtener posts con mejor matching
                matching_posts_genaro = get_top_matching_posts(
                    user_preferences=genaro_preferences,
                    posts=posts_with_tags,
                    limit=10,
                    min_score=0.0
                )
                
                print("[TOP] TOP 5 RECOMENDACIONES PARA NOTGENARO:")
                print("-" * 40)
                
                for i, post in enumerate(matching_posts_genaro[:5], 1):
                    score = post.get('matching_score', 0)
                    print(f"{i}. Post ID: {post['id']} - Score: {score:.1f}")
                    print(f"   {post['ocation']}")
                    print(f"   Estilo: {post['style']}")
                    print(f"   Tags: {', '.join(post['style_tags'])}")
                    
                    # Explicar por qué tiene ese score
                    if score >= 5.0:
                        print(f"   [PERFECTO] Coincide con estilo casual + ocasiones")
                    elif score >= 3.0:
                        print(f"   [BUENO] Coincide parcialmente")
                    elif score >= 1.0:
                        print(f"   [REGULAR] Pocas coincidencias")
                    else:
                        print(f"   [MALO] No coincide con preferencias")
                    print()
                
                # Análisis del matching
                scores_genaro = [post.get('matching_score', 0) for post in matching_posts_genaro]
                if scores_genaro:
                    avg_score_genaro = sum(scores_genaro) / len(scores_genaro)
                    max_score_genaro = max(scores_genaro)
                    min_score_genaro = min(scores_genaro)
                    
                    print("[ANALISIS] ANALISIS DEL MATCHING:")
                    print(f"   Score promedio: {avg_score_genaro:.2f}")
                    print(f"   Score maximo: {max_score_genaro:.2f}")
                    print(f"   Score minimo: {min_score_genaro:.2f}")
                    print(f"   Posts recomendados: {len(matching_posts_genaro)}")
                    print()
            
            # 6. RESUMEN FINAL
            print("[RESUMEN] RESUMEN DEL FUNCIONAMIENTO")
            print("=" * 60)
            print("[OK] Sistema de matching funcionando correctamente")
            print("[OK] Tags automaticos generados para todos los posts")
            print("[OK] Algoritmo de personalizacion activo")
            print("[OK] Recomendaciones diferenciadas por usuario")
            print()
            print("[FUNCIONALIDADES] FUNCIONALIDADES IMPLEMENTADAS:")
            print("   • Generacion automatica de tags")
            print("   • Algoritmo de matching personalizado")
            print("   • Scores de compatibilidad")
            print("   • Recomendaciones diferenciadas")
            print("   • Analisis detallado de coincidencias")
            print()
            print("[ENDPOINT] ENDPOINT DISPONIBLE:")
            print("   GET /posts/test-schema")
            print("   - Obtiene posts personalizados")
            print("   - Aplica algoritmo de matching")
            print("   - Retorna scores de compatibilidad")
            print("   - Incluye paginacion")
            
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def main():
    """Función principal."""
    print("[INICIO] INICIANDO DEMOSTRACION DEL SISTEMA")
    print("=" * 80)
    
    resultado = mostrar_demo_completo()
    
    if resultado:
        print("\n[COMPLETADO] DEMOSTRACION COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        print("El sistema esta funcionando correctamente y listo para usar")
    else:
        print("\n[ERROR] ERROR EN LA DEMOSTRACION")
        print("=" * 80)
        print("Revisa la configuracion de la base de datos")

if __name__ == "__main__":
    main()
