# from celery.schedules import crontab
from .celery import app
from ..base_task import BaseTask
from ...harvesters.arbitrage_harvester import ArbitrageHarvester


# TODO: Find a way to load configs for celery jobs
# Also api keys on this side multitenant
# config = getcwd() + '/config.json'
config = {
        "db": {
            "engine": "sqlite",
            "name": "core.db",
            "username": "",
            "password": "",
            "host": ""
        }
    }

# TODO: get this to work instead of depending on naming conventions and/or importing everything
# def import_harvester(class_name):
#     package = __import__('kryptobot')
#     print('package', dir(package))
#     harvesters = getattr(package, 'harvesters')
#     print('harvesters', dir(harvesters))
#     return getattr(harvesters, class_name)


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def import_harvester(harvester):
    harvester = to_camel_case(harvester)
    return globals()[harvester]


@app.on_after_configure.connect
def load_open_periodic_harvesters(sender, **kwargs):
    # TODO: Use this to load tasks at launch
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     task_message.s('load_open_harvesters not implemented yet'),
    # )
    pass


@app.task(base=BaseTask)
def launch_harvester(kwargs):
    Harvester = import_harvester(kwargs['harvester'])
    harvester = Harvester(**kwargs)
    return harvester.get_data()


@app.task(base=BaseTask)
def task_message(arg):
    print(arg)
