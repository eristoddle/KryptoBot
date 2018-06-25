import structlog
import requests

from notifiers.base import Base

class Webhook(Base):

    def __init__(self, url, username, password):
        self.logger = structlog.get_logger()
        self.url = url
        self.username = username
        self.password = password


    def notify(self, message):
        if self.username and self.password:
            request = requests.post(self.url, json=message, auth=(self.username, self.password))
        else:
            request = requests.post(self.url, json=message)
        if not request.status_code == requests.codes.ok:
            self.logger.error("Request failed: %s - %s", request.status_code, request.content)
