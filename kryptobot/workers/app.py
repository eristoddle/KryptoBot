import os
from celery import Celery
from kombu_encrypted_serializer import setup_encrypted_serializer
from .config import get_config


config = get_config()

TEST_KEY = config['celery']['encryption_key']
os.environ['KOMBU_ENCRYPTED_SERIALIZER_KEY'] = TEST_KEY
serializer_name = setup_encrypted_serializer(serializer='pickle')

app = Celery('kryptobot.workers',
             broker=config['celery']['broker'],
             backend=config['celery']['backend'],
             redbeat_redis_url=config['celery']['redbeat_redis_url'],
             redbeat_lock_key=None,
             task_serializer=serializer_name,
             serializer=serializer_name,
             accept_content=[serializer_name],
             timezone='America/Chicago',
             loglevel='info')
