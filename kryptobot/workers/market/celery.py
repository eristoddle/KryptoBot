from __future__ import absolute_import, unicode_literals
from celery import Celery

# TODO: Load from configuration

app = Celery('kryptobot.workers.market',
             broker='redis://redis',
             # backend='amqp://',
             loglevel='info',
             include=['kryptobot.workers.market.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
