# from ..ta.talib_rsi import TalibRsi
from ..ta.pyti_average_true_range import PytiAverageTrueRange
from ..ta.pyti_average_true_range_percent import PytiAverageTrueRangePercent
from ..ta.pyti_rsi import PytiRsi
from ..ta.pyti_accumulation_distribution import PytiAccumulationDistribution
from ..ta.pyti_aroon import PytiAroon
from ..ta.pyti_bollinger_bands import PytiBollingerBands
from ..ta.pyti_chaikin_money_flow import PytiChaikinMoneyFlow
from ..ta.pyti_chande_momentum_oscillator import PytiChandeMomentumOscillator
from ..ta.pyti_commodity_channel_index import PytiCommodityChannelIndex
from ..ta.pyti_detrended_price_oscillator import PytiDetrendedPriceOscillator
from ..ta.pyti_directional_indicators import PytiDirectionalIndicators
from ..ta.pyti_double_exponential_moving_average import PytiDema
# from ..ta.pyti_double_smoothed_stochastic import PytiDoubleSmoothedStochastic
from ..ta.pyti_exponential_moving_average import PytiEma
from ..ta.pyti_hull_moving_average import PytiHullMovingAverage
# TODO: Special case with multiple periods
# from ..ta.pyti_ichimoku_cloud import PytiIchimokuCloud
# TODO: Special case with multiple periods
# from ..ta.pyti_keltner_bands import PytiIKeitnerBands
from ..ta.pyti_linear_weighted_moving_average import PytiLwma
from ..ta.pyti_momentum import PytiMomentum
from ..ta.pyti_money_flow import PytiMoneyFlow
from ..ta.pyti_money_flow_index import PytiMoneyFlowIndex
# TODO: Special case with multiple periods
# from ..ta.pyti_moving_average_convergence_divergence import PytiMacd
# TODO: pyti lib won't import?
# from ..ta.pyti_moving_average_envelope import PytiMovingAverageEnvelope
from ..signals.base_signal_generator import BaseSignalGenerator


class TestSignal(BaseSignalGenerator):
    def __init__(self, market, interval, params, strategy):
        super().__init__(market, interval, strategy)
        # self.rsi = TalibRsi(market, interval, params['rsi_period'], params)
        pyti_params = {
            'market': market,
            'interval': interval,
            'periods': params['period'],
            'params': params
        }
        # TODO: Aroon returning both down results
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
        self.atr = PytiAverageTrueRange(**pyti_params)
        self.atrp = PytiAverageTrueRangePercent(**pyti_params)
        self.rsi = PytiRsi(**pyti_params)
        self.ad = PytiAccumulationDistribution(market, interval, None, None)
        self.bb = PytiBollingerBands(**pyti_params)
        self.chaikin = PytiChaikinMoneyFlow(**pyti_params)
        self.chande = PytiChandeMomentumOscillator(**pyti_params)
        self.cci = PytiCommodityChannelIndex(**pyti_params)
        self.dpo = PytiDetrendedPriceOscillator(**pyti_params)
        self.directional = PytiDirectionalIndicators(**pyti_params)
        # TODO: Not working?
        self.dema = PytiDema(**pyti_params)
        # TODO: Not sure of the parameters
        # self.dss = PytiDoubleSmoothedStochastic(**pyti_params)
        self.ema = PytiEma(**pyti_params)
        # TODO: Not working?
        self.hma = PytiHullMovingAverage(**pyti_params)
        self.lwma = PytiLwma(**pyti_params)
        self.momentum = PytiMomentum(**pyti_params)
        self.mf = PytiMoneyFlow(**pyti_params)
        # TODO: Not working?
        self.mfi = PytiMoneyFlowIndex(**pyti_params)
        # self.mae = PytiMovingAverageEnvelope(**pyti_params)

    def check_condition(self, new_candle):
        self.strategy.add_message("TestSignal")
        print('rsi', self.rsi.value)
        print('atr', self.atr.value)
        print('atrp', self.atrp.value)
        print('ad', self.ad.value)
        print('aroon_up', self.aroon_up.value)
        print('aroon_down', self.aroon_down.value)
        print('bb', self.bb.value)
        print('chaikin', self.chaikin.value)
        print('chande', self.chande.value)
        print('cci', self.cci.value)
        print('dpo', self.dpo.value)
        print('directional', self.directional.value)
        print('dema', self.dema.value)
        # print('dss', self.dss.value)
        print('ema', self.ema.value)
        print('hma', self.hma.value)
        print('lwma', self.lwma.value)
        print('momentum', self.momentum.value)
        print('mf', self.mf.value)
        print('mfi', self.mfi.value)
        print('mae', self.mae.value)

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
            'bb': self.bb.value,
            'chaikin': self.chaikin.value,
            'chande': self.chande.value,
            'cci': self.cci.value,
            'dpo': self.dpo.value,
            'directional': self.directional.value,
            'dema': self.dema.value,
            # 'dss': self.dss.value,
            'ema': self.ema.value,
            'hma': self.hma.value,
            'lwma': self.lwma.value,
            'momentum': self.momentum.value,
            'mf': self.mf.value,
            'mfi': self.mfi.value,
            # 'mae': self.mae.value,
        }, 'db')

        return False
