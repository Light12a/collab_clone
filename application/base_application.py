import MySQLdb
from tornado.web import Application
from utilities.ari_client import CollabosARIConnection
from utilities.config import config
import MySQLdb


class CollabosBaseApplication(Application):

    def __init__(self, handlers=[], **settings):
        self._ari = CollabosARIConnection()
        self._cookie_secret = ''

        settings.update(self._generate_required_settings())
        handlers += self._generate_required_handlers()

        self.conn = MySQLdb.connect(
            host = config['db']['host'],
            user = config['db']['user'],
            password = config['db']['password'],
            database= config['db']['database'],
            port = int(config['db']['port'])
        )

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

    def _generate_db_settings(self):
        with open(config['db']) as f:
            pass
