from .generic_indicator import GenericIndicator
from pyti.smoothed_moving_average import smoothed_moving_average as indicator


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/price_oscillator.py
class PytiSmoothedMovingAverage(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = indicator(self.get_close(), self.params['period'])[-1]
