# app/main.py (trechos relevantes)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_all_tables


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)


# CORS – restringir em produção
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Criar tabelas no startup (MVP; depois migrar p/ Alembic)
@app.on_event("startup")
async def on_startup():
    create_all_tables()


# Routers novos
from app.routers import auth as auth_router
from app.routers import pacientes as pacientes_router


app.include_router(auth_router.router)
app.include_router(pacientes_router.router)


# Health/Ready – acrescente verificação de DB
from sqlalchemy import text
from app.core.database import SessionLocal


@app.get("/health/ready")
async def health_ready():
    status = {"db": "ok"}
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        status["db"] = "error"
    overall = "ready" if status["db"] == "ok" else "degraded"
    return {"status": overall, "dependencies": status}