from .generic_indicator import GenericIndicator
from pyti.moving_average_envelope import moving_average_envelope as indicator


# params: period env_percentage
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/moving_average_envelope.py
class PytiMovingAverageEnvelope(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)
        self.value = {}

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value['center'] = indicator.center_band(
                self.get_close(),
                self.params['period']
            )[-1]
            self.value['center'] = indicator.upper_band(
                self.get_close(),
                self.params['period'],
                self.params['env_percentage']
            )[-1]
            self.value['lower'] = indicator.upper_band(
                self.get_close(),
                self.params['period'],
                self.params['env_percentage']
            )[-1]
