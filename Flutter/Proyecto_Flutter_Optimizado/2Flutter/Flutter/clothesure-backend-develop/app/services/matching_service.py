"""
Servicio de matching para calcular compatibilidad entre preferencias de usuario y posts.
"""

from typing import Dict, List, Optional
from app.core.config import MATCHING_WEIGHTS

def calculate_matching_score(
    user_preferences: Dict,
    post_tags: List[str],
    weights: Dict = None
) -> float:
    """
    Calcula score de compatibilidad entre preferencias y post.
    
    Args:
        user_preferences: Dict con preferencias del usuario
        post_tags: Lista de tags del post ["casual", "jeans", "dia_casual"]
        weights: Dict opcional con pesos personalizados
    
    Returns:
        float: Score de compatibilidad (0-10+)
    
    Ejemplo:
        user_prefs = {
            "style_personal": "casual",
            "occasions": ["dia_casual", "trabajo_oficina"],
            "favorite_items": ["jeans", "tops_blusas"]
        }
        post_tags = ["casual", "jeans", "dia_casual"]
        score = calculate_matching_score(user_prefs, post_tags)
        # Returns: 7.0 (3 + 2 + 2)
    """
    if weights is None:
        weights = MATCHING_WEIGHTS
    
    score = 0.0
    
    # Coincidencia en estilo personal
    if user_preferences.get("style_personal") in post_tags:
        score += weights["style_personal"]
    
    # Coincidencias en ocasiones
    occasions = user_preferences.get("occasions", [])
    for occasion in occasions:
        if occasion in post_tags:
            score += weights["occasions"]
            break  # Solo sumar una vez
    
    # Coincidencias en prendas favoritas
    favorite_items = user_preferences.get("favorite_items", [])
    for item in favorite_items:
        if item in post_tags:
            score += weights["favorite_items"]
    
    # Coincidencias en calzado
    shoes = user_preferences.get("shoes", [])
    for shoe in shoes:
        if shoe in post_tags:
            score += weights["shoes"]
            break
    
    # Coincidencia en body_shape (si el post lo especifica)
    if user_preferences.get("body_shape") in post_tags:
        score += weights["body_shape"]
    
    return score

def calculate_matching_scores_for_posts(
    user_preferences: Dict,
    posts: List[Dict],
    weights: Dict = None
) -> List[Dict]:
    """
    Calcula scores de matching para una lista de posts.
    
    Args:
        user_preferences: Dict con preferencias del usuario
        posts: Lista de posts con campo 'style_tags'
        weights: Dict opcional con pesos personalizados
    
    Returns:
        List[Dict]: Lista de posts con score de matching agregado
    """
    if weights is None:
        weights = MATCHING_WEIGHTS
    
    scored_posts = []
    
    for post in posts:
        post_tags = post.get('style_tags', [])
        if not post_tags:
            # Si no tiene tags, score 0
            post['matching_score'] = 0.0
        else:
            score = calculate_matching_score(user_preferences, post_tags, weights)
            post['matching_score'] = score
        
        scored_posts.append(post)
    
    return scored_posts

def get_matching_explanation(
    user_preferences: Dict,
    post_tags: List[str],
    weights: Dict = None
) -> Dict[str, any]:
    """
    Genera explicación detallada del matching score.
    
    Args:
        user_preferences: Dict con preferencias del usuario
        post_tags: Lista de tags del post
        weights: Dict opcional con pesos personalizados
    
    Returns:
        Dict con explicación detallada del matching
    """
    if weights is None:
        weights = MATCHING_WEIGHTS
    
    explanation = {
        "total_score": 0.0,
        "matches": [],
        "max_possible_score": sum(weights.values()),
        "match_percentage": 0.0
    }
    
    # Verificar cada tipo de coincidencia
    matches = []
    
    # Estilo personal
    if user_preferences.get("style_personal") in post_tags:
        matches.append({
            "type": "style_personal",
            "weight": weights["style_personal"],
            "matched": True,
            "user_value": user_preferences.get("style_personal"),
            "description": "Coincidencia en estilo personal"
        })
    else:
        matches.append({
            "type": "style_personal",
            "weight": weights["style_personal"],
            "matched": False,
            "user_value": user_preferences.get("style_personal"),
            "description": "Sin coincidencia en estilo personal"
        })
    
    # Ocasiones
    occasions = user_preferences.get("occasions", [])
    occasion_match = any(occasion in post_tags for occasion in occasions)
    matches.append({
        "type": "occasions",
        "weight": weights["occasions"],
        "matched": occasion_match,
        "user_value": occasions,
        "description": "Coincidencia en ocasiones" if occasion_match else "Sin coincidencia en ocasiones"
    })
    
    # Prendas favoritas
    favorite_items = user_preferences.get("favorite_items", [])
    item_matches = [item for item in favorite_items if item in post_tags]
    matches.append({
        "type": "favorite_items",
        "weight": weights["favorite_items"],
        "matched": len(item_matches) > 0,
        "user_value": favorite_items,
        "matched_items": item_matches,
        "description": f"Coincidencia en {len(item_matches)} prendas favoritas" if item_matches else "Sin coincidencia en prendas favoritas"
    })
    
    # Calzado
    shoes = user_preferences.get("shoes", [])
    shoe_matches = [shoe for shoe in shoes if shoe in post_tags]
    matches.append({
        "type": "shoes",
        "weight": weights["shoes"],
        "matched": len(shoe_matches) > 0,
        "user_value": shoes,
        "matched_shoes": shoe_matches,
        "description": f"Coincidencia en {len(shoe_matches)} tipos de calzado" if shoe_matches else "Sin coincidencia en calzado"
    })
    
    # Body shape
    body_shape_match = user_preferences.get("body_shape") in post_tags
    matches.append({
        "type": "body_shape",
        "weight": weights["body_shape"],
        "matched": body_shape_match,
        "user_value": user_preferences.get("body_shape"),
        "description": "Coincidencia en forma del cuerpo" if body_shape_match else "Sin coincidencia en forma del cuerpo"
    })
    
    # Calcular score total
    total_score = sum(match["weight"] for match in matches if match["matched"])
    explanation["total_score"] = total_score
    explanation["matches"] = matches
    explanation["match_percentage"] = (total_score / explanation["max_possible_score"]) * 100
    
    return explanation

def get_top_matching_posts(
    user_preferences: Dict,
    posts: List[Dict],
    limit: int = 10,
    min_score: float = 0.0,
    weights: Dict = None
) -> List[Dict]:
    """
    Obtiene los posts con mejor matching score.
    
    Args:
        user_preferences: Dict con preferencias del usuario
        posts: Lista de posts con campo 'style_tags'
        limit: Número máximo de posts a retornar
        min_score: Score mínimo para incluir post
        weights: Dict opcional con pesos personalizados
    
    Returns:
        List[Dict]: Lista de posts ordenados por score descendente
    """
    # Calcular scores
    scored_posts = calculate_matching_scores_for_posts(user_preferences, posts, weights)
    
    # Filtrar por score mínimo
    filtered_posts = [post for post in scored_posts if post['matching_score'] >= min_score]
    
    # Ordenar por score descendente
    sorted_posts = sorted(filtered_posts, key=lambda x: x['matching_score'], reverse=True)
    
    # Limitar resultados
    return sorted_posts[:limit]
