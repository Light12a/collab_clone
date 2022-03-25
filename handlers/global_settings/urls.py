from .handlers import SettingListHandler, SettingUpdateHandler

urlpatterns = [
    ('setting/get', SettingListHandler),
    ('setting/update', SettingUpdateHandler)
]