from ..db.models import Portfolio

class Base():

    def __init__(self, batch_id, portfolio_id):
        self.portfolio_id = portfolio_id
        self.batch_id = batch_id
        # query = session.query(model).filter_by(**kwargs)
        # instance = query.first()
