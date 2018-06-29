from .generic_indicator import GenericIndicator
from pyti.aroon import aroon_up, aroon_down


# params: direction, period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/aroon.py
class PytiAroon(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def get_analysis(self, data):
        if self.params['aroon_direction'] == 'up':
            return aroon_up(data, self.params['period'])[-1]
        return aroon_down(data, self.params['period'])[-1]

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = self.get_analysis(self.get_close())
