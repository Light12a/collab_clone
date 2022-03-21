import handlers.users.urls
import handlers.sound_settings.urls
import handlers.corresponding_memo.urls

urlpatterns = []
urlpatterns += handlers.users.urls.urlpatterns
urlpatterns += handlers.sound_settings.urls.urlpatterns
urlpatterns += handlers.corresponding_memo.urls.urlpatterns


