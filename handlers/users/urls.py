from .handlers import LoginHandler, LogoutHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler)
]