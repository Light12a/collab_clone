 
from .handlers import (HistoricalReportSearchHandler, HistoricalReportCreateHandler, HistoricalReportDeleteHandler, HistoricalReportGetHandler, HistoricalReportListGetHandler,
                       HistoricalReportTabulatedCSVHandler, HistoricalReportTabulatedGetHandler, HistoricalReportUpdateHandler, HistoricalReportViewCallCenterHandler)

urlpatterns = [
    (r'/hist-report/search', HistoricalReportSearchHandler),
    (r'/hist-report/get', HistoricalReportGetHandler),
    (r'/hist-report/delete', HistoricalReportDeleteHandler),
    (r'/hist-report/create', HistoricalReportCreateHandler),
    (r'/hist-report/update', HistoricalReportUpdateHandler),
    (r'/hist-report/tabulated/get', HistoricalReportTabulatedGetHandler),
    (r'/hist-report/tabulated/csv', HistoricalReportTabulatedCSVHandler),
    (r'/hist-report/list/get', HistoricalReportListGetHandler),
]