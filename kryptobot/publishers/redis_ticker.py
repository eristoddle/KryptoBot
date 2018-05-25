from threading import Thread
import time
import redis
import logging
# TODO: Make this an optional replacment for ticker
# redis py
# https://github.com/andymccurdy/redis-py
# TODO: Make a version using Apscheduler
# https://hackernoon.com/visualizing-bitcoin-prices-moving-averages-using-dash-aac93c994301

logger = logging.getLogger(__name__)

tickers = {}


class RedisTicker:

    def __init__(self, channel='ticker'):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.channel = channel

    # NOTE: subscribe directly from redis
    # def subscribe(self, tick_callable, interval):
    #     self.start_ticker(interval)
    #     self.p.subscribe(tick_callable, "tick" + interval)

    def start_ticker(self, interval):
        if interval not in tickers:
            tickers[interval] = Thread(
                target=self.__start_ticker, args=(
                    interval,)).start()

    def __start_ticker(self, interval):
        """Start a ticker own its own thread, will use pypubsub to send a message each time interval"""
        logger.info(interval + " ticker running...")
        live_tick_count = 0
        while True:
            """Running this 'ticker' from the main loop to trigger listeners to pull candles every 5 minutes"""
            logger.info("Live Tick: {}".format(str(live_tick_count)))
            print(interval + " tick")
            self.r.publish(self.channel, "tick" + interval)
            live_tick_count += 1
            time.sleep(self.__convert_interval_to_int(interval))

    def __convert_interval_to_int(self, interval):
        if interval == "15s":
            return 15
        if interval == "1m":
            return 60
        if interval == "5m":
            return 300
        if interval == "15m":
            return 900
        if interval == "1h":
            return 3600
