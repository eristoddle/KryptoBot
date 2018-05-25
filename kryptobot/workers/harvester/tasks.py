from __future__ import absolute_import, unicode_literals
from .celery import app


@app.task
def launch_harvester(strategy, params):
    return 'launch_harvester not implemented yet'


@app.task
def load_open_harvesters():
    return 'load_open_harvesters not implemented yet'
