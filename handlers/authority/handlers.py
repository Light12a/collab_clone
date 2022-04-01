import json
from datetime import datetime

from ..base import BaseHandler
from handlers.authority.decorators import authorize
import tornado.gen
from .models import Authority
from handlers.users.models import User
from sqlalchemy import or_
import pandas as pd
from io import StringIO
from .schema import SEARCH_SCHEMA, GET_SCHEMA, CREATE_SCHEMA, CONVERT_CREATE
from .schema import PUT_SCHEMA, JUDGE_SCHEMA, USER_GET_SCHEMA
from services.logging import logger

LOG = logger.get(__name__)


class AuthoritySearchHandler(BaseHandler):
   SCHEMA = SEARCH_SCHEMA

   @authorize("use_auth")
   @tornado.gen.coroutine
   def post(self):
      search_word = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

      query = self.db.query(Authority).filter(or_(
         Authority.auth_name.like("%" + search_word + "%"),
         Authority.tenant_id.like("%" + search_word + "%")))[offset:limit]
      result = []
      for i in query:
         temp = {}
         data = self.to_json(i)
         temp["AuthId"] = data["auth_id"]
         temp["AuthName"] = data["auth_name"]
         temp["UpdateDate"] = data["update_date"]
         result.append(temp)
      result.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      raise tornado.gen.Return(self.created(2001, result))


class AuthorityGetHandler(BaseHandler):
   SCHEMA = GET_SCHEMA

   @authorize("use_auth")
   def post(self):
      auth_id = self.validated_data.get("AuthId")
      try:
         auth_id = int(auth_id)
      except ValueError:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % auth_id)
      query = self.db.query(Authority).filter(Authority.auth_id == auth_id)
      if (query.count() == 1):
         response_data = self.to_json(query[0])
         return self.created(2001, response_data)
      else:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % auth_id)


class AuthorityDeleteHandler(BaseHandler):
   SCHEMA = GET_SCHEMA

   @authorize("del_auth")
   def post(self):
      auth_id = self.validated_data.get("AuthId")
      try:
         auth_id = int(auth_id)
      except ValueError:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % auth_id)
      query = self.db.query(Authority).filter(Authority.auth_id == auth_id)
      if (query.count() == 1):
         self.db.delete(query[0])
         self.db.commit()
         return self.deleted(2000)
      else:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % auth_id)


class AuthorityCreateHandler(BaseHandler):
   SCHEMA = CREATE_SCHEMA

   @authorize("edit_auth")
   def post(self):
      data = Authority()
      for k, v in self.validated_data.items():
         setattr(data, CONVERT_CREATE[k], v)
      data.insert_date = datetime.now()
      data.update_date = datetime.now()
      self.db.add(data)
      self.db.commit()
      return self.created(2001, self.to_json(data))


class AuthorityUpdateHandler(BaseHandler):
   SCHEMA = PUT_SCHEMA

   @authorize("edit_auth")
   def post(self):
      auth_id = self.validated_data.get("auth_id")
      try:
         auth_id = int(auth_id)
      except ValueError:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % auth_id)
      query = self.db.query(Authority).filter(Authority.auth_id == auth_id)
      if (query.count() == 1):
         data = query[0]
         for k, v in self.validated_data.items():
            setattr(data, CONVERT_CREATE[k], v)
         data.update_date = datetime.now()
         self.db.add(data)
         self.db.commit()
         return self.created(2001, self.to_json(data))
      else:
         return self.not_found(
            40004, "Authority with auth_id=%s not found" % auth_id)


class AuthorityBulkHandler(BaseHandler):
   SCHEMA = {}

   @authorize("edit_auth")
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
               setattr(data, CONVERT_CREATE[k], v)
            self.db.add(data)
            self.db.commit()
      return self.created(2001, body)


class AuthorityJudgementHandler(BaseHandler):
   SCHEMA = JUDGE_SCHEMA

   @authorize("use_auth")
   def post(self):
      user_id = self.validated_data.get("user_id")
      auth_id = self.db.query(User.auth_id).filter(User.user_id == user_id)
      if (auth_id.count() == 1):
         try:
            query = self.db.query(
               getattr(Authority, self.validated_data.get("operation"))).filter(
                  Authority.auth_id == auth_id[0][0])
            if (query.count() == 1):
               response_data = {
                  "user_id": user_id,
                  self.validated_data.get("operation"): query[0][0]
               }
               return self.created(2001, response_data)
         except AttributeError:
            return self.not_found(
               40004,
               "Operation=%s not found" % self.validated_data.get("operation"))
      else:
         return self.not_found(
            40004, "User with user_id=%s not found" % user_id)


class UserAuthorityGetHandler(BaseHandler):
   SCHEMA = USER_GET_SCHEMA

   @authorize("use_auth")
   def post(self):
      user_id = self.validated_data.get("user_id")
      auth_id = self.db.query(User.auth_id).filter(User.user_id == user_id)
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
            40004, "User with user_id=%s not found" % user_id)

