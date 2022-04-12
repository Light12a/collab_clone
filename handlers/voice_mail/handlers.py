import json
from datetime import datetime

from ..base import BaseHandler
from handlers.authority.decorators import authorize
import tornado.gen
from .models import VoiceMails
from .schema import SEARCH_SCHEMA, GET_SCHEMA, CREATE_SCHEMA, CONVERT_CREATE
from .schema import PUT_SCHEMA, JUDGE_SCHEMA, USER_GET_SCHEMA
from services.logging import logger

LOG = logger.get(__name__)


class VoiceMailCreateHandler(BaseHandler):
   SCHEMA = CREATE_SCHEMA

   @tornado.gen.coroutine
   def post(self):
      for i in ["SaveDate", "IncomingDate"]:
         try:
            datetime.strptime(self.validated_data.get(i), '%Y-%m-%d %H:%M:%S')
         except ValueError:
            raise tornado.gen.Return(
               self.fail("Incorrect data format, "
                         "%s should be YYYY-MM-DD HH:MM:SS" % i))

      data = VoiceMails()
      for k, v in self.validated_data.items():
         setattr(data, CONVERT_CREATE[k], v)
      data.insert_date = datetime.now()
      data.update_date = datetime.now()
      try:
         self.db.add(data)
         self.db.commit()
      except Exception:
         self.db.rollback()
         raise tornado.gen.Return(self.error("Cannot connect to backend."))
      raise tornado.gen.Return(self.created(2001, self.to_json(data)))
