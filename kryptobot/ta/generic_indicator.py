import importlib
from talib import abstract
from .base_indicator import BaseIndicator


class GenericIndicator(BaseIndicator):

    def __init__(self, market, interval, periods, lib, indicator, params=None):
        super().__init__(market, interval, periods)
        self.indicator_lib = lib
        if lib == 'pyti':
            self.indicator_name = indicator
            self.indicator = self.dynamic_import(
                'pyti.' + indicator,
                indicator
            )
            print(self.indicator)
        elif lib == 'talib':
            self.indicator = abstract.Function(indicator)
        self.params = params
        self.value = None

    def dynamic_import(self, abs_module_path, class_name):
        module_object = importlib.import_module(abs_module_path)
        target_class = getattr(module_object, class_name)
        return target_class

    def get_datawindow(self):
        dataset = self.market.candles[self.interval]
        if len(dataset) >= self.periods:
            self.data_window = dataset[-self.periods:]
            return self.data_window
        return None

    def get_timestamp(self):
        return list(c[0] for c in self.data_window)

    def get_open(self):
        return list(c[1] for c in self.data_window)

    def get_high(self):
        return list(c[2] for c in self.data_window)

    def get_low(self):
        return list(c[3] for c in self.data_window)

    def get_close(self):
        return list(c[4] for c in self.data_window)

    def get_volume(self):
        return list(c[5] for c in self.data_window)

    # Inherit from and override this
    def get_analysis(self, data):
        return self.indicator(data, **self.params)

    # Override this if you just need one column of the candles
    def next_calculation(self, candle):
        if self.get_datawindow() is not None:
            self.value = self.get_analysis(self.data_window)
