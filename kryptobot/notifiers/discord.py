import structlog
from webcord import Webhook


class DiscordNotifier():

    def __init__(self, webhook, username, avatar=None):
        self.logger = structlog.get_logger()
        self.discord_username = username
        self.discord_client = Webhook(webhook, avatar_url=avatar)

    def notify(self, message):
        self.discord_client.send_message(message, self.discord_username)
