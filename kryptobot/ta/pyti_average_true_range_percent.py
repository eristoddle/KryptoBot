from .generic_indicator import GenericIndicator
from pyti.average_true_range_percent import average_true_range_percent as atrp


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/average_true_range_percent.py
class PytiAverageTrueRangePercent(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def get_analysis(self, data):
        return atrp(data, self.params['period'])[-1]

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = self.get_analysis(self.get_close())
