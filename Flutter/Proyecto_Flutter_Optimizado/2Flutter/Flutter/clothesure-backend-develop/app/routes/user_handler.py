from fastapi import APIRouter, Depends, Form
from typing import List
from sqlalchemy.orm import Session
from app.dto.user_dto import UserCreate, UserOut, PasswordResetRequest
from app.models.user_model import User
from app.factories.repository_factory import  get_user_service,get_user_device_service
from app.core.db import get_db
from passlib.context import CryptContext
from app.models.user_device_model import UserDevice
from app.dto.user_device_dto import UserDeviceOut
from app.security.jwt import create_access_token
from app.security.google_oauth import oauth
from starlette.responses import RedirectResponse
import os
from fastapi.security import OAuth2PasswordBearer
from app.services.email_helper import send_password_reset_email
from app.security.dependencies import get_current_user
from fastapi import HTTPException, Request,Header
from app.security.dependencies import get_current_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
router = APIRouter()

#get current user information
@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register/", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    service = get_user_service(db)
    return service.register_user(db, user_data.dict())


@router.post("/login/", response_model=dict)
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    fcm_token: str = Form(None),
    device_type: str = Form(None),
    device_name: str = Form(None),
    device_os: str = Form(None),
    browser: str = Form(None),
    db: Session = Depends(get_db)
):
    user_service = get_user_service(db)
    device_service = get_user_device_service(db)
    user = user_service.authenticate_user(email, password)
    if "user_id" in user:
        ip_address = request.client.host 
        device = device_service.register_or_update_device(
            db,
            user_id=user["user_id"],
            fcm_token=fcm_token,
            device_type=device_type,
            device_name=device_name,
            device_os=device_os,
            browser=browser,
            ip_address=ip_address
        )
        # Adjuntar session_token a la respuesta
        user["session_token"] = device.session_token

    return user

#google auth handler
@router.get("/auth/login-google")
async def login_with_google(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    email = user_info.get("email")
    username = user_info.get("name")

    if not email or not username:
        raise HTTPException(status_code=400, detail="Invalid user info from Google")

    service = get_user_service(db)
    user = service.get(email, User.email)

    if not user:
        user = service.create({
            "username": username,
            "email": email,
            "password": ""
        })

    jwt_token = create_access_token(data={"sub": str(user.user_id)})

    # 👇 redirige a tu app con el token
    return RedirectResponse(url=f"galeriq://auth/callback?token={jwt_token}")

#update user information
@router.put("/me/{user_id}", response_model=UserOut)
def update_user(user_id: int, 
                username: str,
                email: str,
                phone: str,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    service = get_user_service(db)
    
    return service.update(user_id,User.user_id, {
        "full_name": username,
        "email": email,
        "phone": phone
    }, current_user.user_id)

@router.post("/password/forgot")
def forgot_password(email: str = Form(...), db: Session = Depends(get_db)):
    service = get_user_service(db)
    user = service.get(email, User.email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    token = service.generate_password_reset_token(email)
    send_password_reset_email(email, token)
    return {
        "msg": "Link de recuperación enviado, revisa tu correo"
    }

@router.post("/password/reset")
def reset_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    service = get_user_service(db)
    user = service.reset_password_with_token(db, request.token, request.new_password)
    return {"msg": "Contraseña actualizada exitosamente", "user_id": user.user_id}

@router.post("/logout")
def logout(session_token: str = Header(...), db: Session = Depends(get_db)):
    device_service = get_user_device_service(db)
    device = device_service.logout_device(db, session_token=session_token)

    if not device:
        raise HTTPException(status_code=404, detail="Device/session not found")

    return {"detail": "Logged out successfully", "device_id": device.id}

@router.post("/logout_all")
def logout_all(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_service = get_user_service(db)
    user_payload = user_service.get_current_user_from_token(token)
    user_id = user_payload["user_id"]

    device_service = get_user_device_service(db)
    device_service.logout_all_devices(db, user_id=user_id)

    return {"detail": f"All sessions for user {user_id} have been logged out"}


@router.get("/sessions", response_model=List[UserDeviceOut])
def list_sessions(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_service = get_user_service(db)
    user_payload = user_service.get_current_user_from_token(token)
    user_id = user_payload["user_id"]

    device_service = get_user_device_service(db)
    device_service.mark_inactive_expired(db)
    devices = db.query(UserDevice).filter(UserDevice.user_id == user_id).all()
    return devices


@router.post("/password/change")
def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = get_user_service(db)
    updated_user = service.update_password(
        db,
        user_id=current_user.user_id,
        old_password=old_password,
        new_password=new_password
    )
    return {"msg": "Contraseña cambiada exitosamente", "user_id": updated_user.user_id}