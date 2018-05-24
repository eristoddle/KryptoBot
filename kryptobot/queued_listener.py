from threading import Thread
from queue import Queue
import logging
from .listener import Listener

logger = logging.getLogger(__name__)


# from kryptobot import ticker
# listener = QueuedListener(ticker, {'interval':'15s'})
class QueuedListener(Listener):

    def __init__(self, publisher, publisher_params, config=None):
        super().__init__(publisher, publisher_params, config)
        self.__thread = Thread(target=self.__run)  # create thread for listener
        self._jobs = Queue()  # create job queue
        self.__running = False
        self.__thread.start()

    def __run(self):
        self.__running = True
        while self.__running:
            if not self._jobs.empty():
                job = self._jobs.get()
                try:
                    job()
                except Exception as e:
                    print(e)
                    logger.error(job.__name__ + " threw error:\n" + str(e))

    # Extend class and override tick method
    def tick(self):
        self._jobs.put(lambda: self.job())

    # Or Extend class and override job method
    def job(self):
        print('job tick')

    def stop(self):
        self.__running = False
