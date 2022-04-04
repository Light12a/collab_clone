from asyncio.log import logger
import imp
from urllib import request
import json

from sqlalchemy import delete
from ..base import BaseHandler
from .models import Announcement
from http import HTTPStatus
from utils.config import config
from tornado import gen, web
from services.logging import logger
from .schema import CREATE_SCHEMA

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

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


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
    def post(self, *args, **kwargs):

        data = Announcement(tenant_id=self.validated_data.get("TenantId"),
                            announce_name=self.validated_data.get(
                                "AnnounceName"),
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
