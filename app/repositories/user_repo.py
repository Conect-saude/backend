# app/repositories/user_repo.py
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()


    def create(self, db: Session, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user