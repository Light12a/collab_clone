import json
from datetime import datetime
from unittest import result

from handlers.authority.schema import CONVERT_CREATE, CREATE_SCHEMA

from ..base import BaseHandler
import tornado.gen
from .models import Tenant
from sqlalchemy import or_
import pandas as pd
from io import StringIO
from .schema import SEARCH_SCHEMA, GET_SCHEMA
from services.logging import logger

LOG = logger.get(__name__)


class Common:
   def __init__(self, db):
      self.db = db

   def check_tenant_exist(self, tenant_id):
      query = self.db.query(Tenant).filter(
         Tenant.tenant_id == tenant_id).first()
      if query:
         return True
      return False


class TenantSearchHandler(BaseHandler):
   """
   This class handles tenant retrieval.
   It accedes to term, the tenant is retrieved, and the result is returned.
   """
   SCHEMA = SEARCH_SCHEMA

   @tornado.gen.coroutine
   def post(self):
      search_word = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "")
      sort2 = self.validated_data.get("Sort2", "")
      sort3 = self.validated_data.get("Sort3", "")

      query = self.db.query(Tenant).filter(or_(
         Tenant.tenant_name.like("%" + search_word + "%"),
         Tenant.tenant_id.like("%" + search_word + "%")))[offset:limit]
      result = []
      for i in query:
         temp = {}
         data = self.to_json(i)
         temp["TenantId"] = data["tenant_id"]
         temp["TenantName"] = data["tenant_name"]
         temp["Identifier"] = data["identifier"]
         temp["ChannelCnt"] = data["channel_cnt"]
         temp["UpdateDate"] = data["update_date"]
         result.append(temp)
      result.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      raise tornado.gen.Return(self.created(2001, result))


class TenantGetHandler(BaseHandler):
   """
   This class handles tenant acquisition.
   Details of specified tenant information are acquired.
   """
   SCHEMA = GET_SCHEMA

   def post(self):
      try:
         tenant_id = self.validated_data.get("TenantId")
      except ValueError:
         return self.not_found(
            40004, "Tenant with tenant_id=%s not found" % tenant_id)
      query = self.db.query(Tenant).filter(Tenant.tenant_id == tenant_id)
      if (query.count() == 1):
         response_data = self.to_json(query[0])
         return self.created(2001, response_data)
      else:
         return self.not_found(
            40004, "Tenant with tenant_id=%s not found" % tenant_id)


class TenantDeleteHandler(BaseHandler):
   """
   This API is used to delete a tenant.
   Params: {
      TenantId
   }
   """
   SCHEMA = GET_SCHEMA

   @tornado.gen.coroutine
   def post(self):
      tenant_id = self.validated_data.get('TenantId')
      try:
         tenant_id = str(tenant_id)
      except ValueError:
         tornado.gen.Return(self.not_found(
            4009, "Tenant with TenantId=%s not found" % tenant_id))
      query = self.db.query(Tenant).filter(
          Tenant.tenant_id == tenant_id)
      if (query.count() == 1):
         try:
            self.db.delete(query[0])
            self.db.commit()
            tornado.gen.Return(self.deleted(2000))
         except Exception:
            self.error(
               message="Tenant with TenantId=%s can not delete" % tenant_id)
      else:
         tornado.gen.Return(self.not_found(
            4009, "Tenant with TenantId=%s not found" % tenant_id))


class TenantCreateHandler(BaseHandler):
   """
   This API is used to register a new tenant.
   Params: {
      TenantId,
      TenantName,
      Identifier,
      ChannelCnt,
      UseSpeechToText,
      StEngine
   }
   """
   SCHEMA = CREATE_SCHEMA

   def post(self):
      com = Common(self.db)
      tenant_id = self.validated_data.get('TenantId')
      check_tenant = com.check_tenant_exist(tenant_id)

      if check_tenant:
         return self.conflict(
            4009, 'Record with GroupId=%s already exist.' % tenant_id)
      data = Tenant()
      for k, v in self.validated_data.items():
         setattr(data, CONVERT_CREATE[k], v)
      data.insert_date = datetime.now()
      data.update_date = datetime.now()
      self.db.add(data)
      self.db.commit()
      return self.created(2001, self.to_json(data))
