import ccxt
from pymarketcap import Pymarketcap
from datetime import datetime, timedelta
from .base_harvester import BaseHarvester


class CmcNewCoinHarvester(BaseHarvester):

    cmc = Pymarketcap()
    days_to_hold = 10
    per_coin_investment = 100
    stake = 0
    portfolio = {}
    cryptopia = ccxt.cryptopia()
    cryptopia_markets = cryptopia.load_markets()
    cryptopia_pairs = [k for k, v in cryptopia_markets.items()]

    def __init__(self, interval, is_simulated):
        super().__init__(interval, is_simulated)

    def get_cmc_targets(max_days):
    global cryptopia_pairs
    recent = cmc.recently()
    targets = []
    for r in recent:
        if r['added'] == 'Today':
            days_old = 0
        else:
            days_old = int(r['added'].replace(' days ago', ''))
        if days_old > max_days:

            targets.append({
                'symbol': r['symbol'],
                'days_old': days_old,
                'volume_24h': r['volume_24h'],
                'market_cap': r['market_cap'],
            })

    target_pairs = [i['symbol'] + '/BTC' for i in targets]
    cryptopia_targets = [s for s in target_pairs if any(xs in s for xs in cryptopia_pairs)]
#     print('cryptopia_targets', cryptopia_targets)
    return targets

    def buy_and_sell(symbol, days_ago):
        global stake, portfolio
        start = datetime.today() - timedelta(days=days_ago+2)
        end = datetime.today() - timedelta(days=(days_ago-days_to_hold))
        print('buying: ' + symbol, start, end)
        try:
            ohlc = cmc.historical(name=symbol, start=start, end=end)
            prices = ohlc['history']
            latest = prices[0]['open']
            oldest = prices[len(prices)-1]['open']
            print('BUY:', oldest, 'SELL:', latest)
            bought = per_coin_investment/oldest
            portfolio.update({symbol: bought})
            stake = stake - per_coin_investment
            sold = bought * latest
            stake = stake + sold
        except ValueError:
            print('ValueError, skipping: ' + symbol)
        except IndexError:
            print('IndexError, skipping: ' + symbol)


# targets = get_cmc_targets(days_to_hold)
# stake = per_coin_investment * len(targets)
# print('Starting Capital: $ ' + str(stake) + '.00')
# for t in targets:
#     buy_and_sell(t['symbol'], t['days_old'])
#
# print(portfolio)
# print('Ending Capital: $ ' + str(stake) + '.00')
