from .generic_indicator import GenericIndicator


# params: period
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/average_true_range.py
class PytiAverageTrueRange(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(
            market,
            interval,
            periods,
            'pyti',
            'average_true_range',
            params
        )

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = self.get_analysis(self.get_close())
