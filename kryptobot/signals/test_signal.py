from ..ta.talib_macd import TalibMacd
from ..signals.base_signal_generator import BaseSignalGenerator


class TestSignal(BaseSignalGenerator):
    def __init__(self, market, interval, params, strategy):
        super().__init__(market, interval, strategy)
        self.macd = TalibMacd(self.market, interval, None, params)

    def check_condition(self, new_candle):
        self.strategy.add_message("GETTING TALIB MACD SIGNAL")
        if self.macd.value is not None:
            self.strategy.add_message({
                'timestamp': new_candle[0],
                'open': new_candle[1],
                'high': new_candle[2],
                'low': new_candle[3],
                'close': new_candle[4],
                'volume': new_candle[5],
                'macd': self.macd.value['macd'],
                'macdSignal': self.macd.value['macdSignal'],
                'macdHist': self.macd.value['macdHist'],
                'positions': self.strategy.get_open_position_count(),
                'quote_balance': self.market.get_wallet_balance(),
                'base_balance': self.market.base_balance,
                'exit_balance': self.market.get_wallet_balance()
                    + (self.market.base_balance * ((new_candle[2] + new_candle[3])/ 2))
            }, 'db')
            self.strategy.add_message("macd: " + str(self.macd.value['macd']))
            return False
        return False
