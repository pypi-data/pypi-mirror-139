"""Declares :class:`Message`."""
import fastapi

from .models import GoogleEventArcMessage


class Message:
    """Represents an incoming message. The :class:`Message` object
    abstracts the message content from its underlying transport."""

    @property
    def api_version(self) -> str:
        """Return the message API version, if specified, else
        ``None``.
        """
        return self.__params.get('apiVersion')

    @property
    def kind(self) -> str:
        """Return the message kind, if specified, else ``None``."""
        return self.__params.get('kind')

    @classmethod
    def inject(cls):
        return fastapi.Depends(cls.parse)

    @classmethod
    async def parse(cls, transport: str, dto: dict):
        # TODO: Refactor this to a real mechanism.
        if transport == 'google.cloud.pubsub.topic.v1.messagePublished':
            dto = GoogleEventArcMessage(**dto)
            msg = cls(
                message_id=dto.message.message_id,
                published=int(dto.message.publish_time.timestamp()*1000),
                **dto.message.attributes
            )
        else:
            raise NotImplementedError
        return msg

    def __init__(self, message_id: str, published: int, **params):
        self.__message_id = message_id
        self.__published = published
        self.__params = params
