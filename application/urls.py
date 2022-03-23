import imp
import handlers.users.urls
import handlers.authority.urls
import handlers.global_settings.urls

urlpatterns = []
urlpatterns += handlers.users.urls.urlpatterns
urlpatterns += handlers.authority.urls.urlpatterns
urlpatterns += handlers.global_settings.urls.urlpatterns
