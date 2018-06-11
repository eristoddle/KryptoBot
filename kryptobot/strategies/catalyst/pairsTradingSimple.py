"""
https://www.quantopian.com/posts/how-to-build-a-pairs-trading-strategy-on-quantopian
"""
import numpy as np
import pandas as pd
from catalyst.api import symbol, order_target_percent, record
from catalyst.exchange.utils.stats_utils import get_pretty_stats
from catalyst.utils.run_algo import run_algorithm
from logbook import Logger

log = Logger('pairs_trader')


def initialize(context):
    log.info('initializing pairs trading algorithm')
    context.bitfinex = context.exchanges['bitfinex']
    context.pair1 = symbol('btc_usd', context.bitfinex.name)
    context.pair2 = symbol('xmr_usd', context.bitfinex.name)

    context.swallow_errors = True
    context.errors = []

    context.threshold = 2.6
    context.in_high = False
    context.in_low = False
    pass


def _handle_data(context, data):
    s1 = context.pair1
    s2 = context.pair2

    p61 = data.history(s1, bar_count=60, frequency='1T', fields='close')
    p62 = data.history(s2, bar_count=60, frequency='1T', fields='close')

    p51 = p61.iloc[-5:]
    p52 = p62.iloc[-5:]

    # Get the 60 day mavg
    m60 = np.mean(p61 - p62)
    # Get the std of the last 60 days
    std60 = np.std(p61 - p62)

    # Current diff = 5 day mavg
    m5 = np.mean(p51 - p52)

    # Compute z-score
    if std60 > 0:
        zscore = (m5 - m60) / std60
    else:
        zscore = 0

    if zscore > context.threshold and not context.in_high:
        log.info('Short BTC Long XMR')
        order_target_percent(s1, -0.5)  # short top
        order_target_percent(s2, 0.5)  # long bottom
        context.in_high = True
        context.in_low = False
    elif zscore < -context.threshold and not context.in_low:
        log.info('Long BTC Short XMR')
        order_target_percent(s1, 0.5)  # long top
        order_target_percent(s2, -0.5)  # short bottom
        context.in_high = False
        context.in_low = True
    elif abs(zscore) < 0.1:
        log.info('Back to zero')
        order_target_percent(s1, 0)
        order_target_percent(s2, 0)
        context.in_high = False
        context.in_low = False

    record(zscore=zscore)


def handle_data(context, data):
    # log.info('----------------------------------------------------------')
    try:
        _handle_data(context, data)
    except Exception as e:
        log.warn('aborting the bar on error {}'.format(e))
        context.errors.append(e)

    # log.info('completed bar {}, total execution errors {}'.format(data.current_dt, len(context.errors)))

    if len(context.errors) > 0:
        log.info('the errors:\n{}'.format(context.errors))


def analyze(context, perf):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(411)
    ax2 = plt.subplot(412)
    perf.loc[:, ['portfolio_value']].plot(ax=ax1)
    perf[['zscore']].plot(ax=ax2)
    plt.show()


run_algorithm(initialize=initialize,
              handle_data=handle_data,
              analyze=analyze,
              capital_base=10000,
              live=False,
              base_currency='usd',
              exchange_name='bitfinex',
              algo_namespace='Trade Pairs',
              data_frequency='minute',
              start=pd.to_datetime('2018-04-01', utc=True),
              end=pd.to_datetime('2018-04-02', utc=True))
