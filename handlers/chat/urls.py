from .handlers import User_RetrievalHandler, User_Status_AcquisitionHandler

urlpatterns = [
    ("/chat/user/search", User_RetrievalHandler),
    ("/chat/user/get", User_Status_AcquisitionHandler)
]