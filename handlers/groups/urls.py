from .handlers import (
    GroupSearchHandler,
    GroupDetailHandler,
    GroupCreateHandler,
    GroupDeleteHandler,
    GroupUpdateHandler,
    GroupBulkHandler
)

urlpatterns = [
    ('/group/search', GroupSearchHandler),
    ('/group/get', GroupDetailHandler),
    ('/group/create', GroupCreateHandler),
    ('/group/update', GroupUpdateHandler),
    ('/group/delete', GroupDeleteHandler),
    ('/group/bulk', GroupBulkHandler)
]