

class BaseHarvester:

    def __init__(self, interval, is_simulated):
        self.interval = interval
        self.is_simulated = is_simulated
