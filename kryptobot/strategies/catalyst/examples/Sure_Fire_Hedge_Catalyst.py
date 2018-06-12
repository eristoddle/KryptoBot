import numpy as np
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
from catalyst import run_algorithm
from catalyst.exchange.utils.stats_utils import extract_transactions
from catalyst.api import (
    record,
    order,
    order_target,
    symbol,
    get_order
)
from logbook import Logger

log = Logger("Hedge")


def initialize(context):
    log.info('Initializing Sure Fire Hedge Algorithm')
    context.bitfinex = context.exchanges['poloniex']
    context.asset = symbol('btc_usdt', context.bitfinex.name)

    context.ORDER_SIZE = 0.1
    context.BARS = 365
    context.frequency = 'minute'

    context.swallow_errors = True
    context.errors = []

    context.upper = 150
    context.lower = 300
    context.multiplyBy = 3
    context.distance = 150
    context.level = 1

    context.SMA_FAST = 50
    context.SMA_SLOW = 100

    context.in_long = False
    context.in_short = False
    context.cost_basis = 1

    pass


def _handle_data(context, data):
    s1 = context.asset
    prices = data.history(s1, bar_count=context.BARS, fields=['price', 'open', 'high', 'low', 'close'],
                          frequency=context.frequency)
    analysis = pd.DataFrame(index=prices.index)

    # SMA FAST
    analysis['sma_f'] = ta.SMA(prices.close.as_matrix(), context.SMA_FAST)
    # SMA SLOW
    analysis['sma_s'] = ta.SMA(prices.close.as_matrix(), context.SMA_SLOW)
    # SMA FAST over SLOW Crossover
    analysis['sma_test'] = np.where(analysis.sma_f > analysis.sma_s, 1, 0)

    # Save the prices and analysis to send to analyze
    context.prices = prices
    context.analysis = analysis
    context.price = data.current(context.asset, 'price')

    record(price=data.current(context.asset, 'price'),
           cash=context.portfolio.cash,
           short_mavg=analysis['sma_f'],
           long_mavg=analysis['sma_s'])

    makeOrders(context, analysis)


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

    # Get the base_currency that was passed as a parameter to the simulation
    exchange = list(context.exchanges.values())[0]
    base_currency = exchange.base_currency.upper()

    # First chart: Plot portfolio value using base_currency
    ax1 = plt.subplot(411)
    perf.loc[:, ['portfolio_value']].plot(ax=ax1)
    ax1.legend_.remove()
    ax1.set_ylabel('Portfolio Value\n({})'.format(base_currency))
    start, end = ax1.get_ylim()
    ax1.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))


    # Second chart: Plot asset price, moving averages and buys/sells
    ax2 = plt.subplot(412, sharex=ax1)
    perf.loc[:, ['price']].plot(
        ax=ax2,
        label='Price')
    ax2.legend_.remove()
    ax2.set_ylabel('{asset}\n({base})'.format(
        asset=context.asset.symbol,
        base=base_currency
    ))
    start, end = ax2.get_ylim()
    ax2.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    transaction_df = extract_transactions(perf)
    if not transaction_df.empty:
        buy_df = transaction_df[transaction_df['amount'] > 0]
        sell_df = transaction_df[transaction_df['amount'] < 0]
        ax2.scatter(
            buy_df.index.to_pydatetime(),
            perf.loc[buy_df.index, 'price'],
            marker='^',
            s=100,
            c='green',
            label=''
        )
        ax2.scatter(
            sell_df.index.to_pydatetime(),
            perf.loc[sell_df.index, 'price'],
            marker='v',
            s=100,
            c='red',
            label=''
        )

    plt.show()


def makeOrders(context, analysis):
    if context.in_long:
        weAreLong(context, analysis)

    elif context.in_short:
        weAreShort(context, analysis)

    else:
        if getLast(analysis, 'sma_test') == 1:
            order(context.asset, amount=context.ORDER_SIZE)
            context.in_long = True
            context.in_short = False
            context.level = 1
            context.cost_basis = context.price
            '''
            context.position = position
            '''
            log.info('Bought {amount} @ {price}'.format(amount=context.ORDER_SIZE, price=context.price))


def weAreLong(context, analysis):
    s1 = context.asset
    TP = context.cost_basis + context.upper
    SL = context.cost_basis - context.lower
    Crit = context.cost_basis - context.distance
    position = context.portfolio.positions[context.asset]
    log.info('We Are Long. Holdings: {amount} @ {cost_basis}'.format(amount=position.amount,
                                                                     cost_basis=context.cost_basis))

    if context.price < Crit:
        order(s1, amount=-(context.ORDER_SIZE * context.multiplyBy * context.level))
        context.in_long = False
        context.in_short = True
        context.level += 1
        log.info('Kill Long! GO SHORT! Sold {amount} @ {price}'.format(amount=position.amount, price=context.price))

    elif context.price > TP:
        context.in_long = False
        context.in_short = False
        context.level = 1
        order_target(s1, 0)
        log.info('We made it! Sold {amount} @ {price}'.format(amount=position.amount, price=context.price))

    elif context.price < SL:
        context.in_long = False
        context.in_short = False
        context.level = 1
        order_target(s1, 0)
        log.info('We lost it all! Sold {amount} @ {price}'.format(amount=position.amount, price=context.price))

    else:
        log.info('no buy or sell opportunity found')


def weAreShort(context, analysis):
    s1 = context.asset
    TP = context.cost_basis - context.lower
    SL = context.cost_basis + context.upper
    Crit = context.cost_basis
    position = context.portfolio.positions[context.asset]
    log.info('We are Short. Holdings: {amount} @ {cost_basis}'.format(amount=position.amount, cost_basis=context.cost_basis))

    if context.price > Crit:
        order(s1, amount=(context.ORDER_SIZE * context.multiplyBy * context.level))
        context.in_long = True
        context.in_short = False
        context.level += 1
        log.info('Kill Short! GO LONG! Sold {amount} @ {price}'.format(amount=position.amount, price=context.price))

    elif context.price < TP:
        context.in_long = False
        context.in_short = False
        context.level = 1
        order_target(s1, 0)
        log.info('We made it! Sold {amount} @ {price}'.format(amount=position.amount, price=context.price))

    elif context.price > SL:
        context.in_long = False
        context.in_short = False
        context.level = 1
        order_target(s1, 0)
        log.info('We lost it all! Sold {amount} @ {price}'.format(amount=position.amount, price=context.price))

    else:
        log.info('no buy or sell opportunity found')


def getLast(arr, name):
    return arr[name][arr[name].index[-1]]


if __name__ == '__main__':
    live = False
    if live:
        run_algorithm(
            capital_base=3000,
            initialize=initialize,
            handle_data=handle_data,
            analyze=analyze,
            exchange_name='bittrex',
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
            algo_namespace='hedge',
            base_currency='usdt',
            start=pd.to_datetime('2018-04-01', utc=True),
            end=pd.to_datetime('2018-04-02', utc=True),
        )
