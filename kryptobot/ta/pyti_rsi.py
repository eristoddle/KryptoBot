from .generic_indicator import GenericIndicator
from pyti.relative_strength_index import relative_strength_index as rsi


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/relative_strength_index.py
class PytiRsi(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def get_analysis(self, data):
        return rsi(data, self.params['rsi_period'])[-1]

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = self.get_analysis(self.get_close())
