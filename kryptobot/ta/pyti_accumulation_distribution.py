from .generic_indicator import GenericIndicator
from pyti.accumulation_distribution import accumulation_distribution as ad


# params: close_data, high_data, low_data, volume
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/accumulation_distribution.py
class PytiAccumulationDistribution(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, 2, None, None, params)

    def get_analysis(self, close, high, low, volume):
        return ad(close, high, low, volume)[-1]

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = self.get_analysis(
                self.get_close(),
                self.get_high(),
                self.get_low(),
                self.get_volume()
            )
