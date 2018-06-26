from ..signals.base_signal_generator import BaseSignalGenerator
import importlib
from talib import abstract


class GenericSignal(BaseSignalGenerator):

    # TODO: Make indicators a list of dicts: lib, indicator, params
    def __init__(self, market, interval, lib, indicator, params, strategy):
        super().__init__(market, interval, strategy)
        self.indicator_lib = lib
        if lib == 'pyti':
            self.indicator_name = indicator
            self.indicator = self.dynamic_import(
                lib + '.' + indicator,
                indicator
            )
            print(self.indicator)
        elif lib == 'talib':
            self.indicator = abstract.Function(indicator)
        self.params = params

    def dynamic_import(self, abs_module_path, class_name):
        module_object = importlib.import_module(abs_module_path)
        target_class = getattr(module_object, class_name)
        return target_class

    # Inherit and then override this
    def check_condition(self, new_candle):
        self.params['data'] = [6, 7, 3, 6, 3, 9, 5]
        self.analysis = self.indicator(**self.params)
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
