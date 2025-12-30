from fastapi import (
    APIRouter, Depends, HTTPException, status, UploadFile, File, Form
)
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import uuid
from app.models.post_model import Post
from app.models.photo_model import Photo
from app.security.dependencies import get_current_user
from app.core.db import get_db
from app.cloud.s3 import S3Service, delete_file_from_s3
from app.dto.posts_dto import PostOut
from app.dto.user_dto import UserInPost
from app.dto.photo_dto import PhotoOut
from app.services.matching_service import get_top_matching_posts
from app.repositories.user_preference_repository import UserPreferenceRepository

router = APIRouter(prefix="/posts", tags=["Posts"])

def str_to_bool(value: Optional[str]) -> bool:
    if value is None:
        return False
    return str(value).lower() in ("true", "1", "t", "yes")

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    ocation: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    style: Optional[str] = Form(None),
    hide_location: Optional[str] = Form("false"),  
    hide_votes: Optional[str] = Form("false"),     
    hide_comments: Optional[str] = Form("false"),  
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        hide_location_bool = str_to_bool(hide_location)
        hide_votes_bool = str_to_bool(hide_votes)
        hide_comments_bool = str_to_bool(hide_comments)

        post = Post(
            ocation=ocation,
            location=location,
            style=style,
            hide_location=hide_location_bool,
            hide_votes=hide_votes_bool,
            hide_comments=hide_comments_bool,
            user_id=current_user.user_id,
            created_by=current_user.user_id,
            updated_by=current_user.user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(post)
        db.flush()

        saved_photos = []
        for index, file in enumerate(files):
            file_key = f"users/{current_user.user_id}/posts/{post.id}/{uuid.uuid4()}_{file.filename}"
            photo_url = S3Service().upload_photo(file, file_key)

            photo = Photo(
                post_id=post.id,
                url=photo_url,
                order_index=index,
                reactions_count=0,
                comments_count=0,
                views_count=0,
                created_by=current_user.user_id,
                updated_by=current_user.user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(photo)
            saved_photos.append(photo)

        db.commit()

        db.refresh(post)
        for photo in saved_photos:
            db.refresh(photo)

        post_dict = post.__dict__.copy()
        post_dict.update({
            "user_id": post.created_by,
            "user": UserInPost(
                user_id=current_user.user_id,
                username=current_user.username,
                profile_picture_url=current_user.profile_picture_url
            ),
            "images": [PhotoOut.from_orm(photo) for photo in saved_photos]
        })

        return PostOut(**post_dict)

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error creando el post: {str(e)}")

# ---

@router.get("/{post_id}")
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = db.query(Post).filter(
        Post.id == post_id, Post.created_by == current_user.user_id
    ).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado o no tienes permiso para verlo.")

    photos = db.query(Photo).filter(Photo.post_id == post.id).all()
    
    return {
        "id": post.id,
        "ocation": post.ocation,
        "location": post.location,
        "style": post.style,
        "hide_location": post.hide_location,
        "hide_votes": post.hide_votes,
        "hide_comments": post.hide_comments,
        "photos": [{"id": p.id, "url": p.url} for p in photos],
    }

# ---

@router.put("/{post_id}")
def update_post(
    post_id: int,
    ocation: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    style: Optional[str] = Form(None),
    hide_location: Optional[bool] = Form(None),
    hide_votes: Optional[bool] = Form(None),
    hide_comments: Optional[bool] = Form(None),
    files: Optional[List[UploadFile]] = File(None), 
    delete_photo_ids: Optional[List[int]] = Form(None), 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = db.query(Post).filter(
        Post.id == post_id, Post.created_by == current_user.user_id
    ).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado o no tienes permiso para editarlo.")

    if ocation is not None:
        post.caption = ocation
    if location is not None:
        post.location = location
    
    # Actualización de campos nuevos
    if style is not None:
        post.style = style
    if hide_location is not None:
        post.hide_location = hide_location
    if hide_votes is not None:
        post.hide_votes = hide_votes
    if hide_comments is not None:
        post.hide_comments = hide_comments

    if delete_photo_ids:
        photos_to_delete = db.query(Photo).filter(
            Photo.id.in_(delete_photo_ids), Photo.post_id == post.id
        ).all()
        for photo in photos_to_delete:
            try:
                s3_key = photo.url.split(".amazonaws.com/")[1]
                delete_file_from_s3(s3_key)
            except Exception:
                pass
            db.delete(photo)

    if files:
        last_index = (
            db.query(Photo.order_index).filter(Photo.post_id == post.id).order_by(Photo.order_index.desc()).first()
        )
        start_index = last_index[0] + 1 if last_index else 0
        for i, file in enumerate(files, start=start_index):
            file_key = f"users/{current_user.user_id}/posts/{post.id}/{uuid.uuid4()}_{file.filename}"
            photo_url = S3Service().upload_photo(file, file_key)

            new_photo = Photo(
                post_id=post.id,
                url=photo_url,
                order_index=i,
                reactions_count=0,
                comments_count=0,
                views_count=0,
                created_by=current_user.user_id,
                updated_by=current_user.user_id
            )
            db.add(new_photo)

    post.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Post actualizado correctamente"}

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = db.query(Post).filter(
        Post.id == post_id, Post.created_by == current_user.user_id
    ).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado o no tienes permiso para borrarlo.")

    photos = db.query(Photo).filter(Photo.post_id == post.id).all()
    for photo in photos:
        try:
            s3_key = photo.url.split(".amazonaws.com/")[1]
            delete_file_from_s3(s3_key)
        except Exception:
            pass
        db.delete(photo)

    db.delete(post)
    db.commit()
    return {"message": "Post eliminado correctamente"}

@router.get("/test-schema")
def get_test_schema_posts(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Endpoint para obtener todos los posts del esquema test.
    Utiliza la funcionalidad completa del sistema de matching y recomendaciones.
    """
    try:
        # 1. Obtener todos los posts del esquema test
        all_posts = db.query(Post).order_by(Post.created_at.desc()).all()
        
        if not all_posts:
            return {
                "success": True,
                "message": "No hay posts en el esquema test",
                "posts": [],
                "total_count": 0,
                "has_more": False,
                "schema": "test"
            }
        
        # 2. Verificar si el usuario tiene preferencias para personalización
        user_pref_repo = UserPreferenceRepository(db)
        prefs = user_pref_repo.get_by_user_id(str(current_user.user_id))
        
        posts_response = []
        
        if prefs and prefs.completed_survey:
            # Usuario tiene preferencias - aplicar matching personalizado
            print(f" Usuario {current_user.user_id} tiene preferencias - aplicando matching personalizado")
            
            # Convertir posts a formato para matching
            posts_for_matching = []
            for post in all_posts:
                post_dict = {
                    "id": post.id,
                    "user_id": post.user_id,
                    "ocation": post.ocation,
                    "location": post.location,
                    "style": post.style,
                    "style_tags": [],  # No existe en la DB real, usar array vacío
                    "hide_location": post.hide_location,
                    "hide_votes": post.hide_votes,
                    "hide_comments": post.hide_comments,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at
                }
                posts_for_matching.append(post_dict)
            
            # Calcular matching scores
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
                posts=posts_for_matching,
                limit=limit + offset,
                min_score=0.0
            )
            
            # Aplicar paginación
            paginated_posts = matching_posts[offset:offset + limit]
            
            posts_response = paginated_posts
            
            response_message = f"Posts personalizados basados en tus preferencias (estilo: {prefs.style_personal})"
            
        else:
            # Usuario sin preferencias - mostrar todos los posts ordenados por fecha
            print(f"📋 Usuario {current_user.user_id} sin preferencias - mostrando feed genérico")
            
            paginated_posts = all_posts[offset:offset + limit]
            
            for post in paginated_posts:
                post_dict = {
                    "id": post.id,
                    "user_id": post.user_id,
                    "ocation": post.ocation,
                    "location": post.location,
                    "style": post.style,
                    "style_tags": [],  # No existe en la DB real, usar array vacío
                    "hide_location": post.hide_location,
                    "hide_votes": post.hide_votes,
                    "hide_comments": post.hide_comments,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at,
                    "matching_score": 0,  # Sin personalización
                    "matching_explanation": "Sin personalización - completa tu encuesta para recomendaciones personalizadas"
                }
                posts_response.append(post_dict)
            
            response_message = "Feed genérico - completa tu encuesta para obtener recomendaciones personalizadas"
        
        return {
            "success": True,
            "message": response_message,
            "posts": posts_response,
            "total_count": len(all_posts),
            "has_more": (offset + limit) < len(all_posts),
            "schema": "test",
            "user_preferences_applied": bool(prefs and prefs.completed_survey),
            "pagination": {
                "limit": limit,
                "offset": offset,
                "returned": len(posts_response)
            }
        }
        
    except Exception as e:
        print(f"Error en endpoint test-schema: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener posts del esquema test: {str(e)}")

@router.get("/feed/for-you")
def get_personalized_feed(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Feed personalizado basado en preferencias del usuario.
    """
    try:
        # 1. Verificar si usuario tiene preferencias
        user_pref_repo = UserPreferenceRepository(db)
        prefs = user_pref_repo.get_by_user_id(str(current_user.user_id))
        
        if not prefs or not prefs.completed_survey:
            # Si no tiene preferencias, devolver feed genérico
            posts = db.query(Post).order_by(Post.created_at.desc()).offset(offset).limit(limit).all()
            
            return {
                "success": True,
                "requires_survey": True,
                "message": "Completa tu encuesta para personalizar el feed",
                "posts": [post.__dict__ for post in posts],
                "total_count": len(posts),
                "has_more": len(posts) == limit
            }
        
        # 2. Obtener todos los posts disponibles
        all_posts = db.query(Post).order_by(Post.created_at.desc()).all()
        
        # 3. Convertir posts a formato para matching
        posts_for_matching = []
        for post in all_posts:
            post_dict = {
                "id": post.id,
                "user_id": post.user_id,
                "ocation": post.ocation,
                "location": post.location,
                "style": post.style,
                "style_tags": [],  # No existe en la DB real, usar array vacío
                "hide_location": post.hide_location,
                "hide_votes": post.hide_votes,
                "hide_comments": post.hide_comments,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }
            posts_for_matching.append(post_dict)
        
        # 4. Calcular matching scores
        user_preferences = {
            "style_personal": prefs.style_personal,
            "occasions": prefs.occasions or [],
            "favorite_items": prefs.favorite_items or [],
            "body_shape": prefs.body_shape,
            "shoes": prefs.shoes or [],
            "accessories": prefs.accessories
        }
        
        # 5. Obtener posts con mejor matching
        matching_posts = get_top_matching_posts(
            user_preferences=user_preferences,
            posts=posts_for_matching,
            limit=limit + offset,  # Obtener más para paginación
            min_score=0.0
        )
        
        # 6. Aplicar paginación
        paginated_posts = matching_posts[offset:offset + limit]
        
        return {
            "success": True,
            "requires_survey": False,
            "posts": paginated_posts,
            "total_count": len(matching_posts),
            "has_more": (offset + limit) < len(matching_posts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener feed personalizado: {str(e)}")