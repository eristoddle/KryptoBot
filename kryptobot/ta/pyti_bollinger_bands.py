from .generic_indicator import GenericIndicator
from pyti import bollinger_bands


# params: period, std, upper_bb_std, lower_bb_std
# https://github.com/kylejusticemagnuson/pyti/blob/master/pyti/bollinger_bands.py
class PytiBollingerBands(GenericIndicator):

    def __init__(self, market, interval, periods, params=None):
        super().__init__(market, interval, periods, None, None, params)
        self.value = {}

    def get_analysis(self, data, bollinger_function):
        if bollinger_function == 'upper':
            return bollinger_bands.upper_bollinger_band(
                data,
                self.params['period']
                )
        if bollinger_function == 'middle':
            return bollinger_bands.middle_bollinger_band(
                data,
                self.params['period']
                )
        if bollinger_function == 'lower':
            return bollinger_bands.lower_bollinger_band(
                data,
                self.params['period']
                )
        if bollinger_function == 'bandwidth':
            return bollinger_bands.bandwidth(
                data,
                self.params['period']
                )
        if bollinger_function == 'range':
            return bollinger_bands.bb_range(
                data,
                self.params['period']
                )
        if bollinger_function == 'percent_bandwidth':
            return bollinger_bands.percent_bandwidth(
                data,
                self.params['period']
                )
        if bollinger_function == 'percent_b':
            return bollinger_bands.percent_b(
                data,
                self.params['period']
                )

    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            data = self.get_open()
            self.value['bb_upper'] = self.get_analysis(data, 'upper')[-1]
            self.value['bb_middle'] = self.get_analysis(data, 'middle')[-1]
            self.value['bb_lower'] = self.get_analysis(data, 'lower')[-1]
            self.value['bb_bandwidth'] = self.get_analysis(data, 'bandwidth')[-1]
            self.value['bb_range'] = self.get_analysis(data, 'range')[-1]
            self.value['bb_percent_bandwidth'] = self.get_analysis(data, 'percent_bandwidth')[-1]
            self.value['bb_percent_b'] = self.get_analysis(data, 'percent_b')[-1]
