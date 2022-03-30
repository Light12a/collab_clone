from services.logging import logger
from .models import Authority
from handlers.users.models import Token, User
from ..base import BaseHandler

LOG = logger.get(__name__)


def query_db(request_handler, query, filter, value):
   query = request_handler.db.query(query).filter(filter == value)
   if(query.count() == 1):
      return query[0][0]
   raise request_handler.error('Cannot Process Request')


def authorize(action):
   """
   Authorize decorator used to enforce authorization permissions
   defined in the API policy.

   :param action: api action:verb string
   """

   def function_wrapper(function):
      def wrapper(*args, **kwargs):
         request_handler = args[0]
         if isinstance(request_handler, BaseHandler):
            if (request_handler.get_current_user() is None):
               return request_handler.unauthorized()

            user_id = query_db(request_handler, getattr(Token, 'user_id'),
                               getattr(Token, 'token_id'),
                               request_handler.get_current_user())

            auth_id = query_db(request_handler, getattr(User, 'auth_id'),
                               getattr(User, 'user_id'), user_id)

            value = query_db(request_handler, getattr(Authority, action),
                             getattr(Authority, 'auth_id'), auth_id)
            if(not bool(value)):
               return request_handler.forbidden()
            return function(*args, **kwargs)
         else:
            raise request_handler.error('Cannot Process Request')
      return wrapper
   return function_wrapper
