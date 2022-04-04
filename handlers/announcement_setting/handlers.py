from asyncio.log import logger

from ..base import BaseHandler
from .models import Announcement
from http import HTTPStatus
from tornado import gen, web
from services.logging import logger
from .schema import CREATE_SCHEMA, GET_SCHEMA

LOG = logger.get(__name__)


class AnnouncementSearchHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      pass


class AnnouncementListGetHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      pass


class AnnouncementGetHandler(BaseHandler):

   SCHEMA = GET_SCHEMA

   @web.authenticated
   def post(self):
      announce_id = self.validated_data.get("AnnounceId")
      try:
         announce_id = int(announce_id)
      except ValueError:
         return self.not_found(
            40004, "Announcement with AnnounceId=%s not found" % announce_id)
      query = self.db.query(Announcement).filter(
         Announcement.announce_id == announce_id)
      if (query.count() == 1):
         response_data = self.to_json(query[0])
         return self.created(2001, response_data)
      else:
         return self.not_found(
            40004, "Announcement with AnnounceId=%s not found" % announce_id)


class AnnouncementDeleteHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      pass


class AnnouncementFileGetHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      pass


class AnnouncementCreateHandler(BaseHandler):

   SCHEMA = CREATE_SCHEMA

   @web.authenticated
   def post(self):

      data = Announcement(
         tenant_id=self.validated_data.get("TenantId"),
         announce_name=self.validated_data.get("AnnounceName"),
         summary=self.validated_data.get("Summary"),
         location=self.validated_data.get("FileName"))
      self.db.add(data)
      self.db.commit()
      LOG.info({"user_id": self.validated_data.get("OperationUserId"),
               "api": "announcement/create", "message": "Success"})
      return self.created(2001, self.to_json(data))


class AnnouncementUpdateHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      pass
