from .generic_indicator import GenericIndicator
from pyti.directional_indicators import positive_directional_movement, negative_directional_movement, positive_directional_index, negative_directional_index, average_directional_index


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/detrended_price_oscillator.py
class PytiDirectionalIndicators(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)
        self.value = {}

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            high = self.get_high()
            low = self.get_low()
            close = self.get_low()
            period = self.params['period']
            self.value['positive_directional_movement'] = positive_directional_movement(high, low)[-1]
            self.value['negative_directional_movement'] = negative_directional_movement(high, low)[-1]
            self.value['positive_directional_index'] = positive_directional_index(close, high, low, period)[-1]
            self.value['negative_directional_index'] = negative_directional_index(close, high, low, period)[-1]
            self.value['average_directional_index'] = average_directional_index(close, high, low, period)[-1]
