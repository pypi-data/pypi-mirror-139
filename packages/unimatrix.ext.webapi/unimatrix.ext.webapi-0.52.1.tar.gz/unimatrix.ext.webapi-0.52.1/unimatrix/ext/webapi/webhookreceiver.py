"""Declares :class:`WebhookReceiver`."""
from fastapi import Request
from fastapi.responses import JSONResponse
from unimatrix.lib.datastructures import ImmutableDTO

from .service import Service
from .webhookdispatcher import WebhookDispatcher
from .webhook import Message


class WebhookReceiver(Service):
    """A :class:`~unimatrix.ext.webapi.Service` implementation
    that configures itself to handle webhooks through a single
    entry point, accepting webhooks/events as JSON objects.
    """

    def __init__(self, *args, **kwargs):
        # Remove the URL configuration since we don't need it for
        # now.
        kwargs['urlconf'] = None
        self.dispatcher = WebhookDispatcher(
            handlers=kwargs.pop('handlers', []),
        )
        super().__init__(*args, **kwargs)
        self.add_api_route(
            '/{transport}',
            self.handle,
            name='entrypoint',
            status_code=202,
            tags=['Webhooks'],
            methods=['POST'],
            response_description="Confirmation of the event received."
        )

    async def handle(self,
        request: Request,
        message: Message = Message.inject()
    ) -> JSONResponse:
        """Handles an incoming message."""
        result = await self.dispatcher.dispatch(request, message)
        return JSONResponse(
            content={
                'handlers': [],
                'accepted': True,
                'message': None
            },
            status_code=202
        )
        #return JSONResponse(
        #    content=await self.dispatcher.dispatch(
        #        request=request,
        #        dto=ImmutableDTO.fromdict(await request.json())
        #    ),
        #    status_code=202
        #)
