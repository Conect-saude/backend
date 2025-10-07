# app/core/config.py (trecho ilustrativo)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Conecta+Saúde API"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "API Backend para análise de pacientes com IA - Conecta+Saúde"


    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8082


    DATABASE_URL: str


    API_V1_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"


    ALLOWED_ORIGINS: str = "*"


    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60


    # SMTP
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 25
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM: str | None = None


    # Classificação
    CLASSIFICATION_SERVICE_URL: str | None = None


    class Config:
        env_file = ".env"


settings = Settings()