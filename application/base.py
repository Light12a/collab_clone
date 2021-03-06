import imp
from tornado.web import Application
from sqlalchemy.orm import scoped_session, sessionmaker
from services.database.mysqldb import sql
from utils.config import config


class CollabosBaseApplication(Application):

   def __init__(self, handlers=[], **settings):
      self._cookie_secret = ''
      settings.update(self._generate_required_settings())
      handlers += self._generate_required_handlers()
      self.be = scoped_session(sessionmaker(
         bind=sql.engine['backend'], autocommit=False,
         autoflush=True, expire_on_commit=False))
      self.ast = scoped_session(sessionmaker(
         bind=sql.engine['asterisk'], autocommit=False,
         autoflush=True, expire_on_commit=False))
      Application.__init__(self, handlers=handlers, **settings)

   def _generate_required_handlers(self):
      """ Override me """
      return []

   def _generate_required_settings(self):
      with open(config['application']['cookie_screct_path']) as f:
         self._cookie_secret = f.read().strip()

      return {
          # 'xsrf_cookies': True,
          'cookie_secret': self._cookie_secret
      }
      # return {}
