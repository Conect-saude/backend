# app/services/classification.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
import requests
from app.core.config import settings


@dataclass
class ClassificationResult:
    classificacao: str # "normal" | "outlier"
    risk_level: Optional[str] = None
    confidence: Optional[float] = None
    recomendacao: Optional[str] = None


class ClassificationService:
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url or settings.CLASSIFICATION_SERVICE_URL


    def classify(self, row: Dict[str, Any]) -> ClassificationResult:
        # Se houver serviço externo, tenta usar
        if self.base_url:
            try:
                r = requests.post(f"{self.base_url.rstrip('/')}/classify", json=row, timeout=5)
                r.raise_for_status()
                data = r.json()
                return ClassificationResult(
                    classificacao=data.get("classificacao", "normal"),
                    risk_level=data.get("risk_level"),
                    confidence=data.get("confidence"),
                    recomendacao=data.get("recomendacao"),
            )
            except Exception:
                pass
        # Fallback local simples
        glic = (row.get("glicemia_jejum_mg_dl") or 0)
        pas = (row.get("pressao_sistolica_mmHg") or 0)
        pad = (row.get("pressao_diastolica_mmHg") or 0)
        imc = (row.get("imc") or 0.0)


        """ Regras muito simples para MVP """
        score = 0
        if glic >= 126: score += 2
        if pas >= 140 or pad >= 90: score += 2
        if imc >= 30: score += 1


        if score >= 3:
            return ClassificationResult("outlier", risk_level="alto", confidence=0.7, recomendacao="Avaliar com equipe de saúde e verificar adesão terapêutica.")
        elif score == 2:
            return ClassificationResult("outlier", risk_level="moderado", confidence=0.6, recomendacao="Monitorar e reforçar hábitos saudáveis.")
        else:
            return ClassificationResult("normal", risk_level="baixo", confidence=0.5, recomendacao="Manter acompanhamento de rotina.")