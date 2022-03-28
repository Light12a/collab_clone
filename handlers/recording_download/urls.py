from .handlers import (
    RecDownloadCreateHandler,
    RecDownloadListHandler,
    RecDownloadListFileHandler,
    RecDownloadCreateFileHandler
)

urlpatterns = [
    ('/response-history/recording/archive/create', RecDownloadCreateHandler),
    ('/response-history/recording/archive/get', RecDownloadListHandler),
    ('/response-history/recording/archive/file/get', RecDownloadListFileHandler),
    ('/response-history/recording/archive/make', RecDownloadCreateFileHandler)
]