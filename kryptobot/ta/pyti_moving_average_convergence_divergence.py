from .generic_indicator import GenericIndicator
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as indicator


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/ichimoku_cloud.py
class PytiMacd(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def get_datawindow(self):
        # import sys
        # sys.exit()
        dataset = self.market.candles[self.interval]
        if self.periods is None:
            print('periods is None in GenericIndicator.get_datawindow')
        if len(dataset) >= self.periods:
            self.data_window = dataset[-self.periods:]
            return self.data_window
        return None

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = indicator(self.get_close(), self.params['period'])[-1]
