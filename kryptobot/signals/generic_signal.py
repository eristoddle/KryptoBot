from ..signals.base_signal_generator import BaseSignalGenerator
import importlib
from talib import abstract
import numpy as np
import pandas as pd


class GenericSignal(BaseSignalGenerator):

    # TODO: Make indicators a list of dicts: lib, indicator, params
    def __init__(self, market, interval, lib, indicator, params, strategy):
        super().__init__(market, interval, strategy)
        self.indicator_lib = lib
        if lib == 'pyti':
            self.indicator_name = indicator
            self.indicator = self.dynamic_import(
                'pyti.' + indicator,
                indicator
            )
            self.data_key = 'data'
            print(self.indicator)
        elif lib == 'talib':
            self.indicator = abstract.Function(indicator)
            self.data_key = 'real'
        self.params = params

    def dynamic_import(self, abs_module_path, class_name):
        module_object = importlib.import_module(abs_module_path)
        target_class = getattr(module_object, class_name)
        return target_class

    def get_analysis(self, data):
        # self.params[self.data_key] = data
        return self.indicator(data, **self.params)

    # Inherit and then override this
    def check_condition(self, new_candle):
        # data = np.random.random(100)
        data = {
            'open': np.random.random(100),
            'high': np.random.random(100),
            'low': np.random.random(100),
            'close': np.random.random(100),
            'volume': np.random.random(100)
        }
        self.analysis = self.get_analysis(data)
        print(self.analysis)
        self.strategy.add_message({
            'timestamp': new_candle[0],
            'open': new_candle[1],
            'high': new_candle[2],
            'low': new_candle[3],
            'close': new_candle[4],
            'volume': new_candle[5],
            'positions': self.strategy.get_open_position_count(),
            'quote_balance': self.market.get_wallet_balance(),
            'base_balance': self.market.base_balance,
            'exit_balance': self.market.get_wallet_balance()
                + (self.market.base_balance * ((new_candle[2] + new_candle[3])/ 2))
        }, 'db')

        return False
