from .handlers import (TriggerCreateHandler, TriggerDeleteHandler, TriggerGetHandler,
                       TriggerListGetHandler, TriggerSearchHandler, TriggerUpdateHandler)

urlpatterns = [
    (r'/trigger/search', TriggerSearchHandler),
    (r'/trigger/get', TriggerGetHandler),
    (r'/trigger/delete', TriggerDeleteHandler),
    (r'/trigger/create', TriggerCreateHandler),
    (r'/trigger/update', TriggerUpdateHandler),
    (r'/trigger/list/get', TriggerListGetHandler),
]
