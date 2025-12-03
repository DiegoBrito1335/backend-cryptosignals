import pandas as pd
import ta
from typing import Dict, Tuple

class TechnicalAnalysis:
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcular todos os indicadores técnicos
        
        Args:
            df: DataFrame com OHLCV
        
        Returns:
            DataFrame com indicadores adicionados
        """
        # RSI (Relative Strength Index)
        df['rsi'] = ta.momentum.RSIIndicator(
            close=df['close'], 
            window=14
        ).rsi()
        
        # MACD (Moving Average Convergence Divergence)
        macd = ta.trend.MACD(
            close=df['close'],
            window_slow=26,
            window_fast=12,
            window_sign=9
        )
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        
        # EMAs (Exponential Moving Averages)
        df['ema_20'] = ta.trend.EMAIndicator(
            close=df['close'], 
            window=20
        ).ema_indicator()
        
        df['ema_50'] = ta.trend.EMAIndicator(
            close=df['close'], 
            window=50
        ).ema_indicator()
        
        df['ema_200'] = ta.trend.EMAIndicator(
            close=df['close'], 
            window=200
        ).ema_indicator()
        
        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(
            close=df['close'],
            window=20,
            window_dev=2
        )
        df['bb_high'] = bollinger.bollinger_hband()
        df['bb_mid'] = bollinger.bollinger_mavg()
        df['bb_low'] = bollinger.bollinger_lband()
        
        # Volume
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        
        return df
    
    def analyze_trend(self, df: pd.DataFrame) -> Dict:
        """
        Analisar tendência baseado em EMAs
        
        Returns:
            Dicionário com análise da tendência
        """
        last = df.iloc[-1]
        
        # Cruzamento de EMAs
        ema_20 = last['ema_20']
        ema_50 = last['ema_50']
        ema_200 = last['ema_200']
        current_price = last['close']
        
        trend = "NEUTRO"
        
        # Tendência de alta
        if ema_20 > ema_50 > ema_200:
            trend = "ALTA_FORTE"
        elif ema_20 > ema_50:
            trend = "ALTA"
        # Tendência de baixa
        elif ema_20 < ema_50 < ema_200:
            trend = "BAIXA_FORTE"
        elif ema_20 < ema_50:
            trend = "BAIXA"
        
        return {
            "trend": trend,
            "ema_20": float(ema_20),
            "ema_50": float(ema_50),
            "ema_200": float(ema_200),
            "current_price": float(current_price)
        }
    
    def analyze_rsi(self, df: pd.DataFrame) -> Dict:
        """
        Analisar RSI
        
        Returns:
            Dicionário com análise do RSI
        """
        last_rsi = df.iloc[-1]['rsi']
        
        status = "NEUTRO"
        if last_rsi < 30:
            status = "SOBREVENDIDO"  # Oportunidade de compra
        elif last_rsi > 70:
            status = "SOBRECOMPRADO"  # Oportunidade de venda
        
        return {
            "value": float(last_rsi),
            "status": status
        }
    
    def analyze_macd(self, df: pd.DataFrame) -> Dict:
        """
        Analisar MACD
        
        Returns:
            Dicionário com análise do MACD
        """
        last = df.iloc[-1]
        previous = df.iloc[-2]
        
        macd = last['macd']
        macd_signal = last['macd_signal']
        macd_diff = last['macd_diff']
        
        # Detectar cruzamentos
        signal = "NEUTRO"
        
        # Cruzamento para cima (bullish)
        if macd > macd_signal and previous['macd'] <= previous['macd_signal']:
            signal = "COMPRA"
        # Cruzamento para baixo (bearish)
        elif macd < macd_signal and previous['macd'] >= previous['macd_signal']:
            signal = "VENDA"
        elif macd > macd_signal:
            signal = "ALTA"
        elif macd < macd_signal:
            signal = "BAIXA"
        
        return {
            "macd": float(macd),
            "signal": float(macd_signal),
            "histogram": float(macd_diff),
            "status": signal
        }
    
    def analyze_volume(self, df: pd.DataFrame) -> Dict:
        """
        Analisar volume
        
        Returns:
            Dicionário com análise de volume
        """
        last = df.iloc[-1]
        
        current_volume = last['volume']
        avg_volume = last['volume_sma']
        
        status = "NORMAL"
        if current_volume > avg_volume * 1.5:
            status = "ALTO"
        elif current_volume < avg_volume * 0.5:
            status = "BAIXO"
        
        return {
            "current": float(current_volume),
            "average": float(avg_volume),
            "status": status
        }
    
    def get_full_analysis(self, df: pd.DataFrame) -> Dict:
        """
        Análise técnica completa
        
        Returns:
            Dicionário com todas as análises
        """
        # Calcular indicadores
        df = self.calculate_indicators(df)
        
        # Obter última linha
        last = df.iloc[-1]
        
        return {
            "trend": self.analyze_trend(df),
            "rsi": self.analyze_rsi(df),
            "macd": self.analyze_macd(df),
            "volume": self.analyze_volume(df),
            "bollinger": {
                "upper": float(last['bb_high']),
                "middle": float(last['bb_mid']),
                "lower": float(last['bb_low']),
                "current_price": float(last['close'])
            }
        }

# Instância global
technical_analysis = TechnicalAnalysis()