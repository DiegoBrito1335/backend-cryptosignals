import ccxt
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

class BinanceService:
    def __init__(self):
        # Inicializar exchange Binance (sem API keys para dados públicos)
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',  # Futuros
            }
        })
    
    def get_price(self, symbol: str) -> float:
        """
        Buscar preço atual de um par
        
        Args:
            symbol: Par de trading (ex: 'BTC/USDT')
        
        Returns:
            Preço atual
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            print(f"Erro ao buscar preço de {symbol}: {e}")
            return None
    
    def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        """
        Buscar dados OHLCV (Open, High, Low, Close, Volume)
        
        Args:
            symbol: Par de trading (ex: 'BTC/USDT')
            timeframe: Timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
            limit: Número de candles
        
        Returns:
            DataFrame com dados OHLCV
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # Converter para DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # Converter timestamp para datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            return df
        
        except Exception as e:
            print(f"Erro ao buscar OHLCV de {symbol}: {e}")
            return None
    
    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, float]:
        """
        Buscar preços de múltiplos pares
        
        Args:
            symbols: Lista de pares ['BTC/USDT', 'ETH/USDT', ...]
        
        Returns:
            Dicionário {symbol: price}
        """
        prices = {}
        for symbol in symbols:
            price = self.get_price(symbol)
            if price:
                prices[symbol] = price
        return prices
    
    def get_top_volume_pairs(self, limit: int = 10) -> List[str]:
        """
        Buscar pares com maior volume
        
        Args:
            limit: Número de pares a retornar
        
        Returns:
            Lista de símbolos
        """
        try:
            tickers = self.exchange.fetch_tickers()
            
            # Filtrar apenas USDT pairs
            usdt_pairs = {
                symbol: data for symbol, data in tickers.items()
                if '/USDT' in symbol and data['quoteVolume']
            }
            
            # Ordenar por volume
            sorted_pairs = sorted(
                usdt_pairs.items(),
                key=lambda x: x[1]['quoteVolume'],
                reverse=True
            )
            
            # Retornar top N
            return [pair[0] for pair in sorted_pairs[:limit]]
        
        except Exception as e:
            print(f"Erro ao buscar pares por volume: {e}")
            # Retornar pares padrão se falhar
            return [
                'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 
                'SOL/USDT', 'ADA/USDT'
            ]

# Instância global
binance_service = BinanceService()