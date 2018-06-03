from .app import app


class BaseTask(app.Task):
    """Abstract base class for all tasks in my app."""

    abstract = True
