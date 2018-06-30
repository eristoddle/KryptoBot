from .generic_indicator import GenericIndicator
from pyti import volume_index as indicator


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/double_smoothed_stochastic.py
class PytiVolumeIndex(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)
        self.value = {}

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value['positive_volume_index'] = indicator.positive_volume_index(
                self.get_close(),
                self.get_volume()
            )[-1]
            self.value['negative_volume_index'] = indicator.negative_volume_index(
                self.get_close(),
                self.get_volume()
            )[-1]
