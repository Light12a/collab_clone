import imp
from urllib.request import urlretrieve
from .base import CollabosBaseApplication
from .urls import urlpatterns
import os
class SettingsApplication(CollabosBaseApplication):

    #COOKIE_SECRET_PATH = os.path.join(
    #    os.path.dirname(os.path.abspath(__file__)), 'secure_cookie')

    def _generate_required_handlers(self):
        return urlpatterns