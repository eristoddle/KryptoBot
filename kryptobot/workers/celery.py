from .app import app

app.conf.update(
    include=[
       # catalyst pandas error
       # 'kryptobot.workers.catalyst.tasks',
       'kryptobot.workers.harvester.tasks',
       'kryptobot.workers.strategy.tasks',
       # 'kryptobot.workers.core.tasks',
       'kryptobot.workers.t2.tasks',
       'kryptobot.workers.batch.tasks',
       'kryptobot.workers.learner.tasks',
       'kryptobot.workers.tasks'
       ],
)

if __name__ == '__main__':
    app.start()
