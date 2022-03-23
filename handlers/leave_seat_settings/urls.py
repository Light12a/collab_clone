from .handlers import GetAwayReasonHandler

urlpatterns = [
    ('/aux', GetAwayReasonHandler)
]
