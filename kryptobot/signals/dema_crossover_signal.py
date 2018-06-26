from ..ta.exponential_moving_average import ExponentialMovingAverage
from ..signals.base_signal_generator import BaseSignalGenerator


class DEMACrossoverSignal(BaseSignalGenerator):
    """"This signal generator is a copy of the DEMA strategy example used in gekko
    This strategy is similar to the sma_crossover_signal except is is simpler in that it does not worry about caching candles
    ...it simply signals true when FMA > SMA and false whe SMA > FMA at an amount greater than the threshold"""
    def __init__(self, market, interval, ema_short, ema_long, threshold, strategy):
        super().__init__(market, interval, strategy)
        self.fma = ExponentialMovingAverage(self.market, interval, ema_short)
        self.sma = ExponentialMovingAverage(self.market, interval, ema_long)
        self.threshold = threshold

    def check_condition(self, new_candle):
        """will run every time a new candle is pulled"""
        self.strategy.add_message("GETTING DEMA CROSSOVER SIGNAL")
        if (self.sma.value is not None) & (self.fma.value is not None):
            self.strategy.add_message({
                'timestamp': new_candle[0],
                'open': new_candle[1],
                'high': new_candle[2],
                'low': new_candle[3],
                'close': new_candle[4],
                'volume': new_candle[5],
                'sma': self.sma.value,
                'fma': self.fma.value,
                'positions': self.strategy.get_open_position_count(),
                'quote_balance': self.market.get_wallet_balance(),
                'base_balance': self.market.base_balance,
                'sell_all_balance': self.market.get_wallet_balance()
                    + (self.market.base_balance * ((new_candle[2] + new_candle[3])/ 2))
            }, 'db')
            self.strategy.add_message("SMA: " + str(self.sma.value))
            self.strategy.add_message("FMA: " + str(self.fma.value))
            if (self.fma.value - self.sma.value) > self.threshold:
                self.strategy.add_message("Currently in up-trend. Buy signal TRUE")
                return True
        return False
