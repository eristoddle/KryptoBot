from .celery import app
from .base_task import BaseTask


@app.task(base=BaseTask)
def stop_task(id):
    app.control.revoke(id)
