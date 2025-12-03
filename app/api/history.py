from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/")
def get_history(
    moeda: str = None,
    tipo: str = None,
    resultado: str = None
):
    """
    Buscar histórico de sinais fechados
    
    Por enquanto retorna dados mockados
    (no futuro, buscar do banco de dados)
    """
    # Dados mockados por enquanto
    moedas = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT']
    
    history = []
    for i in range(50):
        tipo_signal = random.choice(['LONG', 'SHORT'])
        lucro = random.choice([True, True, True, False])  # 75% win rate
        
        if lucro:
            resultado_pct = round(random.uniform(0.5, 5.0), 2)
            status = random.choice(['TP1', 'TP2', 'TP3'])
        else:
            resultado_pct = round(random.uniform(-3.0, -0.5), 2)
            status = 'SL'
        
        moeda_escolhida = random.choice(moedas)
        preco_entrada = random.uniform(100, 100000)
        preco_saida = preco_entrada * (1 + resultado_pct/100)
        
        history.append({
            "id": i + 1,
            "moeda": moeda_escolhida,
            "tipo": tipo_signal,
            "preco_entrada": round(preco_entrada, 2),
            "preco_saida": round(preco_saida, 2),
            "resultado_percentual": resultado_pct,
            "status": status,
            "criado_em": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
        })
    
    # Aplicar filtros
    if moeda:
        history = [h for h in history if h['moeda'] == moeda]
    
    if tipo:
        history = [h for h in history if h['tipo'] == tipo.upper()]
    
    if resultado:
        if resultado == "LUCRO":
            history = [h for h in history if h['resultado_percentual'] > 0]
        elif resultado == "PREJUIZO":
            history = [h for h in history if h['resultado_percentual'] < 0]
    
    return {
        "total": len(history),
        "history": history
    }