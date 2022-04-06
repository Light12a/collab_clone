from tornado import gen
from handlers.base import BaseHandler
from http import HTTPStatus
from email.headerregistry import Group
import imp
import datetime
import uuid
import json
import MySQLdb
from sqlalchemy import func
from ..base import BaseHandler
from ..users.models import User, Token, Tenant
from .models import Group
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log

log = log.get(__name__)
class GroupSearchHandler(BaseHandler):													

   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      Function is used to search for group information.
      Parameter in request:
      :param  TenantId: "Tenant 1"
      :param  SearchWord:  "Retrieval character string"
      :param  Sort1: "GroupId"
      :param  Sort2: "GroupName"
      :param  Sort3: "AuthId"
      :param  Offset: 0
      :param  Limit: 10
      """
      self.write_response()

class GroupDetailHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      Function is used to get detail for specific group information
      Paramter is required in request:
      :param TenantId: "Tenant01"
      """
      self.write_response()

class GroupDeleteHandler(BaseHandler):
   
   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      Function is used to delete a specific group in tenant.
      :param TenantId
      :param GroupId
      :param UserID
      """
      self.write_response()

class GroupCreateHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      Function is used to register a new group in a tenant.
      :param TenantId: "TenantId"
      :param GroupId: 1
      :param GroupName: "Group 1"
      :param AuthId: 1
      :param AutoinTime: 1
      """
      self.write_response()

class GroupUpdateHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      Function is used to update a specific group in a tenant.
      :param TenantId
      :param UserId
      :param GroupId
      :param GroupName
      :param AuthId
      :param AutoinTime
      """

      self.write_response()
   
class GetSkillGroupsHandler(BaseHandler):
   # SCHEMA =
       
   @gen.coroutine
   def post(self):

      data = self.validated_data
      if "token" in data: #
         check = yield self._check_token_exists(data['token'])
         if check:
            groups = yield self._get_groups(data['token'])
            self.write_response("0000", code=HTTPStatus.OK, message={
                  "code": 200, 
                  "skill_groups": groups
            })
         else:
            self.write_response("0000", code=HTTPStatus.OK, message="Groups not found.")
      else:#
         self.write_response("4001", code=HTTPStatus.OK, message="Bad request")#

   @gen.coroutine
   def _get_groups(self, token_id):
      results = self.db.query(Group).filter(Group.tenant_id == User.tenant_id,
                                            User.user_id == Token.user_id,
                                            Token.token_id == token_id).all()
      if results:
         results_ = []
         for elemant in results:
            results_.append(self.to_json(elemant))
            
         groups = [{
            "group_id": element['group_id'],
            "name": element['group_name']
         } for element in results_]
      else:
            err = "Not found any group"
            raise gen.Return(False)
      raise gen.Return(groups)

   @gen.coroutine
   def _check_token_exists(self, token):
      """
      Function take in token to verify this one is the newest.
      @params: Token.
      """
      result = self.db.query(Token.token_id).filter(Token.token_id==token).distinct().all()

      try:
            raise gen.Return(result[0][0])
      except IndexError:
            self.write({"code":401, "errorMessage":"token is wrong"})
            self.set_status(401)
            raise gen.Return(False)
