import pandas as pd
import json
from .schema import *
from tornado import gen
from io import StringIO
from .models import Group
from handlers.base import BaseHandler
from handlers.authority.decorators import authorize
from handlers.tenant_settings.models import Tenant
from handlers.authority.models import Authority
from handlers.users.models import User
from http import HTTPStatus
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy import or_, func
from datetime import datetime


class Common:
   def __init__(self, db):
      self.db = db

   def check_tenant_exist(self, tenant_id):
      query = self.db.query(Tenant).filter(
            Tenant.tenant_id == tenant_id).first()
      if query:
         return True
      return False

   def check_group_exist(self, group_id):
      query = self.db.query(Group).filter(Group.group_id == group_id).first()
      if query:
         return True
      return False

   def check_authority_exist(self, auth_id):
      query = self.db.query(Authority).filter(
          Authority.auth_id == auth_id).first()
      if query:
         return True
      return False


class GroupSearchHandler(BaseHandler):
   SCHEMA = SEARCH_SCHEMA

   # @authorize("use_group")
   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to search for group information.
      Parameter in request:
      :param  TenantId: "Tenant 1"
      :param  SearchWord:  "Retrieval character string"
      :param  Sort1: "GroupId"
      :param  Sort2: "GroupName"
      :param  Sort3: "AuthId"
      :param  Offset: 0
      :param  Limit: 10
      """
      tenant_id = self.validated_data.get('TenantId')
      search_word = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

      query = self.db.query(Group).filter(Group.tenant_id == tenant_id, or_(
          Group.group_name.like("%" + search_word + "%"),
          Group.tenant_id.like("%" + search_word + "%")))[offset:limit]

      extensions = yield self.get_affliation_extensions()

      resp = []
      for q in query:
         temp = {}
         temp["GroupId"] = q.group_id
         temp["GroupName"] = q.group_name
         for ex in extensions:
            if q.group_id == ex[0]:
               temp['AffiliationExtension'] = ex[1]
               break
            else:
               temp['AffiliationExtension'] = 0
         temp["AuthId"] = q.auth_id
         temp['AuthName'] = q.authority.auth_name
         temp['AutoinTime'] = q.autoin_time
         temp["UpdateDate"] = q.update_date
         resp.append(temp)
      resp.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      self.write_response(0000, response_data=resp,
                          code=HTTPStatus.OK, message=None)

   @gen.coroutine
   def get_affliation_extensions(self):
      query = self.db.query(User.group_id, func.count(
          User.group_id)).group_by(User.group_id, User.tenant_id).all()
      raise gen.Return(query)


class GroupDetailHandler(BaseHandler):
   SCHEMA = GET_SCHEMA

   @authorize("use_group")
   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to get detail for specific group information
      Paramter is required in request:
      :param TenantId: "Tenant01"
      :param UserId
      :param GroupId
      """
      tenant_id = self.validated_data.get('TenantId')
      group_id = self.validated_data.get("GroupId")
      try:
         group_id = str(group_id)
      except ValueError:
         return self.not_found(
             4009, "Group with GroupId=%s not found" % group_id)
      query = self.db.query(Group).filter(
          Group.group_id == group_id, Group.tenant_id == tenant_id)
      if (query.count() == 1):
         response_data = self.to_json(query[0])
         self.write_response("0000", response_data, code=HTTPStatus.OK)
      else:
         return self.not_found(
             4009, "Group with GroupId=%s not found" % group_id)


