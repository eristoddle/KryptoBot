from .celery import app
from ...bots.bot import Bot
from ..base_task import BaseTask
import importlib
# from celery import chain
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
def schedule_t2_strategy(params):
    Strategy = dynamic_import(
        'kryptobot.strategies.t2.' + params['strategy'],
        title_case(params['strategy'])
    )
    bot = Bot(
        Strategy(params['default'], params['limits'], params['custom']), 
        config=params['config']
    )
    return bot.start()
