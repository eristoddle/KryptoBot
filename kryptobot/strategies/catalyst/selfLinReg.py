import numpy as np
import pandas as pd
import talib as ta
from scipy import stats
import math
import matplotlib.pyplot as plt
from catalyst import run_algorithm
from catalyst.exchange.utils.stats_utils import extract_transactions
from catalyst.api import (
    record,
    order,
    order_target_percent,
    symbol,
    get_order
)
from logbook import Logger

log = Logger("LinReg")


def initialize(context):
    log.info('Initializing LinReg Algorithm')
    context.bitfinex = context.exchanges['poloniex']
    context.asset = symbol('ltc_btc', context.bitfinex.name)

    context.swallow_errors = True
    context.errors = []

    context.CANDLE_SIZE = '15T'
    context.threshold = 0.001
    context.length = 16
    context.in_long = False
    context.in_short = False

    pass


def midpoint(p1, p2):
    return (p1 + p2) / 2


def _handle_data(context, data):
    hist = data.history(
        context.asset,
        fields=['open', 'high', 'low', 'close'],
        bar_count=365,
        frequency=context.CANDLE_SIZE
    )
    close = data.current(context.asset, 'close')

    close_prices = np.asarray(hist.close)
    low_prices = np.asarray(hist.low)
    high_prices = np.asarray(hist.high)
    mid_prices = np.asarray(midpoint(hist.high, hist.low))

    xi = np.arange(0, len(low_prices))

    close_prices_slope, close_prices_intercept, close_prices_r_value, close_prices_p_value, \
        close_prices_std_err = stats.linregress(xi, close_prices)
    low_prices_slope, low_prices_intercept, low_prices_r_value, low_prices_p_value, \
        low_prices_std_err = stats.linregress(xi, low_prices)
    high_prices_slope, high_prices_intercept, high_prices_r_value, high_prices_p_value,\
        high_prices_std_err = stats.linregress(xi, high_prices)
    mid_prices_slope, mid_prices_intercept, mid_prices_r_value, mid_prices_p_value, \
        mid_prices_std_err = stats.linregress(xi, mid_prices)

    log.info('sLRI = {}'.format((mid_prices_intercept - close)))
    log.info('lLRI = {}'.format((close - mid_prices_intercept)))

    if not context.in_long:
        if (mid_prices_intercept - close) > context.threshold:
            order_target_percent(context.asset, 1)
            log.info('bought at {}'.format(close))
            context.in_short = False
            context.in_long = True
    if not context.in_short:
        if (close - mid_prices_intercept) > context.threshold:
            order_target_percent(context.asset, -1)
            log.info('sold at {}'.format(close))
            context.in_short = True
            context.in_long = False

    record(
        close=close,
        price=data.current(context.asset, 'price'),
        sLRI=(mid_prices_intercept - close),
        lLRI=(close - mid_prices_intercept),
    )


def handle_data(context, data):
    try:
        _handle_data(context, data)
    except Exception as e:
        log.warn('aborting the bar on error {}'.format(e))
        context.errors.append(e)

    if len(context.errors) > 0:
        log.info('the errors:\n{}'.format(context.errors))


def analyze(context, results):
    ax1 = plt.subplot(611)
    results.loc[:, ['portfolio_value']].plot(ax=ax1)

    ax2 = plt.subplot(612, sharex=ax1)
    results.loc[:, ['sLRI']].plot(ax=ax2)
    results.loc[:, ['lLRI']].plot(ax=ax2)

    ax3 = plt.subplot(613, sharex=ax1)
    results.loc[:, ['price']].plot(
        ax=ax3,
        label='Price')
    ax3.legend_.remove()
    start, end = ax3.get_ylim()
    ax3.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    transaction_df = extract_transactions(results)
    if not transaction_df.empty:
        buy_df = transaction_df[transaction_df['amount'] > 0]
        sell_df = transaction_df[transaction_df['amount'] < 0]
        ax3.scatter(
            buy_df.index.to_pydatetime(),
            results.loc[buy_df.index, 'price'],
            marker='^',
            s=100,
            c='green',
            label=''
        )
        ax3.scatter(
            sell_df.index.to_pydatetime(),
            results.loc[sell_df.index, 'price'],
            marker='v',
            s=100,
            c='red',
            label=''
        )

    plt.show()
    print(results)


if __name__ == '__main__':
    live = False
    if live:
        run_algorithm(
            capital_base=1000,
            initialize=initialize,
            handle_data=handle_data,
            analyze=analyze,
            exchange_name='poloniex',
            live=True,
            algo_namespace='hedge',
            base_currency='usdt',
            simulate_orders=True,
        )
    else:
        run_algorithm(
            capital_base=10000,
            data_frequency='minute',
            initialize=initialize,
            handle_data=handle_data,
            analyze=analyze,
            exchange_name='poloniex',
            algo_namespace='LinReg',
            base_currency='usdt',
            start=pd.to_datetime('2018-04-21', utc=True),
            end=pd.to_datetime('2018-04-23', utc=True),
        )
