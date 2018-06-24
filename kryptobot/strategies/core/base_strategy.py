from catalyst.api import symbol
from catalyst.exchange.utils.bundle_utils import EXCHANGE_NAMES
import pandas as pd


class BaseStrategy():

    def __init__(self, default, custom):
        self.default = default
        self.custom = custom
        # self.asset = symbol(self.default['pair'])
        self.default['quote_currency'] = self.default['pair'].split('_')[1]
        if 'start' not in self.default:
            self.default['start'] = None
        else:
            self.default['start'] = pd.to_datetime(self.default['start'], utc=True)
        if 'end' not in self.default:
            self.default['end'] = None
        else:
            self.default['end'] = pd.to_datetime(self.default['start'], utc=True)
        # if 'output' not in self.default:
        #     self.default['output'] = '/root/.catalyst_pickles/' + str(strategy_id) + '.pickle'

    def get_ingest_params(self):
        if self.default['exchange_name'] in EXCHANGE_NAMES:
            csv = None
        else:
            csv = 'create'
        return {
            'data_frequency': self.defaul['data_frequency'],
            'include_symbols': self.default['pair'],
            'exchange_name': self.default['exchange_name'],
            'start': self.default['start'],
            'end': self.default['end'],
            'csv': csv
        }

    def get_run_params(self):
        return {
            'capital_base': self.default['capital_base'],
            'data_frequency': self.default['data_frequency'],
            'exchange_name': self.default['exchange_name'],
            'quote_currency': self.default['quote_currency'],
            'initialize': self.get_initialize(),
            'handle_data': self.get_handle_data(),
            'start': self.default['start'],
            'end': self.default['end']
        }
        #     initialize=None,
        #     handle_data=None,
        #     before_trading_start=None,
        #     analyze=None,
        #     algofile=algofile,
        #     algotext=algotext,
        #     defines=define,
        #     data_frequency=None,
        #     capital_base=capital_base,
        #     data=None,
        #     bundle=None,
        #     bundle_timestamp=None,
        #     start=start,
        #     end=end,
        #     output=output,
        #     print_algo=print_algo,
        #     local_namespace=local_namespace,
        #     environ=os.environ,
        #     live=True,
        #     exchange=exchange_name,
        #     algo_namespace=algo_namespace,
        #     quote_currency=quote_currency,
        #     live_graph=live_graph,
        #     analyze_live=None,
        #     simulate_orders=simulate_orders,
        #     auth_aliases=auth_aliases,
        #     stats_output=None,

    # This can be overridden in child class to be dynamic
    def get_order_quantity(self):
        if 'order_quantity' in self.default:
            return self.default['order_quantity']
        return None

    # This can be overridden in child class to be dynamic
    def get_position_limit(self):
        if 'position_limit' in self.default:
            return self.default['position_limit']
        return None

    def get_stop_signals(self):
        pass

    def get_initialize(self):
        raise NotImplementedError()

    def get_handle_data(self):
        raise NotImplementedError()

    def get_analyze(self):
        raise NotImplementedError()
