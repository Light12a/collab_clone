from .handlers import (
    FlowSearchListHandler,
    FlowGetHandler,
    FlowDeleteHandler,
    FlowCopyHandler,
    FlowCreateHandler,
    FlowUpdateHandler
)

urlpatterns = [
    ('/flow/search', FlowSearchListHandler),
    ('/flow/get', FlowGetHandler),
    ('/flow/delete', FlowDeleteHandler),
    ('/flow/copy', FlowCopyHandler),
    ('/flow/create', FlowCreateHandler),
    ('/flow/update', FlowUpdateHandler)
]