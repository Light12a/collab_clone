import ari
from utilities.config import config


class CollabosARIConnection(object):
    def __init__(self):
        super(CollabosARIConnection, self).__init__()
        self._ari_connection = None

    @property
    def connection(self):
        if not self._ari_connection:
            self._init_ari_connection()
        return self._ari_connection

    def _init_ari_connection(self):
        self._ari_connection = ari.connect(*[config['ari-client'][key] for key in (
                'url', 'username', 'password')])
