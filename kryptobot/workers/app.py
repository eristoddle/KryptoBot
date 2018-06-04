import os
from celery import Celery
from kombu_encrypted_serializer import setup_encrypted_serializer


# TODO: Load from configuration
TEST_KEY = 'WgFNqB8eokKER0aFxEmfnK7qyZmGhGmxxOqccW3oZoM='
os.environ['KOMBU_ENCRYPTED_SERIALIZER_KEY'] = TEST_KEY
serializer_name = setup_encrypted_serializer(serializer='pickle')

app = Celery('kryptobot.workers',
             broker='redis://redis:6379/0',
             backend='redis://redis:6379/1',
             redbeat_redis_url="redis://redis:6379/2",
             redbeat_lock_key=None,
             task_serializer=serializer_name,
             serializer=serializer_name,
             accept_content=[serializer_name],
             timezone='America/Chicago',
             loglevel='info')
