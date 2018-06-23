from catalyst.api import symbol


class BaseStrategy():

    def __init__(self, default, extra):
        self.default = default
        self.extra = extra
        # self.quote_currency = self.default['pair'].split('_')[1]
        self.asset = symbol(self.default['pair'])
