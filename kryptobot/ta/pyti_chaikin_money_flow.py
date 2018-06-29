from .generic_indicator import GenericIndicator
from pyti.chaikin_money_flow import chaikin_money_flow as cmf


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/chaikin_money_flow.py
class PytiChaikinMoneyFlow(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = cmf(
                self.get_close(),
                self.get_high(),
                self.get_low(),
                self.get_volume(),
                self.params['period']
            )[-1]
