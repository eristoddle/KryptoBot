# NOTE: Indicators with more than one period must be a standalone signal
import math
from ..ta.volume_change_monitor import VolumeChangeMonitor
from ..ta.pyti_average_true_range import PytiAverageTrueRange
from ..ta.pyti_average_true_range_percent import PytiAverageTrueRangePercent
from ..ta.pyti_rsi import PytiRsi
from ..ta.pyti_accumulation_distribution import PytiAccumulationDistribution
from ..ta.pyti_aroon import PytiAroon
from ..ta.pyti_bollinger_bands import PytiBollingerBands
# TODO: Works but random invalid value encountered in true_divide
# from ..ta.pyti_chaikin_money_flow import PytiChaikinMoneyFlow
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
from ..ta.pyti_moving_average_envelope import PytiMovingAverageEnvelope
from ..ta.pyti_on_balance_volume import PytiOnBalanceVolume
from ..ta.pyti_price_channels import PytiPriceChannels
# TODO: Special case with multiple periods
# from ..ta.pyti_price_oscillator import PytiPriceOscillator
from ..ta.pyti_rate_of_change import PytiRateOfChange
from ..ta.pyti_simple_moving_average import PytiSimpleMovingAverage
from ..ta.pyti_smoothed_moving_average import PytiSmoothedMovingAverage
from ..ta.pyti_standard_deviation import PytiStandardDeviation
from ..ta.pyti_standard_variance import PytiStandardVariance
from ..ta.pyti_stochastic import PytiStochastic
from ..ta.pyti_stochrsi import PytiStochrsi
from ..ta.pyti_triangular_moving_average import PytiTriangularMovingAverage
from ..ta.pyti_triple_exponential_moving_average import PytiTripleExponentialMovingAverage
from ..ta.pyti_true_range import PytiTrueRange
# TODO: Special case with multiple periods
# from ..ta.pyti_ultimate_oscillator import PytiUtlimateOscillator
from ..ta.pyti_vertical_horizontal_filter import PytiVerticalHorizontalFilter
from ..ta.pyti_volatility import PytiVolatility
from ..ta.pyti_volume_adjusted_moving_average import PytiVolumeAdjustedMovingAverage
from ..ta.pyti_volume_index import PytiVolumeIndex
# TODO: Special case with multiple periods
# from ..ta.pyti_volume_oscillator import PytiVolumeOscillator
from ..ta.pyti_weighted_moving_average import PytiWeightMovingAverage
from ..ta.pyti_williams_percent_r import PytiWilliamsPercentR
# from ..ta.talib_hilbert_transform import TalibHilbertTransform
from ..ta.talib_kaufman_adaptive_moving_average import TalibKaufmanAdaptiveMovingAverage
from ..ta.talib_mesa_adaptive_moving_average import TalibMesaAdaptiveMovingAverage
# TODO: Special case with multiple periods
# from ..ta.talib_moving_average_variable_period import TalibMovingAverageVariablePeriod
from ..ta.talib_midpoint import TalibMidpoint
from ..ta.talib_midprice import TalibMidprice
from ..ta.talib_sar import TalibSar
from ..ta.talib_sar_ext import TalibSarExt
# TODO: Special case with multiple periods
# from ..ta.talib_absolute_price_oscillator import TalibAbsolutePriceOscillator
from ..signals.base_signal_generator import BaseSignalGenerator


