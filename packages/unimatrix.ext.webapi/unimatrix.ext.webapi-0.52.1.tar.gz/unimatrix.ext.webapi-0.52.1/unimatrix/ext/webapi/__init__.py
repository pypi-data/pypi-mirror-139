# pylint: skip-file
import os
import sys

import fastapi
import ioc
from fastapi import Request

from .asgi import Application
from .decorators import action
from .dependency import inject
from .dependency import CurrentEntity
from .exceptions import UpstreamServiceNotAvailable
from .exceptions import UpstreamConnectionFailure
from .keytrustpolicy import KeyTrustPolicy
from .resource import resource
from .resourceendpointset import ResourceEndpointSet
from .resourceendpointset import PublicResourceEndpointSet
from .service import Service
from .webhookreceiver import WebhookReceiver
from .webhook import WebhookListener


__all__ = [
    'action',
    'application_factory',
    'inject',
    'limit',
    'offset',
    'resource',
    'Application',
    'EndpointSet',
    'PublicEndpointSet',
    'Service',
    'UpstreamConnectionFailure',
    'UpstreamServiceNotAvailable',
]

APP_ROLE_CLASSES = {
    'http': Application,
    'service': Service,
    'listener': WebhookReceiver,
}

Endpoint = ResourceEndpointSet
EndpointSet = ResourceEndpointSet
PublicEndpointSet = PublicResourceEndpointSet


def application_factory(role: str = None, *args, **kwargs):
    """Return the appropriate application based on the keyword arguments and
    environment variables.

    Instantiate a :class:`fastapi.FastAPI` implementation based on the `role`
    argument. If `role` is ``None``, then inspect the environment for the
    ``APP_ROLE`` variable, or default to ``'service'``.

    Valid roles are:

    - `http` - A generic HTTP server implementation.
    - `service`  - HTTP service (drone).
    - `listener` - An event listener that receives events through an HTTP
      endpoint (``/``) from a push-based consumer model.
    """
    role = role or os.getenv('APP_ROLE') or 'service'
    return APP_ROLE_CLASSES[role](*args, **kwargs)


def singleton(cls):
    """Class decorator that indicates that a resource is a singleton."""
    cls.singleton = True
    return cls


def get_host(request: Request):
    """Return the client IP address from a :class:`fastapi.Request`
    object.
    """
    host = request.client.host
    if 'CF-Connecting-IP' in request.headers:
        host = request.headers['CF-Connecting-IP']

    # TODO: hack for test client.
    if host == 'testclient':
        host = "127.0.0.1"
    return host


def permission(name: str):
    """Decorate a function to require the given permission `name`."""
    def decorator_factory(func):
        if not hasattr(func, 'permissions'):
            func.permissions = set()
        func.permissions.add(name)
        return func
    return decorator_factory


def policy(tags: list) -> KeyTrustPolicy:
    """Declares a policy for an endpoint to determine which public keys
    it wants to trust.

    Args:
        tags (list): The list of tags that this policy accepts.

    Returns:
        A :class:`KeyTrustPolicy` instance.
    """
    return KeyTrustPolicy(tags)


def offset(default=0):
    """Creates the ``offset`` query parameter for request
    handlers.
    """
    return fastapi.Query(
        default,
        title='offset',
        description=(
            "The number of objects to skip from the beginning "
            "of the result set."
        )
    )


def limit(default=100, limit=None):
    """Creates the ``limit`` query parameter for request
    handlers.
    """
    limit = default * 3
    return fastapi.Query(
        default,
        title='limit',
        description=(
            "Optional limit on the number of objects to include "
            "in the response.\n\n"
            f"The default is {default}, and the maximum is {limit}."
        )
    )
