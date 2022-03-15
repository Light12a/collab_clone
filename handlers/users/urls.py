from .handlers import LoginHandler, TestHanlder, RegisterHanlder, LogoutHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/register', RegisterHanlder),
    ('/hello', TestHanlder)
]