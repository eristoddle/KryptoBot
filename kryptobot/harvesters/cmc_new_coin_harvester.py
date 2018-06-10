import ccxt
from pymarketcap import Pymarketcap
from datetime import datetime, timedelta
from .base_harvester import BaseHarvester
from ..portfolio.exchanges import Exchanges


class CmcNewCoinHarvester(BaseHarvester):

    taskname = 'cmc-new-coin-harvester'
    classname = 'CmcNewCoinHarvester'

    def __init__(self, interval, is_simulated, base_currency, portfolio_id, harvester_id, config):
        kwargs = {
            'base_currency': base_currency
        }
        super().__init__(interval, is_simulated, portfolio_id, config, harvester_id, kwargs)
        self.base_currency = base_currency

    def get_data(self):
        targets = self.get_cmc_targets(1)
        target_pairs = [i['symbol'] + '/' + self.base_currency for i in targets]
        apis = Exchanges(self.config['apis'])
        markets = []
        for pr in target_pairs:
            markets.append({'pr': apis.get_pair_markets(pr)})
        return markets

    def get_cmc_targets(self, max_days):
        cmc = Pymarketcap()
        recent = cmc.recently()
        targets = []
        for r in recent:
            if r['added'] == 'Today':
                days_old = 0
            else:
                days_old = int(r['added'].replace(' days ago', ''))
            if days_old < max_days:

                targets.append({
                    'symbol': r['symbol'],
                    'days_old': days_old,
                    'volume_24h': r['volume_24h'],
                    'market_cap': r['market_cap'],
                })
        return targets
