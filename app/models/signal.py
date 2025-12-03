from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.database import Base

class Signal(Base):
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informações do sinal
    moeda = Column(String, nullable=False, index=True)  # BTC/USDT
    tipo = Column(String, nullable=False)  # LONG ou SHORT
    timeframe = Column(String, nullable=False)  # 1h, 4h, 1d
    
    # Preços
    preco_entrada = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit_1 = Column(Float, nullable=False)
    take_profit_2 = Column(Float, nullable=False)
    take_profit_3 = Column(Float, nullable=False)
    
    # Configurações
    alavancagem = Column(Integer, default=5)
    probabilidade = Column(Float, nullable=False)  # 0-100
    
    # Status
    status = Column(String, default="ATIVO")  # ATIVO, TP1, TP2, TP3, SL, EXPIRADO
    
    # Indicadores técnicos
    indicadores = Column(JSON)  # {rsi: 62, macd: {...}, ema20: ..., etc}
    
    # Análise detalhada
    analise = Column(JSON)  # {resumo: "...", confluencias: [...], estrategia: "..."}
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    expira_em = Column(DateTime(timezone=True))
    
    # Resultado (quando fechar)
    preco_saida = Column(Float, nullable=True)
    resultado_percentual = Column(Float, nullable=True)