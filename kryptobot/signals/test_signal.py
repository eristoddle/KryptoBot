# from ..ta.talib_macd import TalibMacd
from ..ta.talib_rsi import TalibRsi
# from ..ta.pyti_average_true_range import PytiAverageTrueRange
from ..ta.pyti_rsi import PytiRsi
from ..signals.base_signal_generator import BaseSignalGenerator


class TestSignal(BaseSignalGenerator):
    def __init__(self, market, interval, params, strategy):
        super().__init__(market, interval, strategy)
        # self.macd = TalibMacd(self.market, interval, params['period'], params)
        # self.atr = PytiAverageTrueRange(market, interval, params['period'], params)
        print('params',market, interval, params['rsi_period'], {'period': params['rsi_period']})
        # self.rsi = TalibRsi(market, interval, params['rsi_period'], params)
        self.rsi = PytiRsi(market, interval, params['rsi_period'], params)
        print(self.rsi)

    def check_condition(self, new_candle):
        self.strategy.add_message("TestSignal")
        print('rsi', self.rsi.value)
        # self.strategy.add_message({
        #     'timestamp': new_candle[0],
        #     'open': new_candle[1],
        #     'high': new_candle[2],
        #     'low': new_candle[3],
        #     'close': new_candle[4],
        #     'volume': new_candle[5],
        #     'positions': self.strategy.get_open_position_count(),
        #     'quote_balance': self.market.get_wallet_balance(),
        #     'base_balance': self.market.base_balance,
        #     'exit_balance': self.market.get_wallet_balance()
        #         + (self.market.base_balance * ((new_candle[2] + new_candle[3])/ 2))
        # }, 'db')
        return False
