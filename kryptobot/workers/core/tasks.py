from catalyst import run_algorithm
from kryptobot.catalyst_extensions.exchange.exchange_bundle import ExchangeBundle
import importlib
from celery import chain
from .celery import app
from ..base_task import BaseTask
from pathlib import Path


def title_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def dynamic_import(abs_module_path, class_name):
    module_object = importlib.import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


@app.on_after_configure.connect
def load_open_strategies(sender, **kwargs):
    return 'load_open_strategies not implemented yet'


@app.task(base=BaseTask)
def schedule_core_strategy(params):
    Strategy = dynamic_import(
        'kryptobot.strategies.core.' + params['strategy'],
        title_case(params['strategy'])
    )
    strategy = Strategy(params['default'], params['custom'])
    run_params = strategy.get_run_params()
    home = str(Path.home())
    run_params['output'] = home + '/.catalyst_pickles/' + str(params['strategy_id']) + '.pickle'
    try:
        run_algorithm(**run_params)
    except:
        ingest_params = strategy.get_ingest_params()
        chain(schedule_core_ingest(**ingest_params) | run_algorithm(**run_params))()


@app.task(base=BaseTask)
def schedule_core_ingest(exchange_name, data_frequency, include_symbols=None, start=None, end=None, csv=None):
    exchange_bundle = ExchangeBundle(exchange_name)
    exchange_bundle.ingest(
        data_frequency=data_frequency,
        include_symbols=include_symbols,
        start=start,
        end=end,
        csv=csv
    )
