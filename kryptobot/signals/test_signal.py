# from ..ta.talib_rsi import TalibRsi
from ..ta.pyti_average_true_range import PytiAverageTrueRange
from ..ta.pyti_average_true_range_percent import PytiAverageTrueRangePercent
from ..ta.pyti_rsi import PytiRsi
from ..ta.pyti_accumulation_distribution import PytiAccumulationDistribution
from ..ta.pyti_aroon import PytiAroon
from ..ta.pyti_bollinger_bands import PytiBollingerBands
from ..signals.base_signal_generator import BaseSignalGenerator


class TestSignal(BaseSignalGenerator):
    def __init__(self, market, interval, params, strategy):
        super().__init__(market, interval, strategy)
        # self.rsi = TalibRsi(market, interval, params['rsi_period'], params)
        self.atr = PytiAverageTrueRange(
            market,
            interval,
            params['period'],
            params
        )
        self.atrp = PytiAverageTrueRangePercent(
            market,
            interval,
            params['period'],
            params
        )
        self.rsi = PytiRsi(market, interval, params['period'], params)
        self.ad = PytiAccumulationDistribution(market, interval, None, None)
        aroon_up_params = params
        aroon_up_params['aroon_direction'] = 'up'
        self.aroon_up = PytiAroon(
            market,
            interval,
            params['period'],
            aroon_up_params
        )
        aroon_down_params = params
        aroon_down_params['aroon_direction'] = 'down'
        self.aroon_down = PytiAroon(
            market,
            interval,
            params['period'],
            aroon_down_params
        )
        self.bb = PytiBollingerBands(
            market,
            interval,
            params['period'],
            params
        )

    def check_condition(self, new_candle):
        self.strategy.add_message("TestSignal")
        print('rsi', self.rsi.value)
        print('atr', self.atr.value)
        print('atrp', self.atrp.value)
        print('ad', self.ad.value)
        print('aroon_up', self.aroon_up.value)
        print('aroon_down', self.aroon_down.value)
        print('bb', self.bb.value)

        self.strategy.add_message({
            'timestamp': new_candle[0],
            'open': new_candle[1],
            'high': new_candle[2],
            'low': new_candle[3],
            'close': new_candle[4],
            'volume': new_candle[5],
            'positions': self.strategy.get_open_position_count(),
            'quote_balance': self.market.get_wallet_balance(),
            'base_balance': self.market.base_balance,
            'exit_balance': self.market.get_wallet_balance()
                    + (self.market.base_balance *
                    ((new_candle[2] + new_candle[3])/ 2)),
            'rsi': self.rsi.value,
            'atr': self.atr.value,
            'atrp': self.atrp.value,
            'ad': self.ad.value,
            'aroon_up': self.aroon_up.value,
            'aroon_down': self.aroon_down.value,
            'bb': self.bb.value
        }, 'db')

        return False
