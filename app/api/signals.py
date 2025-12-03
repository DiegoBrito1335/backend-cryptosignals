from fastapi import APIRouter, Query
from typing import List, Optional
from app.services.binance_service import binance_service
from app.services.signal_generator import signal_generator

router = APIRouter()

@router.get("/")
def get_signals(
    moeda: Optional[str] = None,
    tipo: Optional[str] = None,
    probabilidade_min: Optional[int] = 0,
    timeframe: str = "1h"
):
    """
    Buscar sinais ativos
    
    Query params:
    - moeda: Filtrar por moeda (ex: BTC/USDT)
    - tipo: Filtrar por tipo (LONG ou SHORT)
    - probabilidade_min: Probabilidade mínima (0-100)
    - timeframe: Timeframe (1h, 4h, 1d)
    """
    # Buscar top moedas
    top_symbols = binance_service.get_top_volume_pairs(limit=15)
    
    # Gerar sinais
    signals = signal_generator.generate_signals_batch(top_symbols, timeframe)
    
    # Aplicar filtros
    if moeda:
        signals = [s for s in signals if s['moeda'] == moeda]
    
    if tipo:
        signals = [s for s in signals if s['tipo'] == tipo.upper()]
    
    if probabilidade_min:
        signals = [s for s in signals if s['probabilidade'] >= probabilidade_min]
    
    # Ordenar por probabilidade (maior primeiro)
    signals = sorted(signals, key=lambda x: x['probabilidade'], reverse=True)
    
    return {
        "total": len(signals),
        "signals": signals
    }

@router.get("/{signal_id}")
def get_signal_detail(signal_id: str):
    """
    Buscar detalhes de um sinal específico
    
    Por enquanto, gera o sinal novamente
    (no futuro, buscar do banco de dados)
    """
    # Extrair símbolo do ID (simplificado)
    # Exemplo: signal_id = "BTC-USDT-1h"
    parts = signal_id.split("-")
    if len(parts) >= 3:
        symbol = f"{parts[0]}/{parts[1]}"
        timeframe = parts[2]
        
        signal = signal_generator.generate_signal(symbol, timeframe)
        
        if signal:
            return signal
    
    return {"error": "Sinal não encontrado"}