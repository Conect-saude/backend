# app/models/paciente.py
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, func
from app.core.database import Base


# Enums simples representados como String com validação na camada de schema/serviço para MVP
# (Depois pode migrar para tipos Enum no SQL)

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), index=True, nullable=False)
    endereco = Column(String(300), nullable=True)
    sexo = Column(String(10), nullable=True) # {"masculino","feminino","outro"}
    escolaridade = Column(String(30), nullable=True) # e.g., {"fundamental","medio","superior"}
    renda_familiar_sm = Column(String(20), nullable=True) # e.g., {"<1","1-2","2-5","5+"}


    # Hábitos/condições
    atividade_fisica = Column(String(20), nullable=True)
    consumo_alcool = Column(String(20), nullable=True)
    tabagismo_atual = Column(Boolean, default=False)
    qualidade_dieta = Column(String(20), nullable=True)
    qualidade_sono = Column(String(20), nullable=True)
    nivel_estresse = Column(String(20), nullable=True)
    suporte_social = Column(String(20), nullable=True)
    historico_familiar_dc = Column(Boolean, default=False)
    acesso_servico_saude = Column(String(30), nullable=True)
    aderencia_medicamento = Column(String(30), nullable=True)
    consultas_ultimo_ano = Column(Integer, default=0)


    # Medidas/Exames
    imc = Column(Float, nullable=True)
    pressao_sistolica_mmHg = Column(Integer, nullable=True)
    pressao_diastolica_mmHg = Column(Integer, nullable=True)
    glicemia_jejum_mg_dl = Column(Integer, nullable=True)
    colesterol_total_mg_dl = Column(Integer, nullable=True)
    hdl_mg_dl = Column(Integer, nullable=True)
    triglicerides_mg_dl = Column(Integer, nullable=True)


    # Resultado IA
    classificacao = Column(String(20), nullable=True) # {"normal","outlier"}
    risk_level = Column(String(20), nullable=True) # {"baixo","moderado","alto"}
    confidence = Column(Float, nullable=True)
    medidas_a_serem_tomadas = Column(Text, nullable=True)


    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)