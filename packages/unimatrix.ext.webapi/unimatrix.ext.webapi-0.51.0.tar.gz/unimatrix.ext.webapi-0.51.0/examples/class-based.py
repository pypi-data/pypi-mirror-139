# pylint: skip-file
import asyncio
import typing

import pydantic
import uvicorn
import marshmallow

from unimatrix.ext import webapi
from unimatrix.ext.webapi import PublicResourceEndpointSet
from unimatrix.ext.webapi import __unimatrix__ as boot


asyncio.run(boot.on_setup())


app = webapi.Service(
    allowed_hosts=['*'],
    enable_debug_endpoints=True
)


@webapi.resource("books/v1", True)
class Book:
    id: int
    title: str


class BookEndpoints(PublicResourceEndpointSet):
    path_parameter = 'book_id'
    require_authentication = False
    resource_name = 'books'
    resource_class = Book
    group_name = 'Book'

    class singleton_subresource(PublicResourceEndpointSet):
        resource_name = 'singleton'
        singleton = True

        async def replace(self, book_id: int, dto: dict):
            return book_id, dto

    class author_resource(PublicResourceEndpointSet):
        path_parameter = 'author_id'
        require_authentication = False
        resource_name = 'authors'

        class publications_resource(PublicResourceEndpointSet):
            path_parameter = 'publication_id'
            require_authentication = False
            resource_name = 'publications'

            async def index(self):
                pass

            async def retrieve(self, **kwargs):
                return kwargs

        @webapi.action(name='foo', detail=False, methods=['POST'])
        async def non_detail_subresource_action(self, book_id: int):
            pass

        async def purge(self):
            pass

        async def index(self):
            pass

        async def retrieve(self):
            return None

        subresources = [publications_resource]

    subresources = [author_resource, singleton_subresource]

    @webapi.action
    async def index_action(self):
        return "Index Action"

    @webapi.action(detail=True)
    async def detail_action(self, **kwargs):
        return kwargs

    async def apply(self, dto: dict):
        return dto

    async def create(self, dto: dict):
        return dto

    async def destroy(self, book_id: int):
        return book_id

    async def exists(self, book_id: int) -> bool:
        return book_id == 1

    async def index(self) -> Book.List:
        return self.render_to_response(
            [
                {
                    'id': 1,
                    'book_id': 1,
                    'title': "War and Peace"
                },
                {
                    'id': 2,
                    'book_id': 2,
                    'title': "Don Quixote"
                },
            ],
            total_count=99
        )

    async def purge(self):
        return "Destroy all resources under the base path."

    async def replace(self, book_id: str):
        return book_id

    async def retrieve(self, book_id: str) -> Book:
        return self.render_to_response({'book_id': 1, 'id': 1, 'title': "Foo"})

    async def update(self, book_id: str):
        return book_id


BookEndpoints.add_to_router(app, '/books')

if __name__ == '__main__':
    uvicorn.run(app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )
