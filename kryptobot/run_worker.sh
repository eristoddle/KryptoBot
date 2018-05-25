#!/usr/bin/env bash
# celery -A workers worker -l info
# celery -A workers.catalyst worker -l info
# celery -A workers.harvester worker -l info
# celery -A workers.market worker -l info
celery -A workers.strategy worker -l info
