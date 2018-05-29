from ..core import Core
import ccxt


class Manager(Core):

    exchanges = {}
    markets_loaded = False

    def __init__(self, config=None):
        super().__init__(config)
        if('apis' in self.config):
            for key, value in self.config['apis'].items():
                self.add_exchange(key)

    def add_exchange(self, name):
        exchange = getattr(ccxt, name)
        key = self.config['apis'][name]['key']
        secret = self.config['apis'][name]['secret']
        self.exchanges.update({name: exchange({'apiKey': key, 'secret': secret})})

    def load_markets(self):
        for name, exchange in self.exchanges.items():
            exchange.load_markets()
        self.markets_loaded = True

    def get_symbols(self):
        if self.markets_loaded is False:
            self.load_markets()
        return [{name: exchange.symbols} for name, exchange in self.exchanges.items()]

    # def get_profit_for_trades(self):
    #     self.profit = self.get_profit_for_pair(self.exchange, self.pair)
    #     print("The total profit for this pair is {} up to this point in the trading session".format(self.profit))
    #     return self.profit
    #
    # def get_average_profit_per_trades(self):
    #     average_profit_per_trade = (self.profit / self.get_number_of_trades(self.exchange, self.pair)) / 2
    #     print("The average profit up to this point in the trading session is {}".format(average_profit_per_trade))
    #     return average_profit_per_trade
    #
    # def get_profit_for_pair(self, exchange, pair):
    #     """Iterates through all trades for given exchange pair over the course of trading. Starts by subtracting the long positions (the buys) and adding the short positions (the sells) to arrive at the difference (profit"""
    #     """The buys are always the even rows and the sells are the odd rows (buy always before sell starting from zero)"""
    #     profit = 0
    #     counter = 0
    #     s = select([database.TradingPositions]).where(and_(database.TradingPositions.c.Exchange == exchange, database.TradingPositions.c.Pair == pair))
    #     result = conn.execute(s)
    #
    #     for row in result:
    #         if counter % 2 == 0:
    #             profit = profit - row[5]
    #             counter += 1
    #         else:
    #             profit = profit + row[5]
    #             counter += 1
    #         return profit
    #
    # def get_number_of_trades(self, exchange, pair):
    #     s = select([func.count()]).where(and_(database.TradingPositions.c.Exchange == exchange, database.TradingPositions.c.Pair == pair)).select_from(database.TradingPositions)
    #     result = conn.execute(s)
    #     return int(result)
    #
    # def get_trades_for_pair_as_df(self, exchange, pair):
    #     """Returns all trades for given exchange pair over the course of trading in a dataframe"""
    #     s = select([database.TradingPositions]).where(and_(database.TradingPositions.c.Exchange == exchange, database.TradingPositions.c.Pair == pair))
    #     result = conn.execute(s)
    #     df = pd.DataFrame(result.fetchall())
    #     df.columns = result.keys()
    #     result.close()
    #     return df
