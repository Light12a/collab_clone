import imp
import datetime
import uuid
import json

from sqlalchemy import delete
from ..base import BaseHandler
from .models import TalkScript
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen

class TriggerSearchHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass

class TriggerGetHandler(BaseHandler,ResponseMixin):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerDeleteHandler(BaseHandler,ResponseMixin):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerCreateHandler(BaseHandler,ResponseMixin):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerUpdateHandler(BaseHandler,ResponseMixin):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerListGetHandler(BaseHandler,ResponseMixin):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass
    
 