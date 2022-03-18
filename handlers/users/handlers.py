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
        self.set_secure_cookie("user", "85a55880-a85b-4515-a89f-a263fd1c07ce")
        self.write("85a55880-a85b-4515-a89f-a263fd1c07ce")

        # self.set_secure_cookie("user", "092HK3399p@3")
        # self.write("092HK3399p@3")


class LogoutHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        self.clear_cookie("user")
        self.write("Logout")
