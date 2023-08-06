"""Declares :class:`GoogleEventArcMessage`."""
import pydantic

from .googlepubsubmessage import GooglePubSubMessage


class GoogleEventArcMessage(pydantic.BaseModel):
    subscription: pydantic.constr(
        regex='^projects/[\-a-z0-9]{6,30}/subscriptions/.*$'
    )

    message: GooglePubSubMessage
