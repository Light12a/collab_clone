import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from ..users.models import User, Token, Tenant
from .models import SoundFiles
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen
from services.logging import logger as log


log = log.get(__name__)

class GetSelectedRingtoneHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build API for get selected ringtone.
    Params of request is token.
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
            data = self.data_received()
            if 'token' in data:
                check = yield self._check_token_exists(data['token'])
                if check:
                    selected_ringtone = yield self._get_selected_ringtone(data['token'])
                    if selected_ringtone:
                        self.write({
                            "code": 200, 
                            "tone_id": selected_ringtone['sound_id'],
                            "name": selected_ringtone['sound_name'],
                            "url": selected_ringtone['location_path']
                        })
                    else:
                        self.write({"code":404, "errorMessage": "selected ringtone not found"})
                        self.set_status(404)
                else:
                    self.write({"code":401, "errorMessage":"token is wrong"})
                    self.set_status(401)
            else: 
                raise ValueError
        except ValueError:
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Token {} in wrong format"
            log.debug(err.format(data['token']))

    @gen.coroutine
    def _check_token_exists(self, token):
        """
        Function take in token to verify this one is the newest.
        @params: Token.
        """
        result = self.db.query(Token.token_id).filter(Token.token_id==token).distinct().all()

        try:
            raise gen.Return(result[0][0])
        except IndexError:            
            raise gen.Return(False)

    @gen.coroutine
    def _get_selected_ringtone(self, token):
        """
        Meaning: get user's the selected ringtone
        Input: token
        """
        result = self.db.query(SoundFiles).filter(SoundFiles.tenant_id == User.tenant_id,
                                                  User.user_id == Token.user_id,
                                                  Token.token_id == token)
        if result:
            raise gen.Return(result[0].to_json())
        else:
            err = "Not found selected ring tone"
            raise gen.Return(False)


class GetAllRingTonesHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build API for get all ringtone.
    Params of request is token.
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
            data = self.data_received()
            if 'token' in data:
                check = yield self._check_token_exists(data['token'])
                if check:
                    ringtones = yield self._get_all_ringtones()
                    if ringtones:
                        self.write({
                            "code": 200,
                            "ringtones": ringtones
                        })
                    else:
                        self.write({"code":404, "errorMessage": "Ringtones not found"})
                        self.set_status(404)
                else:
                    self.write({"code":401, "errorMessage":"token is wrong"})
                    self.set_status(401)
            else:
                raise ValueError
            
        except ValueError:
            self.set_status(400)
            self.write({"code":400, "errorMessage":"Bad request"})

    @gen.coroutine
    def _get_all_ringtones(self):
        """
        Meaning: get tenant's all ringtones
        Input: token
        """
        results = self.db.query(SoundFiles).all()
        if results:
            results_ = []
            for elemant in results:
                results_.append(elemant.to_json())
            
            ringtones = [{
                "tone_id": element['sound_id'],
                "name": element['sound_name'],
                "url": element['location_path'],
                "selected": "False"
            } for element in results_]
        else:
            err = "Not found any ringtones"
            raise gen.Return(False)
        raise gen.Return(ringtones)
     
    @gen.coroutine
    def _check_token_exists(self, token):
        """
        Function take in token to verify this one is the newest.
        @params: Token.
        """
        result = self.db.query(Token.token_id).filter(Token.token_id==token).distinct().all()

        try:
            raise gen.Return(result[0][0])
        except IndexError:
            raise gen.Return(False)
           
