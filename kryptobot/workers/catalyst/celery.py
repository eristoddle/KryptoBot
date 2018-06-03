from ..app import app


app.conf.update(
    include=['kryptobot.workers.catalyst.tasks'],
)

if __name__ == '__main__':
    app.start()
