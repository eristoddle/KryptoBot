import pandas as pd
# from catalyst.data.bundles.core import register_bundle
from catalyst.data.bundles.base_pricing import BaseCryptoPricingBundle
from catalyst.utils.memoize import lazyval


class BittrexBundle(BaseCryptoPricingBundle):
    @lazyval
    def name(self):
        return 'bittrex'

    @lazyval
    def exchange(self):
        return 'BITT'

    @lazyval
    def frequencies(self):
        return set((
            'daily',
            'minute',
        ))

    @lazyval
    def wait_time(self):
        return pd.Timedelta(milliseconds=170)

    def fetch_raw_metadata_frame(self, api_key, page_number):
        if page_number > 1:
            return pd.DataFrame([])

        raw = pd.read_json(
            self._format_metadata_url(
              api_key,
              page_number,
            ),
            orient='index',
        )

        raw = raw.sort_index().reset_index()
        raw.rename(
            columns={'index': 'symbol'},
            inplace=True,
        )

        raw = raw[raw['isFrozen'] == 0]
        return raw

    def post_process_symbol_metadata(self, asset_id, sym_md, sym_data):
        start_date = sym_data.index[0]
        end_date = sym_data.index[-1]
        ac_date = end_date + pd.Timedelta(days=1)
        min_trade_size = 0.00000001

        return (
            sym_md.symbol,
            start_date,
            end_date,
            ac_date,
            min_trade_size,
        )

    def fetch_raw_symbol_frame(self,
                               api_key,
                               symbol,
                               calendar,
                               start_date,
                               end_date,
                               frequency):

        # TODO: replace this with direct exchange call
        # The end date and frequency should be used to
        # calculate the number of bars
        if(frequency == 'minute'):
            pc = PoloniexCurator()
            raw = pc.onemin_to_dataframe(symbol, start_date, end_date)

        else:
            raw = pd.read_json(
                self._format_data_url(
                    api_key,
                    symbol,
                    start_date,
                    end_date,
                    frequency,
                ),
                orient='records',
            )
            raw.set_index('date', inplace=True)

        # BcolzDailyBarReader introduces a 1/1000 factor in the way
        # pricing is stored on disk, which we compensate here to get
        # the right pricing amounts
        # ref: data/us_equity_pricing.py
        scale = 1
        raw.loc[:, 'open'] /= scale
        raw.loc[:, 'high'] /= scale
        raw.loc[:, 'low'] /= scale
        raw.loc[:, 'close'] /= scale
        raw.loc[:, 'volume'] *= scale

        return raw

    '''
    HELPER METHODS
    '''

    def _format_metadata_url(self, api_key, page_number):
        query_params = [
            ('command', 'returnTicker'),
        ]

        return self._format_polo_query(query_params)

    def _format_data_url(self,
                         api_key,
                         symbol,
                         start_date,
                         end_date,
                         data_frequency):
        period_map = {
            'daily': 86400,
        }

        try:
            period = period_map[data_frequency]
        except KeyError:
            return None

        query_params = [
            ('command', 'returnChartData'),
            ('currencyPair', symbol),
            ('start', start_date.value / 10**9),
            ('end', end_date.value / 10**9),
            ('period', period),
        ]

        return self._format_polo_query(query_params)

    def _format_polo_query(self, query_params):
        # TODO: got against the exchange object
        return 'https://poloniex.com/public?{query}'.format(
            query=urlencode(query_params),
        )
