from .handlers import (RealtimeReportCreateHandler, RealtimeReportDeleteHandler,
                       RealtimeReportGetHandler, RealtimeReportSearchHandler, RealtimeReportUpdateHandler,RealtimeReportListGetHandler)

urlpatterns = [
    (r'/real-report/search', RealtimeReportSearchHandler),
    (r'/real-report/get', RealtimeReportGetHandler),
    (r'/real-report/delete', RealtimeReportDeleteHandler),
    (r'/real-report/create', RealtimeReportCreateHandler),
    (r'/real-report/update', RealtimeReportUpdateHandler),
    (r'/real-report/list/get', RealtimeReportListGetHandler),
]
