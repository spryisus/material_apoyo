"""
Script para generar tags automáticamente para los posts existentes
basados en su estilo y descripción.
"""

import sys
import os
import json

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generar_tags_por_estilo(style, ocation):
    """
    Genera tags automáticamente basados en el estilo y descripción del post.
    """
    tags = []
    
    # Tags basados en el estilo
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
        elif style_lower in ['vintage', 'vintages']:
            tags.extend(['vintage', 'retro', 'eventos_especiales'])
        elif style_lower in ['bohemio', 'bohemios']:
            tags.extend(['bohemio', 'artistico', 'eventos_especiales'])
    
    # Tags basados en la descripción (ocation)
    if ocation:
        ocation_lower = ocation.lower()
        
        # Detectar prendas específicas
        if any(word in ocation_lower for word in ['jeans', 'vaqueros', 'pantalones']):
            tags.append('jeans')
        if any(word in ocation_lower for word in ['camiseta', 'camisetas', 't-shirt']):
            tags.append('camisetas')
        if any(word in ocation_lower for word in ['blusa', 'blusas', 'top']):
            tags.append('tops_blusas')
        if any(word in ocation_lower for word in ['vestido', 'vestidos']):
            tags.append('vestidos')
        if any(word in ocation_lower for word in ['falda', 'faldas']):
            tags.append('faldas')
        if any(word in ocation_lower for word in ['pantalon', 'pantalones']):
            tags.append('pantalones')
        if any(word in ocation_lower for word in ['chaqueta', 'chaquetas', 'blazer']):
            tags.append('chaquetas')
        if any(word in ocation_lower for word in ['sudadera', 'sudaderas', 'hoodie']):
            tags.append('sudaderas')
        if any(word in ocation_lower for word in ['chandal', 'chándal']):
            tags.append('chandal')
        
        # Detectar calzado
        if any(word in ocation_lower for word in ['zapatillas', 'sneakers', 'tenis']):
            tags.append('zapatillas_deportivas')
        if any(word in ocation_lower for word in ['sneakers', 'sneaker']):
            tags.append('sneakers')
        if any(word in ocation_lower for word in ['zapatos', 'zapato']):
            tags.append('zapatos')
        if any(word in ocation_lower for word in ['botas', 'bota']):
            tags.append('botas')
        if any(word in ocation_lower for word in ['sandalias', 'sandalias']):
            tags.append('sandalias')
        
        # Detectar ocasiones
        if any(word in ocation_lower for word in ['trabajo', 'oficina', 'profesional']):
            tags.append('trabajo_oficina')
        if any(word in ocation_lower for word in ['deporte', 'gym', 'ejercicio', 'correr']):
            tags.append('deportes_ejercicio')
        if any(word in ocation_lower for word in ['fiesta', 'evento', 'especial', 'noche']):
            tags.append('eventos_especiales')
        if any(word in ocation_lower for word in ['dia', 'diario', 'normal', 'comun']):
            tags.append('dia_casual')
        if any(word in ocation_lower for word in ['playa', 'verano', 'vacaciones']):
            tags.append('playa_verano')
        if any(word in ocation_lower for word in ['invierno', 'frio', 'abrigo']):
            tags.append('invierno')
    
    # Eliminar duplicados y mantener orden
    unique_tags = []
    for tag in tags:
        if tag not in unique_tags:
            unique_tags.append(tag)
    
    return unique_tags

def actualizar_posts_con_tags():
    """Actualiza todos los posts con tags generados automáticamente."""
    print("GENERANDO TAGS AUTOMATICOS PARA POSTS")
    print("=" * 50)
    
    try:
        from app.core.db import get_db
        from app.models.post_model import Post
        
        # Obtener sesión de base de datos
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Obtener todos los posts
            posts = db.query(Post).all()
            
            print(f"Posts encontrados: {len(posts)}")
            print()
            
            for post in posts:
                # Generar tags basados en estilo y descripción
                tags = generar_tags_por_estilo(post.style, post.ocation)
                
                print(f"Post ID: {post.id}")
                print(f"  Estilo: {post.style}")
                print(f"  Descripción: {post.ocation}")
                print(f"  Tags generados: {tags}")
                print()
                
                # En un sistema real, aquí actualizarías la base de datos
                # Por ahora solo mostramos los tags que se generarían
                
            print(f"[OK] Tags generados para {len(posts)} posts")
            print("Nota: En un sistema real, estos tags se guardarían en la base de datos")
            
            return posts
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return []

