from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.services.binance_service import binance_service
from app.services.technical_analysis import technical_analysis
from app.services.signal_generator import signal_generator
from app.api import signals, history, stats
#from app.database import engine, Base

# Importar rotas (vamos criar depois)
# app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
# app.include_router(history.router, prefix="/api/history", tags=["history"])
# app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

# Criar tabelas
#Base.metadata.create_all(bind=engine)

# Criar app
app = FastAPI(
    title="CryptoSignals Pro API",
    description="API de sinais de trading de criptomoedas",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "CryptoSignals Pro API",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ADICIONAR ESTE ENDPOINT NOVO:
@app.get("/test/price/{symbol}")
def test_price(symbol: str):
    """
    Testar busca de preço
    Exemplo: /test/price/BTCUSDT
    """
    # Converter BTCUSDT para BTC/USDT
    formatted_symbol = f"{symbol[:-4]}/{symbol[-4:]}"
    
    price = binance_service.get_price(formatted_symbol)
    
    if price:
        return {
            "symbol": formatted_symbol,
            "price": price,
            "timestamp": "agora"
        }
    else:
        return {"error": "Não foi possível buscar o preço"}

@app.get("/test/top-coins")
def test_top_coins():
    """
    Testar busca dos top coins por volume
    """
    symbols = binance_service.get_top_volume_pairs(limit=10)
    prices = binance_service.get_multiple_prices(symbols)
    
    result = []
    for symbol, price in prices.items():
        result.append({
            "symbol": symbol,
            "price": price
        })
    
    return {
        "total": len(result),
        "coins": result
    }

@app.get("/test/analysis/{symbol}")
def test_analysis(symbol: str, timeframe: str = "1h"):
    """
    Testar análise técnica completa
    Exemplo: /test/analysis/BTCUSDT?timeframe=1h
    """
    # Converter BTCUSDT para BTC/USDT
    formatted_symbol = f"{symbol[:-4]}/{symbol[-4:]}"
    
    # Buscar dados históricos
    df = binance_service.get_ohlcv(formatted_symbol, timeframe=timeframe, limit=200)
    
    if df is None or df.empty:
        return {"error": "Não foi possível buscar dados"}
    
    # Fazer análise
    analysis = technical_analysis.get_full_analysis(df)
    
    return {
        "symbol": formatted_symbol,
        "timeframe": timeframe,
        "analysis": analysis
    }

@app.get("/test/generate-signal/{symbol}")
def test_generate_signal(symbol: str, timeframe: str = "1h"):
    """
    Testar geração de sinal completo
    Exemplo: /test/generate-signal/BTCUSDT?timeframe=1h
    """
    # Converter BTCUSDT para BTC/USDT
    formatted_symbol = f"{symbol[:-4]}/{symbol[-4:]}"
    
    signal = signal_generator.generate_signal(formatted_symbol, timeframe)
    
    if signal:
        return {
            "success": True,
            "signal": signal
        }
    else:
        return {
            "success": False,
            "message": "Nenhum sinal claro detectado no momento"
        }

@app.get("/test/generate-signals-top10")
def test_generate_signals_top10(timeframe: str = "1h"):
    """
    Gerar sinais para top 10 moedas
    Exemplo: /test/generate-signals-top10?timeframe=4h
    """
    # Buscar top moedas
    top_symbols = binance_service.get_top_volume_pairs(limit=10)
    
    # Gerar sinais
    signals = signal_generator.generate_signals_batch(top_symbols, timeframe)
    
    return {
        "total_analyzed": len(top_symbols),
        "signals_generated": len(signals),
        "signals": signals
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}




# Importar rotas (vamos criar depois)

app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])




