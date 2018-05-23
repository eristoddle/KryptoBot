from kryptobot.bot import Bot
from kryptobot import ticker


class Listener(Bot):

    def __init__(self, strategy=None, config=None, interval='1m'):
        super().__init__(strategy, config)
        self.interval = interval
        ticker.subscribe(self.tick, interval)

    # Extend class and override tick method
    def tick(self):
        print('ticked')
