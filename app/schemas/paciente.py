# app/schemas/paciente.py
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.common import PageMeta


# Para simplificar, enums como str – valide no serviço
class PacienteCreate(BaseModel):

    nome: str = Field(..., min_length=2)
    endereco: Optional[str] = None
    sexo: Optional[str] = Field(None, description="masculino|feminino|outro")
    escolaridade: Optional[str] = None
    renda_familiar_sm: Optional[str] = None


    atividade_fisica: Optional[str] = None
    consumo_alcool: Optional[str] = None
    tabagismo_atual: Optional[bool] = False
    qualidade_dieta: Optional[str] = None
    qualidade_sono: Optional[str] = None
    nivel_estresse: Optional[str] = None
    suporte_social: Optional[str] = None
    historico_familiar_dc: Optional[bool] = False
    acesso_servico_saude: Optional[str] = None
    aderencia_medicamento: Optional[str] = None
    consultas_ultimo_ao: Optional[int] = Field(0, ge=0, alias="consultas_ultimo_ano")


    imc: Optional[float] = Field(None, ge=0)
    pressao_sistolica_mmHg: Optional[int] = None
    pressao_diastolica_mmHg: Optional[int] = None
    glicemia_jejum_mg_dl: Optional[int] = None
    colesterol_total_mg_dl: Optional[int] = None
    hdl_mg_dl: Optional[int] = None
    triglicerides_mg_dl: Optional[int] = None


    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nome": "Maria Silva",
                "endereco": "Rua A, 123",
                "sexo": "feminino",
                "escolaridade": "medio",
                "renda_familiar_sm": "2-5",
                "atividade_fisica": "regular",
                "tabagismo_atual": False,
                "imc": 27.5,
                "pressao_sistolica_mmHg": 135,
                "pressao_diastolica_mmHg": 88,
                "glicemia_jejum_mg_dl": 110
            }
        }

class PacienteOut(BaseModel):
    id: int
    nome: str
    endereco: Optional[str]
    sexo: Optional[str]
    escolaridade: Optional[str]
    renda_familiar_sm: Optional[str]
    atividade_fisica: Optional[str]
    consumo_alcool: Optional[str]
    tabagismo_atual: Optional[bool]
    qualidade_dieta: Optional[str]
    qualidade_sono: Optional[str]
    nivel_estresse: Optional[str]
    suporte_social: Optional[str]
    historico_familiar_dc: Optional[bool]
    acesso_servico_saude: Optional[str]
    aderencia_medicamento: Optional[str]
    consultas_ultimo_ano: Optional[int]
    imc: Optional[float]
    pressao_sistolica_mmHg: Optional[int]
    pressao_diastolica_mmHg: Optional[int]
    glicemia_jejum_mg_dl: Optional[int]
    colesterol_total_mg_dl: Optional[int]
    hdl_mg_dl: Optional[int]
    triglicerides_mg_dl: Optional[int]
    classificacao: Optional[str]
    risk_level: Optional[str]
    confidence: Optional[float]
    medidas_a_serem_tomadas: Optional[str]


    class Config:
        from_attributes = True

class PacienteList(BaseModel):
    items: List[PacienteOut]
    meta: PageMeta