from kryptobot.bot import Bot


# from kryptobot import ticker
# listener = Listener(ticker, {'interval':'15s'})
class Listener(Bot):

    # publisher is a pubsub to subscribe to
    def __init__(self, publisher, publisher_params, config=None):
        super().__init__(None, config)
        publisher.subscribe(self.tick, **publisher_params)
        self.publisher = publisher

    # Extend class and override tick method
    def tick(self):
        print('ticked')
