from .handlers import (
    GetNotificationNumbersHandler,
    ApplyNotificationNumberHandler
)

urlpatterns = [
    ('/get_notification_numbers', GetNotificationNumbersHandler),
    ('/apply_notification_number', ApplyNotificationNumberHandler)
]