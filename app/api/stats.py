from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/")
def get_stats():
    """
    Buscar estatísticas gerais
    
    Por enquanto retorna dados mockados
    """
    return {
        "win_rate_geral": 78.0,
        "win_rate_long": 82.0,
        "win_rate_short": 71.0,
        "total_operacoes": 248,
        "operacoes_long": 150,
        "operacoes_short": 98,
        "lucro_total_brl": 12450.00,
        "lucro_total_usd": 2490.00,
        "melhor_sequencia": 8,
        "melhor_moeda": "LINK/USDT",
        "melhor_moeda_win_rate": 100.0,
        "performance_mensal": [
            {"mes": "Jun", "win_rate": 65},
            {"mes": "Jul", "win_rate": 70},
            {"mes": "Ago", "win_rate": 68},
            {"mes": "Set", "win_rate": 75},
            {"mes": "Out", "win_rate": 73},
            {"mes": "Nov", "win_rate": 78}
        ],
        "performance_por_moeda": [
            {"moeda": "BTC/USDT", "win_rate": 85, "operacoes": 45},
            {"moeda": "ETH/USDT", "win_rate": 78, "operacoes": 38},
            {"moeda": "SOL/USDT", "win_rate": 72, "operacoes": 32},
            {"moeda": "BNB/USDT", "win_rate": 80, "operacoes": 28},
            {"moeda": "ADA/USDT", "win_rate": 65, "operacoes": 25}
        ]
    }