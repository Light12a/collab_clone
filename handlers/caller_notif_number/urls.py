from .handlers import (
    CallerIdSearchHandler,
    CallerIdGetHandler,
    CallerIdUpdateHandler
)

urlpatterns = [
    ('/caller-id/search', CallerIdSearchHandler),
    ('/caller-id/get', CallerIdGetHandler),
    ('/caller-id/update', CallerIdUpdateHandler)
]