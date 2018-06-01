import ccxt


class Exchanges:

    exchanges = {}
    exchange_names = []
    pair_matrix = {}
    markets_loaded = False

    def __init__(self):
        pass

    def add_exchange(self, name):
        exchange = getattr(ccxt, name)
        key = self.config['apis'][name]['key']
        secret = self.config['apis'][name]['secret']
        self.exchanges.update(
            {name: exchange({'apiKey': key, 'secret': secret})}
        )
        self.exchange_names.append(name)

    def load_markets(self):
        for name, exchange in self.exchanges.items():
            exchange.load_markets()
        self.markets_loaded = True

    def get_symbols(self):
        if self.markets_loaded is False:
            self.load_markets()
        return [{name: exchange.symbols} for name, exchange in self.exchanges.items()]

    def get_pair_matrix(self):
        exchange_symbols = self.get_symbols()
        if len(self.pair_matrix) < 1:
            for es in exchange_symbols:
                for name, syms in es.items():
                    for sym in syms:
                        if sym in self.pair_matrix:
                            self.pair_matrix[sym].append(name)
                        else:
                            self.pair_matrix.update({sym: [name]})
        return self.pair_matrix

    def get_pair_markets(self, pair):
        pair_markets = {}
        pair_matrix = self.get_pair_matrix()
        highest_bid = 0
        highest_bid_exchange = None
        lowest_ask = 0
        lowest_ask_exchange = None
        arbitrage_spread = None
        arbitrage_percentage = 0
        if pair in pair_matrix:
            names = pair_matrix[pair]
            for n in names:
                exchange = self.exchanges[n]
                # orderbook = exchange.fetch_order_book(pair)
                # bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
                # ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
                ticker = exchange.fetch_ticker(pair)
                bid = ticker['ask']
                ask = ticker['bid']
                # TODO Fix the None/Float comparison issue
                try:
                    if highest_bid == 0 or bid > highest_bid:
                        highest_bid = bid
                        highest_bid_exchange = n
                    if lowest_ask == 0 or ask > lowest_ask:
                        lowest_ask = ask
                        lowest_ask_exchange = n
                except:
                    pass
                volume = ticker['baseVolume'] if 'baseVolume' in ticker else None
                spread = (ask - bid) if (bid and ask) else None
                pair_markets[n] = {
                    'bid': bid,
                    'ask': ask,
                    'spread': spread,
                    'volume': volume,
                    # 'ticker': ticker
                }
            if highest_bid is not None and lowest_ask is not None:
                arbitrage_spread = highest_bid - lowest_ask
                arbitrage_percentage = (arbitrage_spread / lowest_ask) * 100
            return {
                'markets': pair_markets,
                'arbitrage': {
                    'highest_bid': highest_bid,
                    'highest_bid_exchange': highest_bid_exchange,
                    'lowest_ask': lowest_ask,
                    'lowest_ask_exchange': lowest_ask_exchange,
                    'spread': arbitrage_spread,
                    'percentage': arbitrage_percentage
                }
            }
        return None

    def get_possible_arbitrage(self):
        pair_matrix = self.get_pair_matrix()
        possible = {}
        for sym, names in pair_matrix.items():
            if len(names) > 1:
                possible[sym] = names
        return possible

    def get_arbitrage_prices(self, base_currency, threshold_percentage):
        prices = {}
        possible = self.get_possible_arbitrage()
        for sym, names in possible.items():
            pair = '/' + base_currency
            if pair in sym:
                pair_markets = self.get_pair_markets(sym)
                threshold_met = (pair_markets['arbitrage']['percentage'] > threshold_percentage)
                true_arbitrage = pair_markets['arbitrage']['highest_bid_exchange'] != pair_markets['arbitrage']['lowest_ask_exchange']
                if threshold_met and true_arbitrage:
                    prices[sym] = self.get_pair_markets(sym)
        return prices
