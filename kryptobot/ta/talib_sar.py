from .generic_indicator import GenericIndicator
from talib import SAR as indicator
'''
SAR(...)
    SAR(high, low[, acceleration=?, maximum=?])

    Parabolic SAR (Overlap Studies)

    Inputs:
        prices: ['high', 'low']
    Parameters:
        acceleration: 0.02
        maximum: 0.2
    Outputs:
        real
'''


class TalibSar(GenericIndicator):

    def __init__(self, market, interval, periods, params):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = indicator(
                self.talib_data(self.get_high()),
                self.talib_data(self.get_low())
            )[-1]
