import json
from datetime import datetime
from copy import deepcopy

from ..base import BaseHandler
from handlers.authority.decorators import authorize
import tornado.gen
from .models import FaqWordLists, FaqWordData
from .models import NgWordLists, NgWordData, FaqPartners
from sqlalchemy import or_

SEARCH_SCHEMA = {
   "type": "object",
   "properties": {
      "SearchWord": {
         "type": "string"
      },
      "Sort1": {
         "type": "string"
      },
      "Sort2": {
         "type": "string"
      },
      "Sort3": {
         "type": "string"
      },
      "Offset": {
         "type": "integer"
      },
      "Limit": {
         "type": "integer"
      }
   },
   "additionalProperties": False,
   "required": ["SearchWord"]
}

GET_SCHEMA = {
   "type": "object",
   "properties": {
      "auth_id": {
         "type": "integer"
      }
   },
   "additionalProperties": False,
   "required": ["auth_id"]
}

# PUT_SCHEMA = deepcopy(CREATE_SCHEMA)
# PUT_SCHEMA["required"] = ["auth_id"]

JUDGE_SCHEMA = {
   "type": "object",
   "properties": {
      "user_id": {
         "type": "string"
      },
      "operation": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["user_id", "operation"]
}

USER_GET_SCHEMA = {
   "type": "object",
   "properties": {
      "user_id": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["user_id"]
}


class NGSearchHandler(BaseHandler):
   SCHEMA = SEARCH_SCHEMA

   @authorize("use_speech")
   @tornado.gen.coroutine
   def post(self):
      search = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

      query = self.db.query(NgWordLists).filter(or_(
         NgWordLists.ng_list_name.like("%" + search + "%"),
         NgWordLists.tenant_id.like("%" + search + "%")))[offset:limit]
      result = []
      for i in query:
         temp = {}
         data = self.to_json(i)
         for i in ["ng_list_id", "ng_list_name", "update_date"]:
            temp[i] = data[i]
         result.append(temp)
      result.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      raise tornado.gen.Return(self.created(2001, result))


class FAQSearchHandler(BaseHandler):
   SCHEMA = SEARCH_SCHEMA

   @authorize("use_speech")
   @tornado.gen.coroutine
   def post(self):
      search = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

      query = self.db.query(FaqWordLists).filter(or_(
         FaqWordLists.faq_list_name.like("%" + search + "%"),
         FaqWordLists.tenant_id.like("%" + search + "%")))[offset:limit]
      result = []
      for i in query:
         temp = {}
         data = self.to_json(i)
         for i in ["faq_list_id", "faq_list_name", "update_date"]:
            temp[i] = data[i]
         result.append(temp)
      result.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      raise tornado.gen.Return(self.created(2001, result))


class FAQPartnerSearchHandler(BaseHandler):
   SCHEMA = SEARCH_SCHEMA

   @authorize("use_speech")
   @tornado.gen.coroutine
   def post(self):
      search = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

      query = self.db.query(FaqPartners).filter(or_(
         FaqPartners.faq_partner_name.like("%" + search + "%"),
         FaqPartners.tenant_id.like("%" + search + "%")))[offset:limit]
      result = []
      for i in query:
         temp = {}
         data = self.to_json(i)
         for i in ["faq_partner_id", "faq_partner_name", "update_date"]:
            temp[i] = data[i]
         result.append(temp)
      result.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      raise tornado.gen.Return(self.created(2001, result))
