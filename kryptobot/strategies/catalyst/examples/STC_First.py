import numpy as np
import pandas as pd
import talib as ta
from catalyst.api import symbol, order_target_percent, record, order
from catalyst.exchange.utils.stats_utils import get_pretty_stats
from catalyst.utils.run_algo import run_algorithm
from logbook import Logger
from matplotlib.dates import date2num
import matplotlib.pyplot as plt

log = Logger('Schaff Trend Cycle')


def initialize(context):
    log.info('initializing STC algorithm')
    context.bitfinex = context.exchanges['bitfinex']
    context.asset = symbol('btc_usd', context.bitfinex.name)

    context.threshold = 1
    context.in_high = False
    context.in_low = False

    context.ORDER_SIZE = 10
    context.SLIPPAGE_ALLOWED = 0.05

    context.swallow_errors = True
    context.errors = []

    context.BARS = 60

    context.length = 10
    context.factor = 0.5
    context.MACD_FAST = 23
    context.MACD_SLOW = 50
    context.MACD_SIGNAL = 9
    pass


def _handle_data(context, data):
    prices = data.history(
        context.asset,
        bar_count=context.BARS,
        fields=['price', 'open', 'high', 'low', 'close'],
        frequency='1d')

    analysis = pd.DataFrame(index=prices.index)
    """
    MACD Calculation and Signal Creation. 
    input: analysis panda DataFrame
    output: bool
    """
    analysis['macd'], analysis['macdSignal'], analysis['macdHist'] = ta.MACD(
        prices.close.as_matrix(), fastperiod=context.MACD_FAST,
        slowperiod=context.MACD_SLOW, signalperiod=context.MACD_SIGNAL)
    analysis['macd_test'] = np.where((analysis.macd > analysis.macdSignal), 1, 0)


    """
    m = analysis['macd']
    v1 = min(m, context.length)
    v2 = max(m, context.length) - v1
    f1 = 0
    if v2 > 0:
        f1 = ((m - v1) / v2) * 100
    else:
        f1 = f1[1]



    pf = (na(pf[1]) ? f1: pf[1] + (context.factor * (f1 - pf[1])))
    v3 = min(pf, context.length)
    v4 = max(pf, context.length) - v3
    f2 = (v4 > 0 ? ((pf - v3) / v4) *100: nz(f2[1]))
    pff = (na(pff[1]) ? f2: pff[1] + (factor * (f2 - pff[1])))
    """

    # Save the prices and analysis to send to analyze
    context.prices = prices
    context.analysis = analysis
    context.price = data.current(context.asset, 'price')

    makeOrders(context, analysis)

    # Log the values of this bar
    logAnalysis(analysis)


def handle_data(context, data):
    log.info('handling bar {}'.format(data.current_dt))
    try:
        _handle_data(context, data)
    except Exception as e:
        log.warn('aborting the bar on error {}'.format(e))
        context.errors.append(e)

    log.info('completed bar {}, total execution errors {}'.format(
        data.current_dt,
        len(context.errors)
    ))

    if len(context.errors) > 0:
        log.info('the errors:\n{}'.format(context.errors))


def makeOrders(context, analysis):
    if context.asset in context.portfolio.positions:

        # Current position
        position = context.portfolio.positions[context.asset]

        if (position == 0):
            log.info('Position Zero')
            return

        # Cost Basis
        cost_basis = position.cost_basis

        log.info(
            'Holdings: {amount} @ {cost_basis}'.format(
                amount=position.amount,
                cost_basis=cost_basis
            )
        )

        # Sell when holding and got sell singnal
        if isSell(context, analysis):
            profit = (context.price * position.amount) - (
                    cost_basis * position.amount)
            order_target_percent(
                asset=context.asset,
                target=0,
                limit_price=context.price * (1 - context.SLIPPAGE_ALLOWED),
            )
            log.info(
                'Sold {amount} @ {price} Profit: {profit}'.format(
                    amount=position.amount,
                    price=context.price,
                    profit=profit
                )
            )
        else:
            log.info('no buy or sell opportunity found')
    else:
        # Buy when not holding and got buy signal
        if isBuy(context, analysis):
            order(
                asset=context.asset,
                amount=context.ORDER_SIZE,
                limit_price=context.price * (1 + context.SLIPPAGE_ALLOWED)
            )
            log.info(
                'Bought {amount} @ {price}'.format(
                    amount=context.ORDER_SIZE,
                    price=context.price
                )
            )


def isBuy(context, analysis):
    if getLast(analysis, 'macd_test') == 1:
        return True
    return False


def isSell(context, analysis):
    if getLast(analysis, 'macd_test') == 0:
        return True
    return False


def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    results[['portfolio_value']].plot()
    plt.show()


def logAnalysis(analysis):
    log.info('- macd:           {:.2f}'.format(getLast(analysis, 'macd')))
    log.info('- macdSignal:     {:.2f}'.format(getLast(analysis, 'macdSignal')))
    log.info('- macdHist:       {:.2f}'.format(getLast(analysis, 'macdHist')))
    log.info('- macd_test:      {}'.format(getLast(analysis, 'macd_test')))


def chart(context, prices, analysis, results):
    results.portfolio_value.plot()

    # Data for matplotlib finance plot
    dates = date2num(prices.index.to_pydatetime())

    # Create the Open High Low Close Tuple
    prices_ohlc = [tuple([dates[i],
                          prices.open[i],
                          prices.high[i],
                          prices.low[i],
                          prices.close[i]]) for i in range(len(dates))]

    fig = plt.figure(figsize=(14, 18))

    # Draw MACD with TaLib
    ax3 = fig.add_subplot(413)
    ax3.set_ylabel('MACD: ' + str(context.MACD_FAST) + ', ' + str(
        context.MACD_SLOW) + ', ' + str(context.MACD_SIGNAL), size=12)
    analysis.macd.plot(ax=ax3, color='b', label='Macd')
    analysis.macdSignal.plot(ax=ax3, color='g', label='Signal')
    analysis.macdHist.plot(ax=ax3, color='r', label='Hist')
    ax3.axhline(0, lw=2, color='0')
    handles, labels = ax3.get_legend_handles_labels()
    ax3.legend(handles, labels)

    plt.show()


def getLast(arr, name):
    return arr[name][arr[name].index[-1]]


run_algorithm(initialize=initialize,
              handle_data=handle_data,
              analyze=analyze,
              capital_base=10000,
              live=False,
              base_currency='usd',
              exchange_name='bitfinex',
              algo_namespace='STC',
              data_frequency='daily',
              start=pd.to_datetime('2017-11-01', utc=True),
              end=pd.to_datetime('2017-12-31', utc=True))
