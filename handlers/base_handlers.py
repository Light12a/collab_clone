import asyncio
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def initialize(self, **kwargs):
        RequestHandler.initialize(self, **kwargs)
        self._http_client = AsyncHTTPClient()

    async def _async_request(self, url, method='GET', **kwargs):
        request = HTTPRequest(url=url, method=method, **kwargs)
        response = await self._http_client.fetch(request=request)
        return response

    def get_current_user(self):
        """
        Override this method in child class to get the
        authorized Collabos user.
        Access with `self.current_user`.
        """
        return None

    def get(self, *args, **kwargs):
        """ Override this method in derived class. """
        pass

    def post(self, *args, **kwargs):
        """ Override this method in derived class. """
        pass

    async def _body_producer(self, write):
        """
        Override this method in derived class to generate a streaming request.
        The `write` function must be called as new data arrived, example usage is
        to wrap it in a `while` loop.
        HTTPResponse.body and HTTPResponse.buffer will be empty in the final response.
        """
        await write('')

    def _on_chunk_received(self, chunk):
        """
        Override this method to append a chunk response.
        HTTPResponse.headers will be empty in the final response.
        """
        pass

    def _on_header_line_received(self, header_line):
        pass

    def _on_data_received(self, chunk):
        pass
