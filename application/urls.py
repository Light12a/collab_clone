import imp
import handlers.users.urls
import handlers.authority.urls
import handlers.global_settings.urls
import handlers.away_reason.urls
import handlers.groups.urls
import handlers.callflow_settings.urls
import handlers.project_settings.urls
import handlers.recording_download.urls
import handlers.caller_notif_number.urls
import handlers.announcement_setting.urls

urlpatterns = []
urlpatterns += handlers.users.urls.urlpatterns
urlpatterns += handlers.authority.urls.urlpatterns
urlpatterns += handlers.global_settings.urls.urlpatterns
urlpatterns += handlers.groups.urls.urlpatterns
urlpatterns += handlers.callflow_settings.urls.urlpatterns
urlpatterns += handlers.project_settings.urls.urlpatterns
urlpatterns += handlers.recording_download.urls.urlpatterns
urlpatterns += handlers.caller_notif_number.urls.urlpatterns
urlpatterns += handlers.announcement_setting.urls.urlpatterns
urlpatterns += handlers.away_reason.urls.urlpatterns
