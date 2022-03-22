from unicodedata import name
from .handlers import (
    GroupSearchHandler,
    GroupDetailHandler,
    GroupCreateHandler,
    GroupDeleteHandler,
    GroupUpdateHandler
)

urlpatterns = [
    ('/group/search', GroupSearchHandler),
    ('/group/get', GroupDetailHandler),
    ('/group/create', GroupCreateHandler),
    ('/group/update', GroupUpdateHandler),
    ('/group/delete', GroupDeleteHandler)
]