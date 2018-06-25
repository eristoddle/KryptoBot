from .base_strategy import BaseStrategy
from ...signals import sma_crossover_signal


class DualSimpleMovingAverage(BaseStrategy):
    """A strategy using the SMA crossover signal generator as a buy signal
    This strategy will trigger the SMA crossover signal on every candle and check for buy conditions
    If the condition returns true, the strategy will open a long position it does not have up to (position_limit) opened
    Each position opened will automatically sell itself off when its price (profit_target_percent*buy price) is met
    """
    def __init__(self, default, limits, custom, portfolio_id=None, strategy_id=None):
    # def __init__(self, interval, exchange, base_currency, quote_currency, is_simulated, fma_periods, sma_periods, sim_balance=0, portfolio_id=None, strategy_id=None):
        super().__init__(default, limits, portfolio_id, strategy_id)
        # super().__init__(interval, exchange, base_currency, quote_currency, is_simulated, sim_balance, portfolio_id, strategy_id)
        self.buy_signal = sma_crossover_signal.SmaCrossoverSignal(
            self.market,
            self.interval,
            custom['long_window'],
            custom['short_window'],
            self
        )

    def on_data(self, candle):
        buy_condition = self.buy_signal.check_condition(candle)
        if self.get_open_position_count() >= self.position_limit:
            pass
        elif buy_condition:
            self.long(self.order_quantity, self.fixed_stoploss_percent, self.trailing_stoploss_percent, self.profit_target_percent)