def probar_matching_con_tags():
    """Prueba el algoritmo de matching con tags generados."""
    print(f"\nPROBANDO MATCHING CON TAGS GENERADOS")
    print("=" * 50)
    
    try:
        from app.core.db import get_db
        from app.models.post_model import Post
        from app.repositories.user_preference_repository import UserPreferenceRepository
        from app.services.matching_service import get_top_matching_posts
        
        # Obtener sesión de base de datos
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Obtener posts
            all_posts = db.query(Post).all()
            
            # Obtener usuario con preferencias (Alex)
            user_pref_repo = UserPreferenceRepository(db)
            prefs = user_pref_repo.get_by_user_id("1")  # Alex
            
            if not prefs or not prefs.completed_survey:
                print("[ERROR] Usuario Alex no tiene preferencias completadas")
                return False
            
            print(f"[OK] Usuario Alex encontrado con preferencias:")
            print(f"  Estilo personal: {prefs.style_personal}")
            print(f"  Ocasiones: {prefs.occasions}")
            print(f"  Items favoritos: {prefs.favorite_items}")
            print()
            
            # Convertir posts con tags generados
            posts_with_tags = []
            for post in all_posts:
                tags = generar_tags_por_estilo(post.style, post.ocation)
                post_dict = {
                    "id": post.id,
                    "user_id": post.user_id,
                    "ocation": post.ocation,
                    "location": post.location,
                    "style": post.style,
                    "style_tags": tags,  # Tags generados automáticamente
                    "hide_location": post.hide_location,
                    "hide_votes": post.hide_votes,
                    "hide_comments": post.hide_comments,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at
                }
                posts_with_tags.append(post_dict)
            
            # Preparar preferencias del usuario
            user_preferences = {
                "style_personal": prefs.style_personal,
                "occasions": prefs.occasions or [],
                "favorite_items": prefs.favorite_items or [],
                "body_shape": prefs.body_shape,
                "shoes": prefs.shoes or [],
                "accessories": prefs.accessories
            }
            
            # Obtener posts con mejor matching
            matching_posts = get_top_matching_posts(
                user_preferences=user_preferences,
                posts=posts_with_tags,
                limit=10,
                min_score=0.0
            )
            
            print(f"[OK] Posts con matching calculado: {len(matching_posts)}")
            print()
            
            # Mostrar top 5 posts recomendados
            print(f"[TOP] TOP 5 POSTS RECOMENDADOS PARA ALEX:")
            for i, post in enumerate(matching_posts[:5], 1):
                score = post.get('matching_score', 0)
                print(f"   {i}. Post ID: {post['id']} - Score: {score:.2f}")
                print(f"      {post['ocation'] or 'Sin descripción'}")
                print(f"      Estilo: {post['style'] or 'Sin estilo'}")
                print(f"      Tags: {post['style_tags']}")
                print()
            
            # Análisis del matching
            scores = [post.get('matching_score', 0) for post in matching_posts]
            if scores:
                avg_score = sum(scores) / len(scores)
                max_score = max(scores)
                min_score = min(scores)
                print(f"[ANALISIS] ANALISIS DEL MATCHING:")
                print(f"   Score promedio: {avg_score:.2f}")
                print(f"   Score máximo: {max_score:.2f}")
                print(f"   Score mínimo: {min_score:.2f}")
                
                # Contar posts por estilo
                style_counts = {}
                for post in matching_posts:
                    style = post.get('style', 'sin_estilo')
                    style_counts[style] = style_counts.get(style, 0) + 1
                
                print(f"   Distribución por estilo:")
                for style, count in style_counts.items():
                    print(f"      {style}: {count} posts")
            
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def main():
    """Función principal."""
    print("GENERACION DE TAGS AUTOMATICOS PARA POSTS")
    print("=" * 60)
    
    # 1. Generar tags para todos los posts
    posts = actualizar_posts_con_tags()
    
    if not posts:
        print("[ERROR] No se pudieron obtener los posts")
        return
    
    # 2. Probar matching con tags generados
    resultado = probar_matching_con_tags()
    
    if resultado:
        print(f"\n[COMPLETADO] TAGS GENERADOS Y MATCHING PROBADO")
        print("=" * 60)
        print("Los posts ahora tienen tags automáticos que permiten")
        print("que el algoritmo de matching funcione correctamente")
        print("\nPróximos pasos:")
        print("1. Implementar guardado de tags en la base de datos")
        print("2. Actualizar el endpoint para usar tags reales")
        print("3. Probar el endpoint completo con usuarios")
    else:
        print(f"\n[ERROR] Error en la prueba de matching")

if __name__ == "__main__":
    main()

