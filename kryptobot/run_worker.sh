#!/usr/bin/env bash
celery -A workers worker -l info
