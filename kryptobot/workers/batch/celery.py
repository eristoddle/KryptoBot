from ..app import app


app.conf.update(
    include=['kryptobot.workers.batch.tasks'],
)

if __name__ == '__main__':
    app.start()
