from .handlers import GetSelectedRingtoneHandler, GetAllRingTonesHandler

urlpatterns = [
    ('/get_selected_ringtone', GetSelectedRingtoneHandler),
    ('/get_all_ringtone', GetAllRingTonesHandler)
]