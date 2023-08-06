"""Declares :class:`WebhookListener`."""
from .iwebhooklistener import IWebhookListener
from .message import Message


class WebhookListener(IWebhookListener):

    def __init__(self, message: Message):
        self.message = message
