from .generic_indicator import GenericIndicator
from talib import SAREXT as indicator
'''
SAREXT(...)
    SAREXT(high, low[, startvalue=?, offsetonreverse=?, accelerationinitlong=?, accelerationlong=?, accelerationmaxlong=?, accelerationinitshort=?, accelerationshort=?, accelerationmaxshort=?])

    Parabolic SAR - Extended (Overlap Studies)

    Inputs:
        prices: ['high', 'low']
    Parameters:
        startvalue: 0
        offsetonreverse: 0
        accelerationinitlong: 0.02
        accelerationlong: 0.02
        accelerationmaxlong: 0.2
        accelerationinitshort: 0.02
        accelerationshort: 0.02
        accelerationmaxshort: 0.2
    Outputs:
        real
'''


class TalibSarExt(GenericIndicator):

    def __init__(self, market, interval, periods, params):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = indicator(
                self.talib_data(self.get_high()),
                self.talib_data(self.get_low())
            )[-1]
