from .portfolio_base import PortfolioBase
from ...signals.generic_signal import GenericSignal


class KitchenSinkAnalysis(PortfolioBase):

    def __init__(self, default, limits, custom, portfolio, portfolio_id=None, strategy_id=None):
        super().__init__(default, limits, portfolio, portfolio_id, strategy_id)
        self.buy_signal = GenericSignal(
            self.market,
            self.interval,
            custom['lib'],
            custom['indicator'],
            custom['params'],
            self
        )

    def on_data(self, candle):
        self.buy_signal.check_condition(candle)
