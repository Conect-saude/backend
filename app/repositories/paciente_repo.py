# app/repositories/paciente_repo.py
from typing import Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.paciente import Paciente


class PacienteRepository:
    def create(self, db: Session, data: dict) -> Paciente:
        paciente = Paciente(**data)
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        return paciente


    def get(self, db: Session, paciente_id: int) -> Paciente | None:
        return db.query(Paciente).filter(Paciente.id == paciente_id).first()


    def list_paginated(self, db: Session, page: int, page_size: int, search: str | None) -> Tuple[List[Paciente], int]:
        q = db.query(Paciente)
        if search:
            like = f"%{search}%"
            q = q.filter(Paciente.nome.ilike(like))
        total = q.with_entities(func.count()).scalar() or 0
        items = q.order_by(Paciente.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return items, total