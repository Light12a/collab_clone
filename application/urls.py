import handlers.users.urls
import handlers.authority.urls
import handlers.leave_seat_settings.urls

urlpatterns = []
urlpatterns += handlers.users.urls.urlpatterns
urlpatterns += handlers.authority.urls.urlpatterns
urlpatterns += handlers.leave_seat_settings.urls.urlpatterns