class TestSignal(BaseSignalGenerator):
    def __init__(self, market, interval, params, strategy):
        super().__init__(market, interval, strategy)
        self.volume_change = VolumeChangeMonitor(market, interval)
        pyti_params = {
            'market': market,
            'interval': interval,
            'periods': params['period'],
            'params': params
        }
        self.aroon_up = PytiAroon(
            market,
            interval,
            params['period'],
            {
                'aroon_direction': 'up',
                'period': params['period']
            }
        )
        self.aroon_down = PytiAroon(
            market,
            interval,
            params['period'],
            {
                'aroon_direction': 'down',
                'period': params['period']
            }
        )
        self.atr = PytiAverageTrueRange(**pyti_params)
        self.atrp = PytiAverageTrueRangePercent(**pyti_params)
        self.rsi = PytiRsi(**pyti_params)
        self.ad = PytiAccumulationDistribution(market, interval, None, None)
        self.bb = PytiBollingerBands(**pyti_params)
        # self.chaikin = PytiChaikinMoneyFlow(**pyti_params)
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
        self.mae = PytiMovingAverageEnvelope(**pyti_params)
        self.obv = PytiOnBalanceVolume(**pyti_params)
        self.pc = PytiPriceChannels(**pyti_params)
        self.roc = PytiRateOfChange(**pyti_params)
        self.sma = PytiSimpleMovingAverage(**pyti_params)
        self.smma = PytiSmoothedMovingAverage(**pyti_params)
        self.sd = PytiStandardDeviation(**pyti_params)
        self.sv = PytiStandardVariance(**pyti_params)
        self.stoch = PytiStochastic(**pyti_params)
        #  TODO: All nans?
        self.stochrsi = PytiStochrsi(**pyti_params)
        #  TODO: All nans?
        self.tma = PytiTriangularMovingAverage(**pyti_params)
        #  TODO: All nans?
        self.tema = PytiTripleExponentialMovingAverage(**pyti_params)
        self.true_range = PytiTrueRange(**pyti_params)
        self.vhf = PytiVerticalHorizontalFilter(**pyti_params)
        self.volatility = PytiVolatility(**pyti_params)
        self.vama = PytiVolumeAdjustedMovingAverage(**pyti_params)
        self.vi = PytiVolumeIndex(**pyti_params)
        self.wma = PytiWeightMovingAverage(**pyti_params)
        self.wpr = PytiWilliamsPercentR(**pyti_params)
        talib_params = {
            'market': market,
            'interval': interval,
            'periods': params['period'],
            'params': params
        }
        # TODO: Float division by zero
        # self.ht = TalibHilbertTransform(**talib_params)
        # TODO: All nans
        self.kama = TalibKaufmanAdaptiveMovingAverage(**talib_params)
        # TODO: All nans
        # self.mama = TalibMesaAdaptiveMovingAverage(**talib_params)
        # TODO: Throws halting lambda errors randomly but works
        # self.mid = TalibMidpoint(**talib_params)
        self.midprice = TalibMidprice(**talib_params)
        self.sar = TalibSar(**talib_params)
        self.sarext = TalibSarExt(**talib_params)

    def check_condition(self, new_candle):
        self.strategy.add_message("TestSignal")
        print('volume_change', self.volume_change.value)
        print('rsi', self.rsi.value)
        print('atr', self.atr.value)
        print('atrp', self.atrp.value)
        print('ad', self.ad.value)
        print('aroon_up', self.aroon_up.value)
        print('aroon_down', self.aroon_down.value)
        print('bb', self.bb.value)
        # print('chaikin', self.chaikin.value)
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
        print('obv', self.obv.value)
        print('pc', self.pc.value)
        print('roc', self.roc.value)
        print('sma', self.sma.value)
        print('smma', self.smma.value)
        print('sd', self.sd.value)
        print('sv', self.sv.value)
        print('stoch', self.stoch.value)
        print('stochrsi', self.stochrsi.value)
        print('tma', self.tma.value)
        print('tema', self.tema.value)
        print('true_range', self.true_range.value)
        print('vhf', self.vhf.value)
        print('volatility', self.volatility.value)
        print('vama', self.vama.value)
        print('vi', self.vi.value)
        print('wma', self.wma.value)
        print('wpr', self.wpr.value)
        # print('ht', self.ht.value)
        print('kama', self.kama.value)
        # print('mama', self.mama.value)
        # print('mid', self.mid.value)
        print('midprice', self.midprice.value)
        print('sar', self.sar.value)
        print('sarext', self.sarext.value)

        self.strategy.add_message({
            'timestamp': new_candle[0],
            'open': new_candle[1],
            'high': new_candle[2],
            'low': new_candle[3],
            'close': new_candle[4],
            'volume': new_candle[5],
            # 'positions': self.strategy.get_open_position_count(),
            # 'quote_balance': self.market.get_wallet_balance(),
            # 'base_balance': self.market.base_balance,
            # 'exit_balance': self.market.get_wallet_balance()
            #         + (self.market.base_balance *
            #         ((new_candle[2] + new_candle[3])/ 2)),
            'volume_change': self.volume_change.value,
            'rsi': self.rsi.value,
            'atr': self.atr.value,
            'atrp': self.atrp.value,
            'ad': self.ad.value,
            'aroon_up': self.aroon_up.value,
            'aroon_down': self.aroon_down.value,
            'bb': self.bb.value,
            # 'chaikin': self.chaikin.value,
            'chande': self.chande.value,
            'cci': self.cci.value,
            'dpo': self.dpo.value,
            'directional': self.directional.value,
            'dema': self.dema.value if math.isnan(self.dema.value) is False else None,
            # 'dss': self.dss.value,
            'ema': self.ema.value,
            'hma': self.hma.value if math.isnan(self.hma.value) is False else None,
            'lwma': self.lwma.value,
            'momentum': self.momentum.value,
            'mf': self.mf.value,
            'mfi': self.mfi.value if math.isnan(self.mfi.value) is False else None,
            'mae': self.mae.value,
            'obv': self.obv.value,
            'pc': self.pc.value,
            'roc': self.roc.value,
            'sma': self.sma.value,
            'smma': self.smma.value,
            'sd': self.sd.value,
            'sv': self.sv.value,
            'stoch': self.stoch.value,
            'stochrsi': self.stochrsi.value if math.isnan(self.stochrsi.value) is False else None,
            'tma': self.tma.value if math.isnan(self.tma.value) is False else None,
            'tema': self.tema.value if math.isnan(self.tema.value) is False else None,
            'true_range': self.true_range.value,
            'vhf': self.vhf.value,
            'volatility': self.volatility.value,
            'vama': self.vama.value,
            'vi': self.vi.value,
            'wma': self.wma.value,
            'wpr': self.wpr.value,
            # 'ht': self.ht.value,
            'kama': self.kama.value if math.isnan(self.kama.value) is False else None,
            # 'mama': self.mama.value,
            # 'mid': self.mid.value,
            'midprice': self.midprice.value,
            'sar': self.sar.value,
            'sarext': self.sarext.value,
        }, 'db')

        return False
