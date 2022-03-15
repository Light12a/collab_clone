import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from .models import User, Token
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen,web

class LoginHandler(BaseHandler):
    @property
    def db(self):
        return self.application.session

    @gen.coroutine
    def get(self):
        self.set_secure_cookie("user", "test")
        self.write("Login success.")


# Below is experiment authentication code
# Step to test:
# 1) Access /hello, it will require user to register.
# 2) Access /login, register sucess.
# 3) Access /hello again, now it not block anymore.
# 4) Access /logout, it will clear register's token.
# 5) Access /hello again, now it will require user to register.

class RegisterHanlder(ResponseMixin, BaseHandler):

    @gen.coroutine
    def get(self):
        self.write("You need to register.")


class TestHanlder(BaseHandler):

    @gen.coroutine
    @web.authenticated
    def get(self):
        self.write("Hello, world")


class LogoutHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        self.clear_cookie("user")
        self.write("Logout success.")