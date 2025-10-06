# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from app.core.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.repositories.password_reset_repo import PasswordResetRepository
from app.core.email import send_email


router = APIRouter(prefix="/auth", tags=["Auth"])


user_repo = UserRepository()
prt_repo = PasswordResetRepository()


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    if user_repo.get_by_email(db, body.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    user = user_repo.create(db, body.email, hash_password(body.password))
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, body.email)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, body.email)
    if not user:
        # Para privacidade, responder mensagem genérica
        return {"message": "Se o e-mail existir, você receberá instruções."}
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=2)
    prt_repo.create(db, user_id=user.id, token=token, expires_at=expires)


    reset_link = f"https://frontend/reset?token={token}"
    send_email(
        to_email=user.email,
        subject="Redefinição de senha – Conecta+Saúde",
        html=f"<p>Use o link para redefinir sua senha (expira em 2h):<br><a href='{reset_link}'>Redefinir senha</a></p>",
    )
    return {"message": "Se o e-mail existir, você receberá instruções."}


@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    prt = prt_repo.use(db, body.token)
    if not prt or prt.used or prt.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")
    user = prt.user
    user.hashed_password = hash_password(body.new_password)
    prt_repo.mark_used(db, prt)
    db.commit()
    return {"message": "Senha atualizada com sucesso"}