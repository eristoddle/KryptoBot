from .generic_indicator import GenericIndicator
from pyti.money_flow_index import money_flow_index as indicator


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/money_flow_index.py
class PytiMoneyFlowIndex(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = indicator(
                self.get_close(),
                self.get_high(),
                self.get_low(),
                self.get_volume(),
                self.params['period']
            )[-1]
