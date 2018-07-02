from .base_strategy import BaseStrategy, logger
from ...db.utils import generate_uuid
from ...db.models import Backtest, Result, Portfolio, Strategy
import simplejson as json

class PortfolioBase(BaseStrategy):

    def __init__(self, default, limits, portfolio, portfolio_id=None, strategy_id=None):
        super().__init__(default, limits, portfolio_id, strategy_id)
        self.name = portfolio['name']
        self.run_key = generate_uuid()
        if self.is_simulated:
            self.model = Backtest
        else:
            self.model = Result

    def __del__(self):
        self._session.close()

    def add_session(self, session):
        self.session = session
        self._session = session()
        self.market.add_session(session)
        self.init_data()

    def init_data(self):
        if self.portfolio_id is not None:
            self.portfolio = self._session.query(Portfolio).filter(Portfolio.id == self.portfolio_id).first()
        if self.strategy_id is not None:
            self.strategy = self._session.query(Strategy).filter(Strategy.id == self.strategy_id).first()

    def process_limits(self, limits):
        self.capital_base = limits['capital_base']
        self.order_quantity = limits['order_quantity']
        self.position_limit = limits['position_limit']
        self.profit_target_percentage = limits['profit_target_percentage']
        self.fixed_stoploss_percentage = limits['fixed_stoploss_percentage']
        self.trailing_stoploss_percentage = limits['trailing_stoploss_percentage']

    def add_message(self, msg, type='print'):
        if type == 'both' or type == 'print':
            if isinstance(msg, dict):
                str_msg = json.dumps(msg)
            else:
                str_msg = str(msg)
            print(str("Strategy " + str(self.strategy_id) + ": " + str_msg))
            logger.info(str_msg)
        if type == 'both' or type == 'db':
            data = self.model(
                strategy_id=self.strategy_id,
                run_key=self.run_key,
                data=msg
            )
            self._session.add(data)
            self._session.commit()
