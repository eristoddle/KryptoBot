from .generic_indicator import GenericIndicator
from pyti.chande_momentum_oscillator import chande_momentum_oscillator as cmo


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/relative_strength_index.py
class PytiChandeMomentumOscillator(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = cmo(self.get_close(), self.params['period'])[-1]
