from .celery import app
from ..base_task import BaseTask


@app.on_after_configure.connect
def load_open_strategies(sender, **kwargs):
    return 'load_open_strategies not implemented yet'


@app.task(base=BaseTask)
def schedule_catalyst_strategy(params):
    pass
