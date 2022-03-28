import json
from datetime import datetime
from copy import deepcopy

from ..base import BaseHandler
from handlers.authority.decorators import authorize
import tornado.gen
from .models import User, Authority
from sqlalchemy import or_
import pandas as pd
from io import StringIO

CREATE_SCHEMA = {
   "type": "object",
   "properties": {
      "auth_id": {
         "type": "integer"
      },
      "tenant_id": {
         "type": "string"
      },
      "auth_name": {
         "type": "string"
      },
      "use_monitor": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "use_address": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_address": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_address": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_address": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_address": {
         "type": "integer"
      },
      "use_responding": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_responding": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_responding": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_responding": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_responding": {
         "type": "integer"
      },
      "use_message": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_message": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_message": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_message": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_message": {
         "type": "integer"
      },
      "edit_dashboard": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_dashboard": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_dashboard": {
         "type": "integer"
      },
      "use_report": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_report": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_report": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_report": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_report": {
         "type": "integer"
      },
      "use_user": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_user": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_user": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_user": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_user": {
         "type": "integer"
      },
      "use_group": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_group": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_group": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_group": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_group": {
         "type": "integer"
      },
      "use_auth": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_auth": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_auth": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_auth": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "use_flow": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_flow": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_flow": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "use_seat": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_seat": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_seat": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_seat": {
         "type": "integer"
      },
      "use_chat": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "scope_chat": {
         "type": "integer"
      },
      "use_speech": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_speech": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_speech": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "use_trigger": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_trigger": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "del_trigger": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "use_config": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "edit_config": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "use_log": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      },
      "dl_log": {
         "type": "integer",
         "enum": [
            0,
            1
         ]
      }
   },
   "additionalProperties": False,
   "required": ["auth_id",
                "tenant_id",
                "auth_name",
                "use_monitor",
                "use_address",
                "edit_address",
                "dl_address",
                "del_address",
                "scope_address",
                "use_responding",
                "edit_responding",
                "dl_responding",
                "del_responding",
                "scope_responding",
                "use_message",
                "edit_message",
                "dl_message",
                "del_message",
                "scope_message",
                "edit_dashboard",
                "del_dashboard",
                "scope_dashboard",
                "use_report",
                "edit_report",
                "dl_report",
                "del_report",
                "scope_report",
                "use_user",
                "edit_user",
                "dl_user",
                "del_user",
                "scope_user",
                "use_group",
                "edit_group",
                "dl_group",
                "del_group",
                "scope_group",
                "use_auth",
                "edit_auth",
                "dl_auth",
                "del_auth",
                "use_flow",
                "edit_flow",
                "del_flow",
                "use_seat",
                "edit_seat",
                "del_seat",
                "scope_seat",
                "use_chat",
                "scope_chat",
                "use_speech",
                "edit_speech",
                "del_speech",
                "use_trigger",
                "edit_trigger",
                "del_trigger",
                "use_config",
                "edit_config",
                "use_log",
                "dl_log"]
}

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

PUT_SCHEMA = deepcopy(CREATE_SCHEMA)
PUT_SCHEMA["required"] = ["auth_id"]

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


class AuthoritySearchHandler(BaseHandler):
   SCHEMA = SEARCH_SCHEMA

   @authorize("use_auth")
   @tornado.gen.coroutine
   def post(self):
      search = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

      query = self.db.query(Authority).filter(or_(
         Authority.auth_name.like("%" + search + "%"),
         Authority.tenant_id.like("%" + search + "%")))[offset:limit]
      result = []
      for i in query:
         temp = {}
         data = self.to_json(i)
         for i in ["auth_id", "auth_name", "update_date"]:
            temp[i] = data[i]
         result.append(temp)
      result.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      raise tornado.gen.Return(self.created(2001, result))


class AuthorityGetHandler(BaseHandler):
   SCHEMA = GET_SCHEMA

   @authorize("use_auth")
   def post(self):
      value = self.validated_data.get("auth_id")
      try:
         value = int(value)
      except ValueError:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % value)
      query = self.db.query(Authority).filter(Authority.auth_id == value)
      if (query.count() == 1):
         response_data = self.to_json(query[0])
         return self.created(2001, response_data)
      else:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % value)


