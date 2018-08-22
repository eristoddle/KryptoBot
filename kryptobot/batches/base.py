from ..db.models import Portfolio


class Base():

    def __init__(self, batch_id, portfolio_id, core):
        self.portfolio_id = portfolio_id
        self.batch_id = batch_id
        self._session = core.session()
        self.config = core.config
        self.portfolio = self._session.query(Portfolio).get(portfolio_id)
