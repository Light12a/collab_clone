import handlers.users.urls
import handlers.authority.urls

urlpatterns = []
urlpatterns += handlers.users.urls.urlpatterns
urlpatterns += handlers.authority.urls.urlpatterns