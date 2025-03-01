from fastapi import APIRouter, Request, HTTPException, status, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from ..schemas import ForgotEmail, ResetPassword
from ..mailer import mail, create_message
from ..database import db_dependency
from ..models import User
from ..utils import hash as hash_password
import secrets

router = APIRouter(tags=['forgot_password'])

templates = Jinja2Templates(directory="app/templates")
SECRET_KEY = secrets.token_hex(32)
serializer = URLSafeTimedSerializer(SECRET_KEY)

@router.get("/forgot")
async def render_forgot_page(request: Request):
    return templates.TemplateResponse("forgot.html", {"request": request})

@router.post("/forgot_val")
async def send_reset_email(
    emails: ForgotEmail, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
):
    user = db.query(User).filter(User.email == emails.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    try:
        # Generate a reset token valid for 1 hour
        token = serializer.dumps(user.email, salt="password-reset-salt")
        reset_url = f"http://localhost:8000/reset-password?token={token}"
        html = f"""
        <p>Hello {user.username},</p>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_url}">RESET URL</a>
        <p>This link will expire in 1 hour.</p>
        <h3>Happy Day !!!</h3>
        """
        subject = "Password Reset Request"

        # Use BackgroundTasks to send the email
        background_tasks.add_task(
            send_email_task,
            recipients=[emails.email],
            subject=subject,
            body=html
        )

        return {"message": "Password reset link has been sent to your email!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to send email: {e}")

async def send_email_task(recipients: list, subject: str, body: str):
    """Background task to send an email."""
    message = create_message(recipients=recipients, subject=subject, body=body)
    await mail.send_message(message)

@router.get("/reset-password")
async def render_reset_page(request: Request, token: str):
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)  # 1 hour
        return templates.TemplateResponse("reset_password.html", {"request": request, "email": email, "token": token})
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")

@router.post("/reset-password")
async def reset_password(data: ResetPassword, db: db_dependency):
    try:
        email = serializer.loads(data.token, salt="password-reset-salt", max_age=3600)  # 1 hour
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        # Hash the new password and save it
        user.password = hash_password(data.new_password)
        db.commit()

        return {"message": "Password has been reset successfully!"}
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to reset password: {e}")
