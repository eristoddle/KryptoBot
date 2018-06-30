from .generic_indicator import GenericIndicator
from pyti import stochastic as indicator


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/double_smoothed_stochastic.py
class PytiStochastic(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)
        self.value = {}

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value['percent_k'] = indicator.percent_k(
                self.get_close(),
                self.params['period']
            )[-1]
        if self.get_datawindow() is not None:
            self.value['percent_d'] = indicator.percent_k(
                self.get_close(),
                self.params['period']
            )[-1]
