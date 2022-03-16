import imp
import datetime
import uuid
import json
from ..base import BaseHandler
from .models import User, Token
from http import HTTPStatus
from utils.config import config
from utils.response import ResponseMixin
from tornado import gen

# class LoginHandler(BaseHandler):
#     @property
#     def db(self):
#         return self.application.session

#     @gen.coroutine
#     def get(self):
#         data = self.db.query(User).all()
#         for item in data:
#             print(item.content)

class LoginHandler(ResponseMixin, BaseHandler):

    @property
    def db(self):
        return self.application.session

    def data_received(self, chunk=None):
        if self.request.body:
            return json.loads(self.request.body)

    def post(self):
        data = self.data_received()
        check = self._check_format_json(data)
        if check:
            self._check_token_valid(data)
        else:
            credential = self._user_credential_read(
                tenant_id=data['tenant_id'], username=data['username'])
            if not credential:
                self.write_response(HTTPStatus.FORBIDDEN,
                                    message="username or tenant_id is wrong")
            else:
                password_valid = self._validate_user_password(
                    credential, password=data['password'])
                if not password_valid:
                    self.write_response(
                        HTTPStatus.BAD_REQUEST, message="Password is wrong")
                else:
                    codes, token = self._create_token(credential)
                    resp = {
                        "code": codes,
                        "token": token['token_id']
                    }
                    self.write_response(HTTPStatus.OK, result=resp)

    def _user_credential_read(self, tenant_id, username):
        result = self.db.query(User).filter(
            User.tenant_id == tenant_id, User.user_name == username)
        if result is None:
            return False
        else:
            return result[0]

    def _validate_user_password(self, user_id, password):
        result = self.db.query(User.password).filter(User.user_id == user_id)
        if result[0][0] == password:
            return True

    def _remove_expired_token(self, user_id):
        """
        docstring
        """
        self.db.query(Token).filter(User.user_id == user_id).delete()
        self.db.commit()

    def _create_token(self, user_id):
        params = dict(
            token_id=str(uuid.uuid4()),
            user_id=user_id,
            expiration_time=config['token']['login_expiry'],
            create_time=str(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        )
        self._remove_expired_token(user_id=user_id)
        new_token = Token(params['token_id'], params['user_id'],
                          params['expiration_time'], params['create_time'])
        self.db.add(new_token)
        self.db.commit()

        return 200, params

    def _check_format_json(self, json):
        try:
            token = json['token']
        except KeyError:
            return False
        return True

    def _check_token_valid(self, request):
        result = self.db.query(Token.token_id, Token.expired_date, Token.create_date).join(
            User, User.user_id == Token.user_id).filter(User.tenant_id == request['tenant_id'], User.user_name == request['username'])

        try:
            if result[0][0] == request['token']:
                inf = "Find out token_id is the same with token_id of user: {} in json request"
                check = self._check_valid_token(
                    result[0][2].strftime("%Y-%m-%d %H:%M:%S"), result[0][1])
                if check:
                    self.write_response(HTTPStatus.OK, result={'code': 200})
                else:
                    resp = {
                        "code": 402,
                        "message": "Token is expiried"
                    }
                    self.write_response(HTTPStatus.NOT_FOUND, result=resp)
            else:
                self.write({
                    "code": 405,
                    "message": "Token is wrong"
                })
                self.set_status(405)
        except TypeError:
            self.write({
                "code": 406,
                "message": "username or tenant_id is not existed"
            })
            self.set_status(406)
            err = "Username: {} or tenant_id: {} attached in json request is not existed in db"
