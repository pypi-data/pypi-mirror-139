"""Declares :class:`WebhookDispatcher`."""
import asyncio
import typing

from fastapi import Request
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import solve_dependencies

from .utils import as_dependant
from .bodyconsumer import BodyConsumer
from .webhook import Message
from .webhook import IWebhookListener


class WebhookDispatcher(BodyConsumer):
    """Dispatches webhook invocations and events to handlers."""

    #: The list of listeners to which incoming (webhook) events
    #: are dispatched.
    handlers: typing.List[IWebhookListener] = []

    def __init__(self, handlers: list = None):
        """Initialize a new :class:`WebhookDispatcher`.

        Args:
            handlers (list): the list of handlers that are matched
                against each event.
        """
        self.handlers = handlers

    async def dispatch(self, request: Request, message: Message) -> None:
        """Collect all handlers for the webhook notification or
        event included in the request body, and run the results.
        """
        futures = []
        for handler in self.get_handlers(request, message):
            futures.append(self.run_handler(request, handler))
        return await asyncio.gather(*futures)

    def get_handlers(self, request: Request, message: Message) -> list:
        """Return the matching handlers for the (webhook) event
        included in the request body.
        """
        return [
            x(message) for x in self.handlers
            if x.can_handle(request, message)
        ]

    async def run_handler(self,
        request: Request,
        handler: IWebhookListener
    ) -> None:
        """Runs the given handler class with the incoming
        event.
        """
        dependant = get_dependant(
            path='/',
            call=as_dependant(handler.handle)
        )
        values, errors, tasks, response, _ = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=None,
            dependency_overrides_provider=None
        )
        result = await dependant.call(**values)
