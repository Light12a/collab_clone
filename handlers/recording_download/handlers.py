from handlers.base import BaseHandler
from http import HTTPStatus
from tornado import gen

#API for recording batch download

class RecDownloadCreateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

class RecDownloadListHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

class RecDownloadListFileHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

class RecDownloadCreateFileHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)