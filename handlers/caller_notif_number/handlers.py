from handlers.base import BaseHandler
from http import HTTPStatus
from tornado import gen

# Create API for caller notification number

class CallerIdSearchHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        API is used to search caller notification number by conditions.
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

class CallerIdGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        API is used to get a specified caller notification number detailed allocation is acquired. 
        :param TenantId
        :param UserId
        :param CallerNumId
        """
        self.write_response()


class CallerIdUpdateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        API is used to update the caller notification number
        :param TenantId
        :param UserId
        :param UserList
            :subparam UserId
        :param GroupList
            :subparam GroupId
        """
        self.write_response()