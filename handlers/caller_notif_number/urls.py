from .handlers import (
    CallerIdSearchHandler,
    CallerIdGetHandler,
    CallerIdUpdateHandler,
    GetNotificationNumbersHandler,
    ApplyNotificationNumberHandler
)

urlpatterns = [
    ('/caller-id/search', CallerIdSearchHandler),
    ('/caller-id/get', CallerIdGetHandler),
    ('/caller-id/update', CallerIdUpdateHandler),
    ('/get_notification_numbers', GetNotificationNumbersHandler),
    ('/apply_notification_number', ApplyNotificationNumberHandler)
]