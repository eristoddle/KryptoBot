from .base_strategy import BaseStrategy, logger
from ...db.utils import generate_uuid
from ...db.models import Backtest, Result, Portfolio, Strategy
import simplejson as json

class PortfolioBase(BaseStrategy):

    def __init__(self, default, limits, portfolio, portfolio_id=None, strategy_id=None):
        super().__init__(default, limits, portfolio_id, strategy_id)
        self.name = portfolio['name']
        self.start_date = None
        self.end_date = None
        self.run_key = generate_uuid()
        self.candle_limit = 1000
        self.candle_set = None
        self.backtest = False
        if 'backtest' in default and default['backtest'] is True:
            self.backtest = True
        if self.is_simulated:
            self.model = Backtest
        else:
            self.model = Result
        if 'start' in default:
            self.start_date = default['start']
        if 'end' in default:
            self.end_date = default['end']

    def __del__(self):
        self._session.close()

    def add_session(self, session):
        self.session = session
        self._session = session()
        self.market.add_session(session)
        self.init_data()
        self.check_if_restarted()

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

    def check_if_restarted(self):
        # TODO: If not simulated sync results and positions
        pass

    def set_candle_limit(self):
        pass

    def run_backtest(self):
        if self.start_date is None:
            print('backtest needs parameters')
            return None
        if self.end_date is None:
            self.set_candle_limit()
            self.run_simulation()
        else:
            self.candle_set = self.market.get_candle_date_range(
                self.inteval,
                self.start_date,
                self.end_date
            )
            self.run_simulation()

    def __run_simulation(self, candle_set=None):
        """Start a simulation on historical candles (runs update method on historical candles)"""
        def run_simulation(candle_set):
            self.add_message("Simulating strategy for market " + self.market.exchange.id + " " + self.market.analysis_pair)
            if self.candle_set is not None:
                candle_set = self.candle_set
            if candle_set is None:
                candle_set = self.market.get_historical_candles(self.interval, self.candle_limit)
            self.simulating = True
            for entry in candle_set:
                self.__update(candle=entry)
            self.simulating = False
        self.__jobs.put(lambda: run_simulation(candle_set))

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
