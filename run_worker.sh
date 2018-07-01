#!/usr/bin/env bash
#
###### ALL WORKERS
# NOTE: Bare Minimum 1
#
celery -A kryptobot.workers worker -l info
#
###### ALL WORKERS WITH CELERY BEAT
# NOTE: This will only work again if I uninstall redbeat
#
# celery -A kryptobot.workers worker -l info -B
#
###### ALL WORKERS WITH REDBEAT
# NOTE: This does not work with redbeat installed
# I think with redbeat you have to run celery beat on another worker
# But redbeat is what is allowing launching new scheduled tasks at runtime
#
# celery -A kryptobot.workers worker -l info -B -S redbeat.RedBeatScheduler
#
###### JUST CELERY BEAT
#
# celery -A kryptobot.workers beat
#
###### WITH CELERY REDBEAT
# NOTE: Bare Minimum 2
#
celery -A kryptobot.workers beat -S redbeat.RedBeatScheduler
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
celery -A kryptobot.workers flower --broker=redis://redis:6379/0
#
###### WORKER API
#
# python kryptobot/server/run.py
