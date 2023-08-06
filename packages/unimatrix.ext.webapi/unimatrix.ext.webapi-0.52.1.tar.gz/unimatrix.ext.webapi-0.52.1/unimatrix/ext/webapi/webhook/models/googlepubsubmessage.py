"""Declares :class:`GooglePubSubMessage`."""
import datetime

import pydantic


class GooglePubSubMessage(pydantic.BaseModel):
    message_id: str = pydantic.Field(..., alias='messageId')
    publish_time: datetime.datetime = pydantic.Field(..., alias='publishTime')
    attributes: dict = None
    data: str = None
