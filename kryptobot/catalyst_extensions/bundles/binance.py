import pandas as pd
import ccxt
import json
from .base_pricing import BaseCryptoPricingBundle
from catalyst.utils.memoize import lazyval


class BinanceBundle(BaseCryptoPricingBundle):
    @lazyval
    def name(self):
        return 'binance'

    @lazyval
    def exchange(self):
        return 'BINA'

    @lazyval
    def frequencies(self):
        return set((
            'daily',
            'minute',
        ))

    @lazyval
    def tar_url(self):
        return (
            'http://google.com'
            'binance/binance-bundle.tar.gz'
        )

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

        exchange = getattr(ccxt, self.name())()
        timeframe = '1m' if frequency == 'minute' else '1d'
        ccxt_symbol = symbol.replace('_', '/').upper()
        ohlcv = json.dumps(exchange.fetch_ohlcv(ccxt_symbol, timeframe))
        # print(ohlcv)
        raw = pd.read_json(ohlcv)
        if frequency == 'daily':
            raw.set_index('date', inplace=True)
        scale = 1
        raw.loc[:, 'open'] /= scale
        raw.loc[:, 'high'] /= scale
        raw.loc[:, 'low'] /= scale
        raw.loc[:, 'close'] /= scale
        raw.loc[:, 'volume'] *= scale

        return raw
