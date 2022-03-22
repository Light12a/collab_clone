import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from handlers.users.models import User, Token
from handlers.sound_settings.models import SoundFiles
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
    @gen.coroutine  
    def post(self):
            data = self.data_received()
            if 'token' in data:
                check, token = yield self._check_token_exists(data['token'])
                if check:
                    self._get_selected_ring_tone(data['token'])
                else:
                    self.write_response("Failure", code=HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
           
            else:
                self.write_response("Failure", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
                err = "Token {} in wrong format"
                log.debug(err.format(data['token']))

    @gen.coroutine
    def _check_token_exists(self, token):
        """
            Meaning: Checking the token's existence
            Input: token
        """
        try:
            result = self.db.query(Token.token_id).filter(Token.token_id == token)
            if result[0][0] == token:
                return True, token
            else: return False, None
        except:
            return False, None
           

    def _get_selected_ring_tone(self, token):
        """
        Meaning: get user's the selected ringtone
        Input: token
        """
        result = self.db.query(SoundFiles.sound_id, SoundFiles.sound_name, SoundFiles.location_path)\
                .join(User, User.sound_id == SoundFiles.sound_id).join(Token, Token.user_id == User.user_id)\
                .filter(Token.token_id == token) 
        
        print("query: ", result)     
        try:
            resp = {
                "code": 200,
                "tone_id": result[0][0],    
                "name": result[0][1],
                "url": result[0][2]
            }
            self.write_response("Success", code=HTTPStatus.OK.value, response_data=resp)
        except:
            resp = {
                "code": 404,
                "errorMessage": "Issue in Server"
            }
            self.write_response("Error", code = HTTPStatus.NOT_FOUND.value, response_data=resp)
class GetAllRingTonesHandler(ResponseMixin, BaseHandler):
    """
    This class is created to build API for get all ringtone.
    Params of request is token.
    """

    @gen.coroutine
    def post(self):
        data = self.data_received()
        if 'token' in data:
            check, token = yield self._check_token_exists(data['token'])
            if check:
                self._get_all_ringtones()
            else:
                self.write_response("Failure", code=HTTPStatus.UNAUTHORIZED.value, message="Token is wrong")
        else:
            self.write_response("Error", code=HTTPStatus.BAD_REQUEST.value, message="Bad request")
            err = "Token {} in wrong format"
            log.debug(err.format(data['token']))

    def _get_all_ringtones(self):
        """
        Meaning: get tenant's all ringtones
        Input: token
        """
        try:
            results = self.db.query(SoundFiles.sound_id, SoundFiles.sound_name, SoundFiles.location_path).all()
            ringtones = [{  "tone_id": result[0],
                            "name": result[1],
                            "url": result[2],
                            "selected": "False"     } for result in results] #adjust in database
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
        """
        try:
            result = self.db.query(Token.token_id).filter(Token.token_id == token)
            if result[0][0] == token:
                return True, token
            else: return False, None
        except:
            return False, None
           