from tornado import gen
from handlers.base import BaseHandler
from http import HTTPStatus

class GroupSearchHandler(BaseHandler):													

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        Function is used to search for group information.
        Parameter in request:
        :param  TenantId: "Tenant 1"
        :param  SearchWord:  "Retrieval character string"
        :param  Sort1: "GroupId"
        :param  Sort2: "GroupName"
        :param  Sort3: "AuthId"
        :param  Offset: 0
        :param  Limit: 10
        """
        self.write_response()

class GroupDetailHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        Function is used to get detail for specific group information
        Paramter is required in request:
        :param TenantId: "Tenant01"
        """
        self.write_response()

class GroupDeleteHandler(BaseHandler):
    
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        Function is used to delete a specific group in tenant.
        :param TenantId
        :param GroupId
        :param UserID
        """
        self.write_response()

class GroupCreateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        Function is used to register a new group in a tenant.
        :param TenantId: "TenantId"
        :param GroupId: 1
        :param GroupName: "Group 1"
        :param AuthId: 1
        :param AutoinTime: 1
        """
        self.write_response()

class GroupUpdateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        Function is used to update a specific group in a tenant.
        :param TenantId
        :param UserId
        :param GroupId
        :param GroupName
        :param AuthId
        :param AutoinTime
        """

        self.write_response()