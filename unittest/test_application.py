import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from application import base_application
from Hrp import Hrp
import test_handlers
from tornado.web import URLSpec


class TestApplication(base_application.CollabosBaseApplication):
    COOKIE_SECRET_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'secure_cookie')

    @property
    def hrp(self):
        if not ('_hrp' in self.__dict__ and self._hrp):
            self._prepare_hrp_connection()
        return self._hrp

    def _generate_required_handlers(self):
        return [
            URLSpec('/upload', test_handlers.UploadHandler, name='upload'),
            ('/proxy', test_handlers.ProxyHandler),
            ('/api/get/(\d+)', test_handlers.TestGetAPIHandler),
            ('/api/post', test_handlers.TestPostAPIHandler),
            ('/api/ami', test_handlers.AmiWSHandler),
            ('/login', test_handlers.LoginHandler),
            ('/logout', test_handlers.LogoutHandler),
            ('/get_user', test_handlers.GetUserHandler)

        ]

    def _prepare_hrp_connection(self):
        server_url = 'https://acp-api.amivoice.com/v1/recognize'
        grammar_file = '-a-general'
        encoding = '16K'
        with open('appkey') as f:
            appkey = f.read().strip()
        self._hrp = Hrp.construct()
        self._hrp.setServerURL(server_url)
        self._hrp.setCodec(encoding)
        self._hrp.setGrammarFileNames(grammar_file)
        self._hrp.setAuthorization(appkey or '')
        os.environ['SSL_CERT_FILE'] = os.path.join(os.path.abspath('.'), 'curl-ca-bundle.crt')
        try:
            if not (self._hrp.connect() and self._hrp.feedDataResume()):
                print(self._hrp.getLastMessage())
                self._hrp = None
        except:
            print('Got hrp error')
            self._hrp = None


