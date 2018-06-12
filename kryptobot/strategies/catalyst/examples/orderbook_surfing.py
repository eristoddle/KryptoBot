import asyncio
import os
import sys
import operator
import ccxt.async as ccxt

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

exchange = ccxt.bitmex({
    'apiKey': 'J19Bq4scXCeyfvPsBCdB8QdN',
    'secret': 'LhpNz6azErECdoGJXkjWbC1S0kVcQxm0IKOLAi7S7h0d0rv6',
    'enableRateLimit': True,
})
exchange.urls['api'] = exchange.urls['test']


pair = 'XBT/USD'
amount = 100
fees = 0.2 + 0.1


async def main(exchange, symbol):
    while True:
        print('--------------------------------------------------------------')
        print(exchange.iso8601(exchange.milliseconds()), 'fetching', symbol, 'ticker from', exchange.name)
        # this can be any call really
        ticker = await exchange.fetch_order_book(symbol)
        bestBid = ticker['bids'][0]
        bestAsk = ticker['asks'][0]
        spread = bestAsk[0] - bestBid[0]
        print(exchange.iso8601(exchange.milliseconds()), 'fetched', symbol, 'ticker from', exchange.name)
        print('best bid: ', bestBid)
        print('best ask: ', bestAsk)
        print('all: ', ticker)
        print('spread: ', spread)
        #print('which one do we surf? ', biggestOrder(ticker))
        print('do we trade? ', doWeTrade(bestBid, bestAsk))


def doWeTrade(bestBid, bestAsk):
    afterFees = (bestAsk[0] / 100 * (100 - fees)) - (bestBid[0] / 100 * (100 + fees))
    if afterFees >= 0:
        return True
    else:
        return False


#def letsTrade(doWeTrade, bestBid, bestAsk):
#    while doWeTrade:
#        if orders == 0:
#            weBuy = bestBid[0] / 100 * (100 + 0.1)
#            weSell = bestAsk[0]
            #exchange.create_limit_buy_order(pair, amount, weBuy)
            #exchange.create_limit_sell_order(pair, amount, weSell)
#        else:
#            return


def max_value(inputlist):
    flatList = ([sublist[-1] for sublist in inputlist])
    maximum = max(flatList)
    index = flatList.index(maximum)
    return inputlist[index]

asyncio.get_event_loop().run_until_complete(main(exchange, pair))
