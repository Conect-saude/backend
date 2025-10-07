# app/routers/pacientes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import jwt
from app.core.database import get_db
from app.schemas.paciente import PacienteCreate, PacienteOut, PacienteList
from app.schemas.common import PageMeta
from app.repositories.paciente_repo import PacienteRepository
from app.services.classification import ClassificationService
from app.core.config import settings
from app.core.security import decode_token


router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])
repo = PacienteRepository()
classifier = ClassificationService()


# Dependência simples de auth via Bearer JWT (MVP)
def get_current_user_id(authorization: str = Query(None, alias="Authorization")) -> int:
    # Aceita também via header padrão pela aplicação – aqui fallback via Query p/ Swagger rápido
    # Em produção, use Security/OAuth2PasswordBearer
    if not authorization:
        raise HTTPException(status_code=401, detail="Token ausente")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    sub = decode_token(parts[1])
    if not sub:
        raise HTTPException(status_code=401, detail="Token inválido")
    return int(sub)


@router.get("", response_model=PacienteList)
def list_pacientes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    _user_id: int = Depends(get_current_user_id),
):
    items, total = repo.list_paginated(db, page=page, page_size=page_size, search=search)
    return PacienteList(
        items=[PacienteOut.model_validate(i, from_attributes=True) for i in items],
        meta=PageMeta(page=page, page_size=page_size, total=total),
    )


@router.post("", response_model=PacienteOut, status_code=201)
def create_paciente(
    body: PacienteCreate,
    db: Session = Depends(get_db),
    _user_id: int = Depends(get_current_user_id),
):
    data = body.model_dump(by_alias=True)


    # Ajuste simples de campos alias
    if "consultas_ultimo_ao" in data:
        data["consultas_ultimo_ano"] = data.pop("consultas_ultimo_ao")


    # Classificação de risco: usa serviço externo se disponível; senão fallback local
    result = classifier.classify(data)
    data.update(
        {
        "classificacao": result.classificacao,
        "risk_level": result.risk_level,
        "confidence": result.confidence,
        "medidas_a_serem_tomadas": result.recomendacao,
        }
    )

    created = repo.create(db, data)
    return PacienteOut.model_validate(created, from_attributes=True)


@router.get("/{paciente_id}", response_model=PacienteOut)
def get_paciente(paciente_id: int, db: Session = Depends(get_db), _user_id: int = Depends(get_current_user_id)):
    obj = repo.get(db, paciente_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return PacienteOut.model_validate(obj, from_attributes=True)