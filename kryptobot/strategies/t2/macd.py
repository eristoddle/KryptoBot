from .portfolio_base import PortfolioBase
from ...signals import pyti_macd_signal


# custom param, default
# 'short_window', 12
# 'long_window', 26
# 'signal_window', 9
class Macd(PortfolioBase):

    def __init__(self, default, limits, custom, portfolio, portfolio_id=None, strategy_id=None):
        super().__init__(default, limits, portfolio, portfolio_id, strategy_id)
        self.signal = pyti_macd_signal.PytiMacdSignal(
            self.market,
            self.interval,
            custom,
            self
        )

    def on_data(self, candle):
        action = self.signal.check_condition(candle)
        if self.get_open_position_count() >= self.position_limit and action == 'buy':
            action = 'hold'
        self.execute(
            self.order_quantity,
            self.fixed_stoploss_percentage,
            self.trailing_stoploss_percentage,
            self.profit_target_percentage,
            action
        )
