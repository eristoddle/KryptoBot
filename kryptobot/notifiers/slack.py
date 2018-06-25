import structlog
import slackweb

from notifiers.base import Base

class Slack(Base):

    def __init__(self, slack_webhook):
        self.logger = structlog.get_logger()
        self.slack_name = "crypto-signal"
        self.slack_client = slackweb.Slack(url=slack_webhook)


    def notify(self, message):
        max_message_size = 4096
        message_chunks = self.chunk_message(message=message, max_message_size=max_message_size)
        for message_chunk in message_chunks:
            self.slack_client.notify(text=message_chunk)
