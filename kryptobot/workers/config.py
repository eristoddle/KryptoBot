from ..core import Core
import json
import os


def get_config():
    config = {
        "db": {
            "engine": "sqlite",
            "name": "core.db",
            "username": None,
            "password": None,
            "host": None
        },
        "celery": {
            "encryption_key": "WgFNqB8eokKER0aFxEmfnK7qyZmGhGmxxOqccW3oZoM=",
            "broker": "redis://redis:6379/0",
            "backend": "redis://redis:6379/1",
            "redbeat_redis_url": "redis://redis:6379/2"
        }
    }
    json_path = os.path.realpath(__file__).replace('.py', '.json')
    if os.path.isfile(json_path):
        with open(json_path, encoding='utf-8') as data_file:
            config = json.loads(data_file.read())
    return config


core = Core(config=get_config())
