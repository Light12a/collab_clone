import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from .handlers import SoundFiles, User, Token
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
                check, token = self._check_token_exists(data['token'])
                if check:
                    self._get_selected_ring_tone(token)
            else: raise ValueError
        except ValueError:
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Token {} in wrong format"
            log.debug(err.format(data['token']))

    @gen.coroutine
    def _check_token_exists(self, token):
        """
            Meaning: Checking the token's existence
            Input: token
            Output: False  or
                    True and token
        """
        result = self.db.query(Token.token_id).filter(Token.token_id == token)
        if result == None:
            raise gen.Return(False)
        else:
            raise gen.Return(True, token)

    def _get_selected_ring_tone(self, token):
        """
        "select sound_id, sound_name, location_path from backend.user as u 
        join backend.token as t on u.user_id = t.user_id join 
        backend.sound_files as s on u.tone_id = s.sound_id  where t.token_id = '{}';"
        """
        result = self.db.query(SoundFiles.sound_id, SoundFiles.sound_name, SoundFiles.location_path)\
                .join(Token, Token.user_id == SoundFiles.user_id).join(SoundFiles, User.sound_id == SoundFiles.sound_id)\
                .filter(Token.token_id == token)      
        try:
            resp = {
                "code": 200,
                "tone_id": result[0][0],
                "name": result[0][1],
                "url": result[0][2]
            }
            self.write_response("Success", code = HTTPStatus.OK.value, response_data=resp)
        except:
            resp = {
                "code": 404,
                "errorMessage": "Issue in Code"
            }
            self.write_response("Failure", code = HTTPStatus.NOT_FOUND.value, response_data=resp)
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
                check, token = self._check_token_exists(data['token'])
                if check:
                    self._get_all_ringtones(token)
            else: raise ValueError
        except ValueError:
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Token {} in wrong format"
            log.debug(err.format(data['token']))

    def _get_all_ringtones(self, token):
        """
        select sound_id, sound_name, location_path from backend.user as u join\
        backend.token as t on u.user_id = t.user_id join backend.sound_files as s\
        on u.tone_id = s.sound_id  where t.token_id = '{}';
        """
        try:
            results = self.db.query(SoundFiles).all()
            ringtones = [{"tone_id": result[0][0],
                            "name": result[0][1],
                            "url": result[0][2],
                            "selected": "False"} for result in results] #adjust in database
            respo = {
                "code": 200,
                "ringtones": ringtones
            }
            self.write_response("Success", code = HTTPStatus.OK.value, response_data= respo)
        except ValueError:
            respo = {
                "code": 404,
                "errorMessage": "Issue in Code"
            }
            self.write_response("Failure", code = HTTPStatus.NOT_FOUND.value, response_data=respo)

    @gen.coroutine
    def _check_token_exists(self, token):
        """
            Meaning: Checking the token's existence
            Input: token
            Output: False  or
                    True and token
        """
        result = self.db.query(Token.token_id).filter(Token.token_id == token)
        if result == None:
            raise gen.Return(False)
        else:
            raise gen.Return(True, token)