from .generic_indicator import GenericIndicator
from talib import MAVP as indicator

'''
MAVP(...)
    MAVP(real, periods[, minperiod=?, maxperiod=?, matype=?])

    Moving average with variable period (Overlap Studies)

    Inputs:
        real: (any ndarray)
        periods: (any ndarray)
    Parameters:
        minperiod: 2
        maxperiod: 30
        matype: 0 (Simple Moving Average)
    Outputs:
        real
'''
class TalibMovingAverageVariablePeriod(GenericIndicator):

    def __init__(self, market, interval, periods, params):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = indicator(
                self.talib_data(self.get_close())
            )[-1]
