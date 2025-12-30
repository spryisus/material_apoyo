from app.cloud.ses import SESService
import os

ses_service = SESService()


def send_password_reset_email(user_email: str, token: str):
    frontend_domain = os.getenv("FRONTEND_DOMAIN", "http://galeriq-reset-psw.s3-website-us-east-1.amazonaws.com")
    reset_link = f"{frontend_domain}/reset-password?token={token}"

    subject = "Restablece tu contraseña"
    html_body = f"""
        <h1>Recupera tu contraseña</h1>
        <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
        <p>Para continuar, da clic en el siguiente enlace:</p>
        <a href="{reset_link}">Click Aquí!</a>
        <p>Si no solicitaste este cambio, ignora este correo.</p>
    """

    return ses_service.send_email(
        recipient=user_email,
        subject=subject,
        html_body=html_body,
    )
