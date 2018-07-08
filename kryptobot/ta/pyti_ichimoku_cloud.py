from .generic_indicator import GenericIndicator
from pyti import ichimoku_cloud as indicator


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/ichimoku_cloud.py
class PytiIchimokuCloud(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            if self.params['indicator'] == 'tenkansen':
                self.value = indicator.tenkansen(self.get_close(), self.periods)[-1]
