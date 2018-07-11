from .generic_indicator import GenericIndicator
from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd

class PytiMacd(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)
        self.macd = []
        self.value = {}

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            md = macd(
                self.get_close(),
                self.params['short_window'],
                self.periods
            )[-1]
            self.macd.append(md)
            signal = ema(self.macd, self.params['signal_window'])
            self.value = {
                'macd': md,
                'signal': signal[-1],
                'crossover': md - signal[-1]
            }
