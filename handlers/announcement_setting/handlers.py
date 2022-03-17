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


class AnnouncementSearchHandler(BaseHandler):
    
    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class AnnouncementListGetHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementGetHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementDeleteHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementFileGetHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementCreateHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementUpdateHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass




    
 