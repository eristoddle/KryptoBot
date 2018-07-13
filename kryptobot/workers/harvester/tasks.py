from .celery import app
from ..config import get_config
from ..base_task import BaseTask
import importlib
import re


config = get_config()

# TODO: get this to work instead of depending on naming conventions and/or importing everything
# def import_harvester(class_name):
#     package = __import__('kryptobot')
#     print('package', dir(package))
#     harvesters = getattr(package, 'harvesters')
#     print('harvesters', dir(harvesters))
#     return getattr(harvesters, class_name)


def title_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def title_to_snake(s):
    _underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
    _underscorer2 = re.compile('([a-z0-9])([A-Z])')
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def dynamic_import(abs_module_path, class_name):
    module_object = importlib.import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


@app.on_after_configure.connect
def load_open_periodic_harvesters(sender, **kwargs):
    # TODO: Use this to load tasks at launch
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     task_message.s('load_open_harvesters not implemented yet'),
    # )
    pass


@app.task(base=BaseTask)
def launch_harvester(classname, params):
    Harvester = dynamic_import(
        'kryptobot.harvesters.' + title_to_snake(classname),
        classname
    )
    harvester = Harvester(**params)
    return harvester.get_data()


@app.task(base=BaseTask)
def schedule_harvester(params):
    Harvester = dynamic_import(
        'kryptobot.harvesters.' + params['harvester'],
        title_case(params['harvester'])
    )
    params.pop('harvester', None)
    harvester = Harvester(**params)
    return harvester.create_schedule(app)
