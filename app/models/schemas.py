from pydantic import BaseModel
from typing import List, Optional

class LogRequest(BaseModel):
    log: str

class AIResponse(BaseModel):
    tipo_erro: str
    resumo: str
    causa_raiz: str
    severidade: str # BAIXO, MEDIO, ALTO
    sugestao_solucao: str

class SimilarCase(BaseModel):
    id: int
    resumo: str
    causa: str
    solucao: str

class AnalyzeResponse(BaseModel):
    summary: str
    cause: str
    solution: str
    severity: str
    similar_cases: List[SimilarCase] = []
