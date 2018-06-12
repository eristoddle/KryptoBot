from catalyst import run_algorithm
import importlib
import pandas as pd
from .celery import app
from ..base_task import BaseTask


@app.on_after_configure.connect
def load_open_strategies(sender, **kwargs):
    return 'load_open_strategies not implemented yet'


@app.task(base=BaseTask)
def schedule_catalyst_strategy(params):
    params.pop('strategy_id', None)
    params.pop('portfolio_id', None)
    params.pop('config', None)
    strategy = params.pop('strategy', None)
    mod = importlib.import_module('kryptobot.strategies.catalyst.' + strategy)
    params['start'] = pd.to_datetime(params['start'], utc=True)
    params['end'] = pd.to_datetime(params['end'], utc=True)
    params['handle_data'] = mod.handle_data
    params['initialize'] = mod.initialize
    # params['analyze'] = mod.analyze
    run_algorithm(**params)


@app.task(base=BaseTask)
def schedule_catalyst_ingest(params):
    strategy = params.pop('strategy', None)
    mod = importlib.import_module('kryptobot.strategies.catalyst.' + strategy)
