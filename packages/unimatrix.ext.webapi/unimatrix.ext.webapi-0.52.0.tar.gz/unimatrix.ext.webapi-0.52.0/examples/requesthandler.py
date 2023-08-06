import inspect

import fastapi
import uvicorn

import ioc
from unimatrix.ext import webapi


app = webapi.Service(
    allowed_hosts=['*'],
    enable_debug_endpoints=True
)


class BookRepository:
    DoesNotExist = type('Exception', (Exception,), {})

    async def transfer(self, *args, **kwargs):
        return {'title': "Homerus"}

ioc.provide('BookRepository', BookRepository)


async def f(request: fastapi.Request, foo: int, bar: int, book=webapi.CurrentEntity('BookRepository')):
    raise Exception


import asyncio
import asyncio.coroutines


class SignatureDescriptor:

    def __get__(self, obj, cls):
        return inspect.signature(cls.handle)


class RequestHandler:
    _is_coroutine = asyncio.coroutines._is_coroutine
    __signature__ = SignatureDescriptor()    

    def __init__(self, *args, **kwargs):
        # Check if the asyncio.iscoroutinefunction() call returns
        # True for this object, since it depends on a private
        # symbol.
        assert asyncio.iscoroutinefunction(self)
        self.args = args
        self.kwargs = kwargs

    async def handle(self, foo: int):
        return kwargs.get('book')

    async def __call__(self, request: fastapi.Request, *args, **kwargs):
        handler = type(self)(*self.args, **self.kwargs)
        handler.request = request
        return await handler.handle(*args, **kwargs)

app.add_api_route('/{foo:int}', RequestHandler(), methods=['GET','POST'])


if __name__ == '__main__':
    uvicorn.run(app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )
