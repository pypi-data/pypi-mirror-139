"""Declares :class:`BodyConsumer`."""
import typing

from fastapi import Request

from .exceptions import ParseError
from .negotiation import DefaultContentNegotiation
from .negotiation import IContentNegotiation
from .parsers import IParser
from .parsers import JSONParser


class BodyConsumer:
    """Mixin class that provides an interface to consume the body of an
    HTTP request.
    """
    #: The content negiotiation procedure. Subclasses may override
    #: this attribute to provide their own implementation.
    #: See also :class:`~unimatrix.ext.webapi.negotiation.IContentNegotiation`.
    negotiator: IContentNegotiation = DefaultContentNegotiation()

    #: The list of request body parsers in order of preference.
    parsers: typing.List[IParser] = []

    #: Default parsers for the specific :class:`BodyConsumer`
    #: implementations.
    default_parsers: typing.List[IParser] = [
        JSONParser
    ]

    async def get_body(self, request: Request = None) -> typing.Any:
        """Parse and return the request body."""
        # Do not parse the body for methods that do not commonly use them.
        #
        #   HTTP request bodies are theoretically allowed for all methods
        #   except TRACE, however they are not commonly used except in PUT,
        #   POST and PATCH. Because of this, they may not be supported properly
        #   by some client frameworks, and you should not allow request bodies
        #   for GET, DELETE, TRACE, OPTIONS and HEAD methods.
        #
        # (from OpenStack API Special Interest Group documentation)
        request = request or self.request
        if request.method in {"GET", "HEAD", "TRACE", "OPTIONS", "DELETE"}:
            return None
        media_type = request.headers.get('Content-Type')
        content_length = request.headers.get('Content-Length') or ''
        if not str.isdigit(content_length) or int(content_length) == 0:
            return None
        parser = self.negotiator.select_parser(request, self.get_parsers())
        if parser is None:
            raise ParseError
        return await parser.parse(request, media_type)

    def get_parsers(self) -> typing.List[IParser]:
        """Return the list of parsers used to deserialize the request body."""
        return self.parsers + self.default_parsers
