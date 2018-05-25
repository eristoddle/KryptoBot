from __future__ import absolute_import, unicode_literals
from celery import Celery

# TODO: Load from configuration

app = Celery('kryptobot.workers',
             broker='redis://redis',
             backend='redis://redis',
             loglevel='info',
             include=[
                'kryptobot.workers.catalyst.tasks',
                'kryptobot.workers.harvester.tasks',
                'kryptobot.workers.market.tasks',
                'kryptobot.workers.strategy.tasks',
                ])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
