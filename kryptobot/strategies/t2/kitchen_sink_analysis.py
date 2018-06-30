from .portfolio_base import PortfolioBase
from ...signals.test_signal import TestSignal


class KitchenSinkAnalysis(PortfolioBase):

    def __init__(self, default, limits, custom, portfolio, portfolio_id=None, strategy_id=None):
        super().__init__(default, limits, portfolio, portfolio_id, strategy_id)
        self.buy_signal = TestSignal(
            self.market,
            self.interval,
            custom,
            self
        )

    def on_data(self, candle):
        self.buy_signal.check_condition(candle)
