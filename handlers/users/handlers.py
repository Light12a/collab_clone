import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from .models import User, Token
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen

class LoginHandler(BaseHandler):
    @property
    def db(self):
        return self.application.session

    @gen.coroutine
    def get(self):
        pass
