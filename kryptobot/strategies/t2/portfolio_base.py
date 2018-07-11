from threading import Thread
from queue import Queue
# import simplejson as json
from datetime import datetime
# import re
from .base_strategy import BaseStrategy, logger
from ...markets import market_watcher, market_simulator, position
from ...db.utils import generate_uuid
from ...db.models import Backtest, Result, Portfolio, Strategy


class PortfolioBase(BaseStrategy):

    def __init__(self, default, limits, portfolio, portfolio_id=None, strategy_id=None):
        super().__init__(default, limits, portfolio_id, strategy_id)
        self.__thread = Thread(target=self.__run)
        self.__jobs = Queue()
        self.name = portfolio['name']
        self.start_date = None
        self.end_date = None
        self.run_key = generate_uuid()
        self.candle_limit = 1000
        self.candle_set = None
        self.backtest = False
        self.action = 'hold'
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

    def start(self):
        """Start thread and subscribe to candle updates"""
        self.__jobs.put(lambda: market_watcher.subscribe(self.market.exchange.id, self.market.base_currency, self.market.quote_currency, self.interval, self.__update, self.session, self.ticker))
        self.__thread.start()

    def run_simulation(self):
        """Queue simulation when market data has been synced"""
        if self.is_simulated:
            market_watcher.subscribe_historical(self.market.exchange.id, self.market.base_currency,
                                            self.market.quote_currency, self.interval, self.__run_simulation, self.session, self.ticker)

    def check_if_restarted(self):
        # TODO: If not simulated append to results and sync positions
        pass

    def run_backtest(self):
        """Queue simulation when market data has been synced"""
        if self.backtest:
            market_watcher.subscribe_backtest(self.market.exchange.id, self.market.base_currency,
                                            self.market.quote_currency, self.interval, self.__run_backtest, self.session, self.ticker)

    def __run_backtest(self):
        def run_backtest():
            if self.start_date is None:
                print('backtest needs parameters')
                return None
            if self.end_date is None:
                today = datetime.now()
                self.end_date = today.strftime('%Y-%m-%d')
            candle_set = self.market.get_candle_date_range(
                self.interval,
                self.start_date,
                self.end_date
            )
            self.backtesting = True
            for entry in candle_set:
                self.__update(candle=entry)
            self.backtesting = False

        # TODO: This stops before updating data but something has to work
        # It needs to stop itself
        # def stop():
        #     self.stop()

        self.__jobs.put(lambda: run_backtest())
        # self.__jobs.put(lambda: stop())

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

    def __update(self, candle):
        """Run updates on all markets/indicators/signal generators running in strategy"""
        def update(candle):
            self.add_message("Received new candle")
            self.market.update(self.interval, candle)
            self.__update_positions()
            self.on_data(candle)
            self.add_message("Simulation BTC balance: " + str(self.market.get_wallet_balance()))
            self.strategy = self._session.query(Strategy).filter(Strategy.id == self.strategy_id).first()
            if self.strategy.status == 'paused':
                print('strategy received signal to stop. ID:', self.strategy_id)
                self.stop()
            # TODO: These should do what they say they do
            if self.strategy.status == 'exited':
                print('exiting strategy before archiving. ID:', self.strategy_id)
                self.stop()
            if self.strategy.status == 'archived':
                print('setting strategy to archived and stopping. ID:', self.strategy_id)
                self.stop()
        self.__jobs.put(lambda: update(candle))

    def __update_positions(self):
        """Loop through all positions opened by the strategy"""
        sell = False
        if self.action == 'sell':
            sell = True
        for p in self.positions:
            if p.is_open:
                p.update(sell)

    # New execute method to handle both buy and sell signals
    def execute(self, order_quantity, fixed_stoploss_percent, trailing_stoploss_percent, profit_target_percent, action):
        self.action = action
        if action == 'buy':
            """Open long position"""
            if self.is_simulated:
                """Open simulated long position"""
                self.add_message("Going long on " + self.market.analysis_pair)
                self.positions.append(market_simulator.open_long_position_simulation(self.market, order_quantity,
                                                                                     self.market.latest_candle[
                                                                                         self.interval][3],
                                                                                     fixed_stoploss_percent,
                                                                                     trailing_stoploss_percent,
                                                                                     profit_target_percent))
            else:
                """LIVE long position"""
                self.add_message("Going long on " + self.market.analysis_pair)
                self.positions.append(position.open_long_position(self.market, order_quantity,
                                                              self.market.get_best_ask(),
                                                              fixed_stoploss_percent,
                                                              trailing_stoploss_percent,
                                                              profit_target_percent))

    def __run(self):
        """Start the strategy thread waiting for commands"""
        self.add_message("Starting strategy " + str(self.strategy_id))
        self.running = True
        while self.running:
            if not self.__jobs.empty():
                job = self.__jobs.get()
                try:
                    job()
                except Exception as e:
                    print(e)
                    logger.error(job.__name__ + " threw error:\n" + str(e))

    def add_message(self, msg, type='print'):
        if type == 'both' or type == 'print':
            # if isinstance(msg, dict):
            #     str_msg = json.dumps(msg)
            # else:
            #     str_msg = str(msg)
            # print(str("Strategy " + str(self.strategy_id) + ": " + str_msg))
            # logger.info(str_msg)
            pass
        if type == 'both' or type == 'db':
            data = self.model(
                strategy_id=self.strategy_id,
                run_key=self.run_key,
                data=msg
            )
            self._session.add(data)
            self._session.commit()

    # TODO: Do any clean up involved in shutting down
    def stop(self):
        market_watcher.stop_watcher(self.market.exchange.id, self.market.base_currency, self.market.quote_currency, self.interval)
        self.running = False
