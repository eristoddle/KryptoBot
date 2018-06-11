import numpy as np
import pandas as pd
import talib as ta
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

log = Logger('BuyTheDip')


def initialize(context):
    context.asset1 = symbol('btc_usd')
    context.asset2 = symbol('eth_usd')
    context.asset3 = symbol('xmr_usd')
    context.asset4 = symbol('xrp_usd')
    context.changes1Length = 2
    context.changes2Length = 2
    context.emaOfChanges1Length = 24  # The length of the change indicator.
    context.emaOfChanges2Length = 24  # The length of the change in change indicator.
    context.bar_count = 25
    context.order_size = 1
    context.slippage_allowed = 0.05
    context._changes1Ratio = -1.0
    context._changes2Ratio = 0.0  # The influence of change in change upon fitness.

    context._historyLength = 2
    context._changes1Length = 2
    context._changes2Length = 2


def handle_data(context, data):
    prices1 = data.history(
        context.asset1,
        bar_count=context.bar_count,
        fields=['close'],
        frequency='1d')
    prices2 = data.history(
        context.asset2,
        bar_count=context.bar_count,
        fields=['close'],
        frequency='1d')
    prices3 = data.history(
        context.asset3,
        bar_count=context.bar_count,
        fields=['close'],
        frequency='1d')
    prices4 = data.history(
        context.asset4,
        bar_count=context.bar_count,
        fields=['close'],
        frequency='1d')

    analysis1 = pd.DataFrame(index=prices1.index)
    analysis2 = pd.DataFrame(index=prices2.index)
    analysis3 = pd.DataFrame(index=prices3.index)
    analysis4 = pd.DataFrame(index=prices4.index)

    # first change calculation
    if prices1.size >= 2:
        change1 = prices1.close.pct_change()
        analysis1['changes1History'] = prices1.close.pct_change()
    if len(change1) >= 2:
        analysis1['changes2History'] = change1.pct_change()
        change2 = change1.pct_change()
    if len(change2) >= 5:
        analysis1['ema1'] = ta.EMA(analysis1['changes1History'].as_matrix(), context.emaOfChanges1Length)
        analysis1['ema2'] = ta.EMA(analysis1['changes2History'].as_matrix(), context.emaOfChanges2Length)

    # second change calculation
    if prices2.size >= 2:
        change1 = prices2.close.pct_change()
        analysis2['changes1History'] = prices2.close.pct_change()
    if len(change1) >= 2:
        analysis2['changes2History'] = change2.pct_change()
        change2 = change1.pct_change()
    if len(change2) >= 5:
        analysis2['ema1'] = ta.EMA(analysis2['changes1History'].as_matrix(), context.emaOfChanges1Length)
        analysis2['ema2'] = ta.EMA(analysis2['changes2History'].as_matrix(), context.emaOfChanges2Length)

    # third change calculation
    if prices3.size >= 2:
        change1 = prices3.close.pct_change()
        analysis3['changes1History'] = prices3.close.pct_change()
    if len(change1) >= 2:
        analysis3['changes2History'] = change1.pct_change()
        change2 = change1.pct_change()
    if len(change2) >= 5:
        analysis3['ema1'] = ta.EMA(analysis3['changes1History'].as_matrix(), context.emaOfChanges1Length)
        analysis3['ema2'] = ta.EMA(analysis3['changes2History'].as_matrix(), context.emaOfChanges2Length)

    # forth change calculation
    if prices4.size >= 2:
        change1 = prices4.close.pct_change()
        analysis4['changes1History'] = prices4.close.pct_change()
    if len(change1) >= 2:
        analysis4['changes2History'] = change1.pct_change()
        change2 = change1.pct_change()
    if len(change2) >= 5:
        analysis4['ema1'] = ta.EMA(analysis4['changes1History'].as_matrix(), context.emaOfChanges1Length)
        analysis4['ema2'] = ta.EMA(analysis4['changes2History'].as_matrix(), context.emaOfChanges2Length)

    context.analysis1 = analysis1
    context.analysis2 = analysis2
    context.analysis3 = analysis3
    context.analysis4 = analysis4
    context.price1 = data.current(context.asset1, 'price')
    context.price2 = data.current(context.asset2, 'price')
    context.price3 = data.current(context.asset3, 'price')
    context.price4 = data.current(context.asset4, 'price')
    makeOrders(context, analysis1, analysis2, analysis3, analysis4)


def makeOrders(context, a1, a2, a3, a4):
    if (getLast(a1, 'ema1') < getLast(a2, 'ema1')) and (getLast(a1, 'ema1') < getLast(a4, 'ema1')) and \
            (getLast(a1, 'ema1') < getLast(a3, 'ema1')):
        order_target_percent(context.asset1, target=1)
        order_target_percent(context.asset2, target=0)
        order_target_percent(context.asset3, target=0)
        order_target_percent(context.asset4, target=0)
        log.info('buy btc')

    if (getLast(a2, 'ema1') < getLast(a4, 'ema1')) and (getLast(a2, 'ema1') < getLast(a1, 'ema1')) and \
            (getLast(a2, 'ema1') < getLast(a3, 'ema1')):
        order_target_percent(context.asset1, target=0)
        order_target_percent(context.asset2, target=1)
        order_target_percent(context.asset3, target=0)
        order_target_percent(context.asset4, target=0)
        log.info('buy eth')

    if (getLast(a3, 'ema1') < getLast(a2, 'ema1')) and (getLast(a3, 'ema1') < getLast(a1, 'ema1')) and \
            (getLast(a3, 'ema1') < getLast(a4, 'ema1')):
        order_target_percent(context.asset1, target=0)
        order_target_percent(context.asset2, target=0)
        order_target_percent(context.asset3, target=1)
        order_target_percent(context.asset4, target=0)
        log.info('buy xmr')

    if (getLast(a4, 'ema1') < getLast(a2, 'ema1')) and (getLast(a4, 'ema1') < getLast(a1, 'ema1')) and \
            (getLast(a4, 'ema1') < getLast(a3, 'ema1')):
        order_target_percent(context.asset1, target=0)
        order_target_percent(context.asset2, target=0)
        order_target_percent(context.asset3, target=0)
        order_target_percent(context.asset4, target=1)
        log.info('buy xrp')


def analyze(context, results):
    results.portfolio_value.plot()
    ax1 = plt.subplot(411)
    results.loc[:, ['portfolio_value']].plot(ax=ax1)
    plt.show()
    print(results)


def getLast(arr, name):
    return arr[name][arr[name].index[-1]]


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
            algo_namespace='buythedip',
            base_currency='usdt',
            simulate_orders=True,
        )
    else:
        run_algorithm(
            capital_base=10000,
            data_frequency='daily',
            initialize=initialize,
            handle_data=handle_data,
            analyze=analyze,
            exchange_name='bitfinex',
            algo_namespace='buythedip',
            base_currency='usd',
            start=pd.to_datetime('2018-01-01', utc=True),
            end=pd.to_datetime('2018-04-02', utc=True),
        )
