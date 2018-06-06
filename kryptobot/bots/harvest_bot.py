from ..publishers.ticker import Ticker
from ..core import Core


# NOTE: WIP

class HarvestBot(Core):

    harvester = None

    def __init__(self, harvester, config=None):
        super().__init__(config)
        self.harvester = harvester

    # override this to inherit
    def __start(self):
        # self.harvester.add_session(self.session)
        # self.harvester.add_keys(self.config['apis'])
        # self.harvester.add_ticker(Ticker)
        self.harvester.create_schedule()

    def start(self):
        try:
            self.__start()

        except Exception as e:
            print(e)

        finally:
            self.engine.dispose()
