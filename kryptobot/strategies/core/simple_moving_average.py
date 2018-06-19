from catalyst import run_algorithm
from catalyst.api import (record, symbol, order_target_percent,)
from logbook import Logger

NAMESPACE = 'simple_moving_average'
log = Logger()

def initialize(context):
    context.i = 0
    context.asset = symbol('ltc_usd')
    context.short_window = 50
    context.long_window = 200
    context.base_price = None

def handle_data(context, data):
    pass
