import imp
import datetime
import uuid
import json
from xml.dom.minidom import Identified

from numpy import where
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
        results = self.db.query(SmsSetting).filter(SmsSetting.setting_name.like(f'%{SearchWord}%'))\
                                           .offset(request['Offset'])\
                                           .limit(request['Limit'])\
                                           .all()
        try:
            results_ = []
            for elemant in results:
                results_.append(elemant.to_json())
            sms = [{
                "SmsSettingId": element['setting_id'],
                "SmsSettingName": element['setting_name'],
                "SmsAuthName": element['sms_auth_id'],
                "UpdateDate": element['update_date']
            } for element in results_]
            raise gen.Return(sms)      
        except IndexError:
            raise gen.Return(False)
            
