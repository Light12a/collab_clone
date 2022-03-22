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


class AnnouncementSearchHandler(BaseHandler):
    
    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

class AnnouncementListGetHandler(BaseHandler):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementGetHandler(BaseHandler):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementDeleteHandler(BaseHandler):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementFileGetHandler(BaseHandler):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementCreateHandler(BaseHandler):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass
    
class AnnouncementUpdateHandler(BaseHandler,ResponseMixin):

    @gen.coroutine    
    def post(self, *args, **kwargs):
        pass




    
 