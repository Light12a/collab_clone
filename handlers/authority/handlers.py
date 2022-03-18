from ..base import BaseHandler
from handlers.authority.decorators import authorize
from utils.response import ResponseMixin
from tornado import gen
from db import Token, User


class AuthorityHandler(BaseHandler):

   @authorize("use_auth")
   @gen.coroutine
   def get(self):
      self.write('Get Authorize.')
