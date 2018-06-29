from .generic_indicator import GenericIndicator
from pyti.detrended_price_oscillator import detrended_price_oscillator as dpo


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/detrended_price_oscillator.py
class PytiDetrendedPriceOscillator(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = dpo(
                self.get_close(),
                self.params['period']
            )[-1]
