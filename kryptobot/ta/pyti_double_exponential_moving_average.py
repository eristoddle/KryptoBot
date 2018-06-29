from .generic_indicator import GenericIndicator
from pyti.double_exponential_moving_average import double_exponential_moving_average as dema


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/relative_strength_index.py
class PytiDema(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = dema(self.get_close(), self.params['period'])[-1]
