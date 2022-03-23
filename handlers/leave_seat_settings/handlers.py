import imp
import datetime
from multiprocessing.sharedctypes import synchronized
from re import U
from unittest import result
from urllib import response
import uuid
import json
import jwt
from ..base import BaseHandler
from .models import Tenant
from handlers.users.models import User, Token
from handlers.leave_seat_settings.models import AuxReasonSetting
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log
from sqlalchemy import inspect

log = log.get(__name__)

class GetAwayReasonHandler(BaseHandler):

    """
        Get aux_reason_settings list
        @params: token
    """
    
    @gen.coroutine
    def post(self):

        data = self.validated_data

        if data:
            if not "token" in data:
                log.error("Json request format is wrong")
                raise gen.Return(
                    self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request"))

            if self._find_token(data['token']):
                username = jwt.decode(data['token'],"secret", algorithms="HS256")

                tenant = yield self._find_tenant(username['id'])

                if tenant:
                    reason_lst = yield self._get_aux_reason(tenant)
                    self.write_response(
                        200, code=HTTPStatus.OK.value, response_data=reason_lst)
                else:
                    log.error("Username: {} is wrong".format())
                    raise gen.Return(
                        self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request"))

        else:
            log.error("Json request format is wrong")
            raise gen.Return(
                self.error(code=HTTPStatus.BAD_REQUEST.value, message="Bad request"))

    @gen.coroutine
    def _find_tenant(self, username):
        """
            Find tenant id to get list aux reason list of this tenant.
            @params: username
        """

        result = self.db.query(User).filter(User.user_name==username).all()

        tenant = self.to_json(result[0])

        try:
            raise gen.Return(tenant['tenant_id'])
        except IndexError:
            raise gen.Return(False)

    @gen.coroutine
    def _get_aux_reason(self, tenant):

        """
            Return dict of aux reason
            @params: tenant id
        """
        result = self.db.query(AuxReasonSetting).filter(AuxReasonSetting.tenant_id==tenant)
        
        reason = self.to_json(result[0])
        
        reason_lst = dict(
            reason1 = reason['reason1_name'],
            reason2 = reason['reason2_name'],
            reason3 = reason['reason3_name'],
            reason4 = reason['reason4_name'],
            reason5 = reason['reason5_name'],
            reason6 = reason['reason6_name'],
            reason7 = reason['reason7_name'],
            reason8 = reason['reason8_name'],
            reason9 = reason['reason9_name'],
            reason10 = reason['reason10_name'],
            reason11 = reason['reason11_name'],
            reason12 = reason['reason12_name'],
            reason13 = reason['reason13_name'],
            reason14 = reason['reason14_name'],
            reason15 = reason['reason15_name'],
        )

        try:
            raise gen.Return(reason_lst)
        except IndexError:
            raise gen.Return(False)

    @gen.coroutine
    def _find_token(self, request):
        result = self.db.query(Token.token_id).filter(Token.token_id==request['token']).all()

        try:
            raise gen.Return(result[0])
        except IndexError:
            raise gen.Return(False)

class GetAuxReasonSettingsGFHandler(BaseHandler):
    """
    
    """
    @gen.coroutine
    def post(self):
        """
            API is to get list aux reasons of tenant
            :param: Tenant id
            :param: userid
        """
        data = self.validated_data
        if not "TenantId" in data and "UserId" in data:
            self.write_response(
                400,code=HTTPStatus.BAD_REQUEST.value, message="Bad request")

        

        self.write_response()
        