from ..bot import Bot
import redis
import time


class RedisListener(Bot):

    def __init__(self, channel, config=None):
        super().__init__(None, config)
        self.channel = channel
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.p.subscribe(channel)
        self.__running = False

    def __run(self):
        self.__running = True
        while self.__running:
            message = self.p.get_message()
            if message:
                self.on_message(message)
                time.sleep(0.001)

    def on_message(self, message):
        print(message)

    def stop(self):
        self.__running = False
