from .generic_indicator import GenericIndicator


class TalibMacd(GenericIndicator):

    def __init__(self, market, interval, periods, params):
        super().__init__(
            market,
            interval,
            periods,
            'talib',
            'macd',
            params
        )
        self.value = {}

    def get_analysis(self, data):
        self.value['macd'],
        self.value['macdSignal'],
        self.value['macdHist'] = self.indicator(
            data,
            fastperiod=self.params['fast'],
            slowperiod=self.params['slow'],
            signalperiod=self.params['signal']
        )
