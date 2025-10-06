# app/repositories/password_reset_repo.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.password_reset import PasswordResetToken


class PasswordResetRepository:
    def create(self, db: Session, user_id: int, token: str, expires_at: datetime) -> PasswordResetToken:
        prt = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(prt)
        db.commit()
        db.refresh(prt)
        return prt


    def use(self, db: Session, token: str) -> PasswordResetToken | None:
        prt = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
        return prt


    def mark_used(self, db: Session, prt: PasswordResetToken):
        prt.used = True
        db.commit()