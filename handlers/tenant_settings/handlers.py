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
from .schema import SEARCH_SCHEMA, GET_SCHEMA, CREATE_SCHEMA, CONVERT_CREATE
from .schema import PUT_SCHEMA, JUDGE_SCHEMA, USER_GET_SCHEMA
from services.logging import logger

LOG = logger.get(__name__)


class TenantSearchHandler(BaseHandler):
   """
   This class handles tenant retrieval.
   It accedes to term, the tenant is retrieved, and the result is returned.
   """
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
         temp["UpdateDate"] = data["update_date"]
         result.append(temp)
      result.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      raise tornado.gen.Return(self.created(2001, result))

class TenantAcquisitionHandler(BaseHandler):
    """
    This class handles tenant acquisition.
    Details of specified tenant information are acquired.
    """
    @property
    def db(self):
        return self.application.session

    def data_received(self, chunk=None):
        if self.request.body:
            return json.loads(bytes.decode(self.request.body))

    @tornado.gen.coroutine
    def post(self):
        try:
            request = self.data_received()
            if ("TenantId" and "OperationUserId") in request:
                tenant = yield self._get_tenant(request)
                if tenant:
                    self.write({
                        "ResultCode": 200,
                        "Message": "Here is the result",
                        "TenantId": tenant['tenant_id'],
                        "TenantName": tenant['tenant_name'],
                        "Identifier": tenant['identifier'],
                        "ChannelCnt": tenant['channel_cnt'],
                        "UseSpeechToText": tenant['use_speech_to_text'],
                        "StEngine": tenant['st_engine']
                    })
                    self.set_status(200)
                else:
                    self.write({"code": 404, "errorMessage": "Tenant not found."})
                    self.set_status(404)
            else:
                raise ValueError
        except ValueError:
            self.set_status(400)
            self.write({"code": 400, "errorMessage": "Bad request"})

    @tornado.gen.coroutine
    def _get_tenant(self, request):
        """
        Get a tenant with tenant_id.
        Param: request
        """
        result = self.db.query(Tenant).filter(Tenant.tenant_id == request['TenantId'])
        try:
            raise tornado.gen.coroutine.Return(result[0].to_json())  
        except IndexError:
            raise tornado.gen.coroutine.Return(False)