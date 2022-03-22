import imp
import datetime
import uuid
import json

from sqlalchemy import delete
from ..base import BaseHandler
from .models import (Trigger,TriggerCondition,TriggerContent)
from http import HTTPStatus
from utils.config import config
from tornado import gen

class TriggerSearchHandler(BaseHandler):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass

class TriggerGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerDeleteHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerCreateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerUpdateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class TriggerListGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass
    
 