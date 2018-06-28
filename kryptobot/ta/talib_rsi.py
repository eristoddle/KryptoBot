from .generic_indicator import GenericIndicator
from talib import RSI


# TODO: Returns nans
# params: rsi_period
class TalibRsi(GenericIndicator):

    def __init__(self, market, interval, periods, params):
        super().__init__(market, interval, periods, None, None, params)

    def get_analysis(self, data):
        return RSI(self.prep_talib_data(data), self.params['rsi_period'])[-1]

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = self.get_analysis(self.get_close())