class AuthorityDeleteHandler(BaseHandler):
   SCHEMA = GET_SCHEMA

   @authorize("del_auth")
   def post(self):
      value = self.validated_data.get("auth_id")
      try:
         value = int(value)
      except ValueError:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % value)
      query = self.db.query(Authority).filter(Authority.auth_id == value)
      if (query.count() == 1):
         self.db.delete(query[0])
         self.db.commit()
         return self.deleted(2000)
      else:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % value)


class AuthorityCreateHandler(BaseHandler):
   SCHEMA = CREATE_SCHEMA

   @authorize("use_auth")
   def post(self):
      value = self.validated_data.get("auth_id")
      try:
         value = int(value)
      except ValueError:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % value)
      query = self.db.query(Authority).filter(Authority.auth_id == value)
      if (query.count() > 0):
         return self.conflict(
            4009, 'Record with auth_id=%s already exist.' % value)
      else:
         data = Authority()
         for k, v in self.validated_data.items():
            setattr(data, k, v)
         self.db.add(data)
         self.db.commit()
         return self.created(2001, self.to_json(data))


class AuthorityUpdateHandler(BaseHandler):
   SCHEMA = PUT_SCHEMA

   @authorize("edit_auth")
   def post(self):
      value = self.validated_data.get("auth_id")
      try:
         value = int(value)
      except ValueError:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % value)
      query = self.db.query(Authority).filter(Authority.auth_id == value)
      if (query.count() == 1):
         data = query[0]
         for k, v in self.validated_data.items():
            setattr(data, k, v)
         data.update_date = datetime.now()
         self.db.add(data)
         self.db.commit()
         return self.created(2001, self.to_json(data))
      else:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % value)


class AuthorityBulkHandler(BaseHandler):
   SCHEMA = {}

   @authorize("use_auth")
   def post(self):
      # pass
      name = list(self.request.files.keys())[0]
      file = self.request.files[name][0]
      s = str(file.body, 'utf-8')
      s = StringIO(s)
      df = pd.read_csv(s)
      body = df.to_json(orient='records')
      body = json.loads(body)
      for content in body:
         value = content.get("auth_id")
         try:
            value = int(value)
         except ValueError:
            return self.not_found(
               40004, "Authority with auth_id=%s not found" % value)
         query = self.db.query(Authority).filter(Authority.auth_id == value)
         if (query.count() > 0):
            return self.conflict(
               4009, 'Record with auth_id=%s already exist.' % value)
         else:
            data = Authority()
            for k, v in content.items():
               setattr(data, k, v)
            self.db.add(data)
            self.db.commit()
      return self.created(2001, body)


class AuthorityJudgementHandler(BaseHandler):
   SCHEMA = JUDGE_SCHEMA

   @authorize("use_auth")
   def post(self):
      value = self.validated_data.get("user_id")
      auth_id = self.db.query(User.auth_id).filter(User.user_id == value)
      if (auth_id.count() == 1):
         try:
            query = self.db.query(
               getattr(Authority, self.validated_data.get("operation"))).filter(
                  Authority.auth_id == auth_id[0][0])
            if (query.count() == 1):
               response_data = {
                  "user_id": value,
                  self.validated_data.get("operation"): query[0][0]
               }
               return self.created(2001, response_data)
         except AttributeError:
            return self.not_found(
               40004,
               "Operation=%s not found" % self.validated_data.get("operation"))
      else:
         return self.not_found(
            40004, "User with user_id=%s not found" % value)


class UserAuthorityGetHandler(BaseHandler):
   SCHEMA = USER_GET_SCHEMA

   @authorize("use_auth")
   def post(self):
      value = self.validated_data.get("user_id")
      auth_id = self.db.query(User.auth_id).filter(User.user_id == value)
      if (auth_id.count() == 1):
         query = self.db.query(Authority).filter(
               Authority.auth_id == auth_id[0][0])
         if (auth_id.count() == 1):
            return self.created(2001, self.to_json(query[0]))
         else:
            return self.not_found(
               40004, "Authority with auth_id=%s not found" % auth_id[0][0])
      else:
         return self.not_found(
            40004, "User with user_id=%s not found" % value)
