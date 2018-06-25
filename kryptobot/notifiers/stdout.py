from notifiers.base import Base


class StdoutNotifier(Base):

    def __init__(self):
        pass

    def notify(self, message):
        print(message)
