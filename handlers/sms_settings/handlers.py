import imp
import datetime
import uuid
import json
from xml.dom.minidom import Identified
from numpy import where
from handlers.sms_authenticators.models import SmsAuthenticator
from ..base import BaseHandler
from .models import SmsSetting
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen

class SmsSettingRetrievalHandler(BaseHandler):
    """
    This class handles SMS setting retrieval.
    It accedes to term, the SMS set up information is retrieved, and the result is returned.
    """
    @property
    def db(self):
        return self.application.session
    
    def data_received(self, chunk=None):
        if self.request.body:
            return json.loads(bytes.decode(self.request.body))
    
    @gen.coroutine
    def post(self):
        try:
            request = self.data_received()
            if ("TenantId" and "OperationUserId" and "SearchWord") in request:
                sms = yield self._get_sms(request)
                if sms:
                    self.write({
                        "ResultCode": 200,
                        "Message": "Here is the result",
                        "DataList": sms
                    })
                    self.set_status(200)
                else:
                    self.write({"code":404, "errorMessage": "No matching results were found."})
                    self.set_status(404)
            else:
                raise ValueError
        except ValueError:
            self.set_status(400)
            self.write({"code":400, "errorMessage":"Bad request"})

    @gen.coroutine
    def _get_sms(self, request):
        """
        Search SMS setting with conditions.
        Param: request
        """  
        SearchWord = request['SearchWord']
        query_sms = self.db.query(SmsSetting.setting_id, 
                                  SmsSetting.setting_name, 
                                  SmsAuthenticator.sms_auth_name,
                                  SmsSetting.update_date)\
                           .filter(SmsSetting.sms_auth_id == SmsAuthenticator.sms_auth_id,
                                   SmsSetting.setting_name.like(f'%{SearchWord}%'))\
                           .offset(request['Offset'])\
                           .limit(request['Limit'])\
                           .all()
        try:
            sms = [{
                "SmsSettingId": result[0],
                "SmsSettingName": result[1],
                "SmsAuthName": result[2],
                "UpdateDate": result[3]
            } for result in query_sms] 
            raise gen.Return(sms)      
        except IndexError:
            raise gen.Return(False)

