from .handlers import (AnnouncementCreateHandler, AnnouncementDeleteHandler, AnnouncementFileGetHandler,
                       AnnouncementGetHandler, AnnouncementListGetHandler, AnnouncementSearchHandler, AnnouncementUpdateHandler)

urlpatterns = [
    (r'/announcement/search', AnnouncementSearchHandler),
    (r'/announcement/get', AnnouncementGetHandler),
    (r'/announcement/delete', AnnouncementDeleteHandler),
    (r'/announcement/file/get', AnnouncementFileGetHandler),
    (r'/announcement/create', AnnouncementCreateHandler),
    (r'/announcement/update', AnnouncementUpdateHandler),
    (r'/announcement/list/get', AnnouncementListGetHandler),
]
