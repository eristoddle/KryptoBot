from ..db.models import Harvester, Portfolio


class BaseHarvester:

    def __init__(self, interval, is_simulated, portfolio_id=None):
        self.interval = interval
        self.is_simulated = is_simulated
        self.portfolio_id = portfolio_id
        self.create_record()

    def create_record(self):
        print('portfolio id', self.portfolio_id)

    def on_data(self):
        return 'You should replace this in child classes'
