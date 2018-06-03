from .app import app

app.conf.update(
    include=[
       'kryptobot.workers.catalyst.tasks',
       'kryptobot.workers.harvester.tasks',
       'kryptobot.workers.market.tasks',
       'kryptobot.workers.strategy.tasks',
       ],
)

if __name__ == '__main__':
    app.start()
