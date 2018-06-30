from .generic_indicator import GenericIndicator
from talib import HT_TRENDLINE as indicator


class TalibHilbertTransform(GenericIndicator):

    def __init__(self, market, interval, periods, params):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = indicator(self.get_close())[-1]
