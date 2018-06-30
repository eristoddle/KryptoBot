from .generic_indicator import GenericIndicator
from pyti import price_channels as indicator


# params: period upper_percent lower_percent
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/price_channels.py
class PytiPriceChannels(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)
        self.value = {}

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value['price_channel_upper'] = indicator.upper_price_channel(
                self.get_close(),
                self.params['period'],
                self.params['upper_percent'],
            )[-1]
            self.value['price_channel_lower'] = indicator.lower_price_channel(
                self.get_close(),
                self.params['period'],
                self.params['lower_percent'],
            )[-1]
