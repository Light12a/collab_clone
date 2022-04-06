import json
from datetime import datetime
from unittest import result

from ..base import BaseHandler
from handlers.authority.decorators import authorize
import tornado.gen
from .models import Tenant
from sqlalchemy import or_
import pandas as pd
from io import StringIO
from .schema import SEARCH_SCHEMA, GET_SCHEMA
from services.logging import logger

LOG = logger.get(__name__)


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
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

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


class TenantAcquisitionHandler(BaseHandler):
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
