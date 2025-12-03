from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class SignalBase(BaseModel):
    moeda: str
    tipo: str  # LONG ou SHORT
    timeframe: str
    preco_entrada: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    take_profit_3: float
    alavancagem: int = 5
    probabilidade: float
    status: str = "ATIVO"

class SignalCreate(SignalBase):
    indicadores: Dict
    analise: Dict
    expira_em: datetime

class SignalResponse(SignalBase):
    id: int
    indicadores: Dict
    analise: Dict
    criado_em: datetime
    atualizado_em: Optional[datetime]
    expira_em: datetime
    preco_saida: Optional[float] = None
    resultado_percentual: Optional[float] = None
    
    class Config:
        from_attributes = True

class SignalList(BaseModel):
    total: int
    signals: List[SignalResponse]