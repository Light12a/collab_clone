from .handlers import SmsSettingRetrievalHandler

urlpatterns = [
    ('/sms/search', SmsSettingRetrievalHandler),
]