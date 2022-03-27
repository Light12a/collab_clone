from tornado import gen
from handlers.base import BaseHandler
from http import HTTPStatus

#Create API request for call flow setting

class FlowSearchListHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """Call flow retrieval.
        Call flow information is retrieved according to the condition, and the result is returned. 
        :param TenantId
        :param UserId
        :param SearchWord
        :param Sort1
        :param Sort2
        :param Sort3
        :param Offset
        :param Limit
        """
        self.write_response()

class FlowGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """Get a specified Call flow
        The specified call flow detailed setting is acquired. 
        :param TenantId
        :param UserId
        """
        self.write_response()

class FlowDeleteHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """Copy a specific call flow
        The call flow set up information is deleted. 
        :param Tenant
        """

class FlowCopyHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """Delete a specific call flow
        The call flow set up information is deleted. 
        :param Tenant
        """
        self.write_response()

class FlowCreateHandler(BaseHandler):								

    @gen.coroutine
    def post(self, *args, **kwargs):
        """Call flow registration
        The call flow set up information is registered. 
        :param TenantId
        :param OperationUserId
        :param FlowName
        :param Summary
        :param FlowSetting
        """
        self.write_response()

class FlowUpdateHandler(BaseHandler):								

    @gen.coroutine
    def post(self, *args, **kwargs):
        """Call flow registration
        The call flow set up information is registered. 
        :param TenantId
        :param OperationUserId
        :param FlowName
        :param Summary
        :param FlowSetting
        """
        self.write_response()