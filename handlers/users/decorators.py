from handlers.base import BaseHandler
from .models import Token
import jwt
from functools import wraps
from http import HTTPStatus


def token_required(func):
   @wraps(func)
   def decorated(*args, **kwargs):
      request = args[0]
      if not isinstance(request, BaseHandler):
         return request.error('Cannot Process Request')

      token = request.get_current_user()

      if not token:
         return request.write_response("0005", code=HTTPStatus.UNAUTHORIZED)
      try:
         data = jwt.decode(token, "secret", algorithms='HS256')
         user_id = request.db.query(Token).filter(
             Token.user_id == data['id'])
         if not user_id:
            return request.write_response("0005", code=HTTPStatus.UNAUTHORIZED)
      except:
         return request.error('Cannot Process Request')
      return func(*args, **kwargs)

   return decorated
