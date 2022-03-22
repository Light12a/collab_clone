import imp
import datetime
import uuid
import json

from sqlalchemy import delete
from ..base import BaseHandler
from .models import TalkScript
from http import HTTPStatus
from utils.config import config
from tornado import gen

class TalkScriptHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        pass

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
    @gen.coroutine
    def put(self):
        pass

    @gen.coroutine
    def delete(self):
        pass

class TalkScriptSearchHandler(BaseHandler):
    @property
    def db(self):
        return self.application.session

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass
    
 