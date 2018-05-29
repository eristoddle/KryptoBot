

class BaseHarvester:

    def __init__(self, manager, interval, is_simulated):
        self.manager = manager
        self.interval = interval
        self.is_simulated = is_simulated
