"""Declares :class:`IWebhookListener`."""
from fastapi import Request
from unimatrix.lib import wildcard

from .message import Message


class IWebhookListener:
    """Specifies the interface of webhook listener implementations."""
    handles: list = []

    @classmethod
    def can_handle(cls, request: Request, message: Message) -> bool:
        """Return a boolean indicating if the listener can handle the given
        message.
        """
        return bool(wildcard.matches(
            cls.handles,
            {f'{message.api_version}.{message.kind}'}
        ))

    async def handle(self, *args, **kwargs):
        raise NotImplementedError
