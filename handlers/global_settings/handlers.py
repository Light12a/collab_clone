from handlers.base import BaseHandler
from .models import Settings
from http import HTTPStatus
from tornado import gen

# Create API for settings

class SettingListHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        Function is used to setting of the entire tenant acquisition.
        :param TenantId
        """
        self.write_response()

class SettingUpdateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """Function is used to update setting of the tenant."""
        self.write_response