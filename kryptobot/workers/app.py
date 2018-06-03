import os
from celery import Celery
from kombu_encrypted_serializer import setup_encrypted_serializer


# TODO: Load from configuration
TEST_KEY = 'WgFNqB8eokKER0aFxEmfnK7qyZmGhGmxxOqccW3oZoM='
os.environ['KOMBU_ENCRYPTED_SERIALIZER_KEY'] = TEST_KEY
serializer_name = setup_encrypted_serializer(serializer='pickle')

app = Celery('kryptobot.workers',
             broker='redis://redis',
             backend='redis://redis',
             task_serializer=serializer_name,
             serializer=serializer_name,
             accept_content=[serializer_name],
             loglevel='info')