class GroupDeleteHandler(BaseHandler):
   SCHEMA = GET_SCHEMA

   @authorize("del_group")
   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to delete a specific group in tenant.
      :param TenantId
      :param GroupId
      :param UserID
      """
      tenant_id = self.validated_data.get('TenantId')
      group_id = self.validated_data.get("GroupId")
      try:
         group_id = str(group_id)
      except ValueError:
         return self.not_found(
             4009, "Group with GroupId=%s not found" % group_id)
      query = self.db.query(Group).filter(
          Group.group_id == group_id, Group.tenant_id == tenant_id)
      if (query.count() == 1):
         try:
            self.db.delete(query[0])
            self.db.commit()
            self.deleted(2000)
         except Exception:
            self.error(
                message="Group with GroupId=%s can not delete" % group_id)
      else:
         self.not_found(
             4009, "Group with GroupId=%s not found" % group_id)


class GroupCreateHandler(BaseHandler):

   SCHEMA = CREATE_SCHEMA

   # @authorize("edit_group")
   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to register a new group in a tenant.
      :param TenantId: "TenantId"
      :param GroupId: 1
      :param GroupName: "Group 1"
      :param AuthId: 1
      :param AutoinTime: 1
      """
      com = Common(self.db)
      group_id = self.validated_data.get("GroupId")
      tenant_id = self.validated_data.get('TenantId')
      auth_id = self.validated_data.get('AuthId')
      check_group = com.check_group_exist(group_id)
      check_tenant = com.check_tenant_exist(tenant_id)
      check_auth = com.check_authority_exist(auth_id)

      if not check_tenant:
         return self.conflict(
             4009, 'Record with TenantId=%s does not exist.' % tenant_id)

      if check_group:
         return self.conflict(
             4009, 'Record with GroupId=%s already exist.' % group_id)

      if not check_auth:
         return self.conflict(
             4009, 'Record with AuthId=%s does not exist.' % auth_id)

      data = Group()
      for k, v in self.validated_data.items():
         setattr(data, CONVERT_FIELDS[k], v)
      data.insert_date = datetime.now()
      data.update_date = datetime.now()
      try:
         self.db.add(data)
         self.db.commit()
      except PendingRollbackError:
         self.db.rollback()
      self.created("0000", response_data=None, message=None)


class GroupUpdateHandler(BaseHandler):
   SCHEMA = PUT_SCHEMA

   @authorize("edit_group")
   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to update a specific group in a tenant.
      :param TenantId
      :param UserId
      :param GroupId
      :param GroupName
      :param AuthId
      :param AutoinTime
      """
      group_id = self.validated_data.get("GroupId")
      try:
         group_id = str(group_id)
      except ValueError:
         return self.not_found(
             4009, "Group with GroupId=%s not found" % group_id)
      query = self.db.query(Group).filter(Group.group_id == group_id)
      if (query.count() == 1):
         data = query[0]
         for k, v in self.validated_data.items():
            setattr(data, CONVERT_FIELDS[k], v)
         data.update_date = datetime.now()
         self.db.add(data)
         self.db.commit()
         return self.created("0000", response_data=None, message=None)
      else:
         return self.not_found(
             4009, "Group with GroupId=%s not found" % group_id)


class GroupBulkHandler(BaseHandler):

   SCHEMA = {}

   # @authorize("edit_group")
   def post(self, *args, **kwargs):
      """
      API is used to register multiple groups in a tenant.
      :param TenantId: "TenantId"
      :param GroupId: 1
      :param GroupName: "Group 1"
      :param AuthId: 1
      :param AutoinTime: 1
      """
      com = Common(self.db)
      name = list(self.request.files.keys())[0]
      file = self.request.files[name][0]
      s = str(file.body, 'utf-8')
      s = StringIO(s)
      df = pd.read_csv(s)
      # # orient records holds a list with one dictionary for each row
      body = df.to_json(orient='records')
      body = json.loads(body)
      for content in body:
         group_id = content.get("GroupId")
         tenant_id = content.get('TenantId')
         auth_id = content.get('AuthId')
         check_group = com.check_group_exist(group_id)
         check_tenant = com.check_tenant_exist(tenant_id)
         check_auth = com.check_authority_exist(auth_id)
         if not check_tenant:
            return self.conflict(
               4009, 'Record with TenantId=%s does not exist.' % tenant_id)

         if check_group:
            return self.conflict(
               4009, 'Record with GroupId=%s already exist.' % group_id)

         if not check_auth:
            return self.conflict(
               4009, 'Record with AuthId=%s does not exist.' % auth_id)

         data = Group()
         for k, v in content.items():
            setattr(data, CONVERT_FIELDS[k], v)
         self.db.add(data)
         self.db.commit()

      self.created("0000", response_data=None, message=None)

