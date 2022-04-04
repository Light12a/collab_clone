from asyncio.log import logger

from ..base import BaseHandler
from .models import Announcement, Tenant
from http import HTTPStatus
from tornado import gen
from services.logging import logger
from .schema import CREATE_SCHEMA, GET_SCHEMA, CONVERT_FIELDS

LOG = logger.get(__name__)


class AnnouncementSearchHandler(BaseHandler):

   @gen.coroutine
   def post(self):
      pass


class AnnouncementListGetHandler(BaseHandler):

   @gen.coroutine
   def post(self):
      pass


class AnnouncementGetHandler(BaseHandler):

   SCHEMA = GET_SCHEMA

   @gen.coroutine
   def post(self):
      """check tenant existed"""

      tenant_id = self.validated_data.get('TenantId')
      check_tenant = yield self._check_tenant_exist(tenant_id)
      if check_tenant:
         return self.conflict(
               4009, 'Record with TenantId=%s does not exist.' % tenant_id)

      """if tenant exits, we will get announcement"""

      announce_id = self.validated_data.get("AnnounceId")
      try:
         announce_id = int(announce_id)
      except ValueError:
         LOG.info({"api": "announcement/get", "message": "NOT FOUND"})
         return self.not_found(
            40004, "Announcement with AnnounceId=%s not found" % announce_id)
      query = self.db.query(Announcement).filter(
         Announcement.announce_id == announce_id)
      if (query.count() == 1):
         response_data = self.to_json(query[0])
         LOG.info({"api": "announcement/get", "message": "Success"})
         return self.created(2001, response_data)
      else:
         LOG.info({"api": "announcement/get", "message": "NOT FOUND"})
         return self.not_found(
            40004, "Announcement with AnnounceId=%s not found" % announce_id)
   
   @gen.coroutine
   def _check_tenant_exist(self, tenant_id):
      query = self.db.query(Tenant).filter(
         Tenant.tenant_id == tenant_id).first()
      if query:
         raise gen.Return(False)
      raise gen.Return(True)


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

   @gen.coroutine
   def post(self):

      """check tenant existed"""

      tenant_id = self.validated_data.get('TenantId')
      check_tenant = yield self._check_tenant_exist(tenant_id)
      if check_tenant:
         return self.conflict(
               4009, 'Record with TenantId=%s does not exist.' % tenant_id)

      """if tenant exits, we will add announcement"""

      data = Announcement()
      for key, value in self.validated_data.items():
         setattr(data, CONVERT_FIELDS[key], value)
      self.db.add(data)
      self.db.commit()
      LOG.info({"api": "announcement/create", "message": "Success"})
      return self.created(2001, self.to_json(data))

   @gen.coroutine
   def _check_tenant_exist(self, tenant_id):
      query = self.db.query(Tenant).filter(
         Tenant.tenant_id == tenant_id).first()
      if query:
         raise gen.Return(False)
      raise gen.Return(True)


class AnnouncementUpdateHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      pass
