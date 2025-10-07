# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


# Dependency para FastAPI
from contextlib import contextmanager


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Inicialização simplificada p/ MVP
def create_all_tables():
    from app.models import user, paciente, password_reset # noqa: F401 – garantir import dos modelos
    Base.metadata.create_all(bind=engine)