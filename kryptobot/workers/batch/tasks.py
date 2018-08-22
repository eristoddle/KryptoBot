from .celery import app
from ..config import core
from ..base_task import BaseTask
import importlib


def title_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def dynamic_import(abs_module_path, class_name):
    module_object = importlib.import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


@app.task(base=BaseTask)
def schedule_batch(params):
    # print('params', params)
    class_name = params.pop('batch', None)
    batch_params = params.pop('params', None)
    batch_params['batch_id'] = params['batch_id']
    batch_params['portfolio_id'] = params['portfolio_id']
    batch_params['core'] = core
    # TODO: Can I make this less convoluted
    config = params.pop('config', None)
    batch_params['core'].config['apis'] = config['apis']
    Batch = dynamic_import(
        'kryptobot.batches.' + class_name,
        title_case(class_name)
    )
    batch = Batch(**batch_params)
    batch.run()
