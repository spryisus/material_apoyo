from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.models.photo_model import Photo
from app.dto.photo_dto import PhotoOut
from app.factories.repository_factory import get_photo_service
from app.cloud.s3 import S3Service, delete_file_from_s3
from app.security.dependencies import get_current_user
from app.core.db import get_db
from app.services import publisher  # Importar publisher global

router = APIRouter()


@router.post("/photos", response_model=PhotoOut)
def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    file_key = f"users/{current_user.user_id}/photos/{uuid.uuid4()}_{file.filename}"
    photo_url = S3Service().upload_photo(file, file_key)

    photo = Photo(
        url=photo_url,
        order_index=0,
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    # Publicar evento de creación de foto
    publisher.publish_persistence_event(
        event_type='photo_created',
        data={'photo_id': photo.id, 'user_id': current_user.user_id}
    )

    return photo


@router.get("/photos/{photo_id}", response_model=PhotoOut)
def get_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = get_photo_service(db)
    photo = service.get(photo_id, Photo.id)

    if not photo:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    if photo.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta foto")

    # Publicar evento de visualización (triggers se encargarán de incrementar el contador)
    publisher.publish_photo_view(
        photo_id=photo.id,
        user_id=current_user.user_id,
        metadata={'source': 'api'}
    )

    return photo


@router.post("/photos/{photo_id}/reaction")
def add_reaction(
    photo_id: int,
    action: str = 'like',  # like/unlike
    reaction_type_id: int = 1,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = get_photo_service(db)
    photo = service.get(photo_id, Photo.id)
    if not photo:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    # Publicar evento de reacción (triggers en DB se encargarán de actualizar counters)
    publisher.publish_photo_reaction(
        photo_id=photo.id,
        user_id=current_user.user_id,
        reaction_type_id=reaction_type_id,
        metadata={'action': action, 'source': 'api'}
    )

    return {"message": f"Reacción '{action}' enviada para photo_id={photo.id}"}


@router.post("/photos/{photo_id}/comment")
def add_comment(
    photo_id: int,
    comment: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = get_photo_service(db)
    photo = service.get(photo_id, Photo.id)
    if not photo:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    # Publicar evento de comentario (triggers en DB se encargarán de incrementar comments_count)
    publisher.publish_photo_comment(
        photo_id=photo.id,
        user_id=current_user.user_id,
        comment=comment,
        metadata={'source': 'api'}
    )

    return {"message": f"Comentario enviado para photo_id={photo.id}"}


@router.delete("/photos/{photo_id}", response_model=PhotoOut)
def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = get_photo_service(db)
    photo = service.get(photo_id, Photo.id)

    if not photo:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    if photo.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta foto")

    try:
        s3_key = photo.url.split(".amazonaws.com/")[1]
        delete_file_from_s3(s3_key)
    except IndexError:
        raise HTTPException(status_code=400, detail="Formato de URL S3 inválido")

    service.delete(photo_id, Photo.id)

    # Publicar evento de eliminación de foto
    publisher.publish_persistence_event(
        event_type='photo_deleted',
        data={'photo_id': photo.id, 'user_id': current_user.user_id}
    )

    return photo
