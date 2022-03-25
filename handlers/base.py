import asyncio
from copy import deepcopy
import tornado.gen
from tornado.web import HTTPError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import RequestHandler
from utils.response import ResponseMixin
import json
from jsonschema.exceptions import ValidationError
from jsonschema import FormatChecker
from jsonschema import validate
from sqlalchemy import inspect
from services.logging import logger


LOG = logger.get(__name__)


class BaseHandler(RequestHandler, ResponseMixin):
    def initialize(self, **kwargs):
        RequestHandler.initialize(self, **kwargs)
        self._http_client = AsyncHTTPClient()
        self.validated_data = None
        self.schema = None

    async def _async_request(self, url, method='GET', **kwargs):
        request = HTTPRequest(url=url, method=method, **kwargs)
        response = await self._http_client.fetch(request=request)
        return response

    @tornado.gen.coroutine
    def prepare(self):
        """
        Called at the beginning of a request before  `get`/`post`/etc.

        Override this method to perform common initialization regardless
        of the request method.
        """
        super(BaseHandler, self).prepare()
        # Validate incoming request body against.
        # Only POST, PUT and PATCH HTTP methods should have any form of request
        # body.
        data = {}
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            if(len(self.request.files)):
                return
            try:
                data = json.loads(self.request.body or '{}')
            except ValueError:
                raise tornado.gen.Return(
                    self.error('Invalid json in request body.', code=400))
            try:
                schema_to_apply = self.get_local_schema_with_overrides(
                    self.request.method)
                # Validate the data against the schema to apply
                LOG.debug({"schema": schema_to_apply, "data": data})
                validate(data, schema_to_apply, format_checker=FormatChecker())
            except ValidationError as supported_exception:
                e_mssg = supported_exception.message
                if e_mssg.endswith('is too long') and len(e_mssg) > 250:
                    supported_exception.message = (
                        e_mssg[:50] + ' ... ... ... ' + e_mssg[-50:])
                raise self.error(supported_exception.message, code=400)
        if self.request.method == 'GET':
            # Validate incoming arguments.
            pass
        self.validated_data = deepcopy(data)

    @classmethod
    def get_local_schema_with_overrides(cls, request_method):
        # Allow Exception to be thrown. Handled gracefully in request handler
        schema_to_apply = {}
        if (getattr(cls, 'SCHEMA', False)):
            schema_to_apply = deepcopy(cls.SCHEMA)
        if (getattr(cls, 'SCHEMA_OVERRIDES', False)):
            schema_to_apply.update(
                cls.SCHEMA_OVERRIDES.get(request_method, {}))
        return schema_to_apply

    def get_current_user(self):
        """
        Override this method in child class to get the
        authorized Collabos user.
        Access with `self.current_user`.
        """
        return self.get_secure_cookie("user")

    """ Override theses method in derived class. """
    def get(self, *args, **kwargs):
        raise HTTPError(405)

    def post(self, *args, **kwargs):
        raise HTTPError(405)

    def delete(self, *args, **kwargs):
        raise HTTPError(405)

    def patch(self, *args, **kwargs):
        raise HTTPError(405)

    def put(self, *args, **kwargs):
        raise HTTPError(405)

    def options(self, *args, **kwargs):
        raise HTTPError(405)

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

    @property
    def db(self):
        return self.application.session

    def to_json(self, data):
        return {c.key: getattr(data, c.key)
                for c in inspect(data).mapper.column_attrs}

    # def write_error(self, status_code, **kwargs):
    #     self.finish(json.dumps({
    #         'error': {
    #             'code': status_code,
    #             'message': self._reason
    #         }
    #     }))

    # def write_response(self, status_code, result=None, message=None):
    #     self.set_status(status_code)
    #     if result:
    #         self.finish(json.dumps(result))
    #     elif message:
    #         self.finish(json.dumps({
    #             "message": message
    #         }))
    #     elif status_code:
    #         self.set_status(status_code)
    #         self.finish()