#!/usr/bin/env bash
#
###### ALL WORKERS
#
celery -A kryptobot.workers worker -l info
#
###### SEPERATE WORKERS
#
# celery -A kryptobot.workers.catalyst worker -l info
# celery -A kryptobot.workers.harvester worker -l info
# celery -Akryptobot.workers.market worker -l info
# celery -A kryptobot.workers.strategy worker -l info
#
###### FLOWER CELERY TASK ADMIN on port 5555
#
# celery -A kryptobot.workers flower --broker=redis://redis:6379/0
#
###### WORKER API
#
# python kryptobot/server/run.py
