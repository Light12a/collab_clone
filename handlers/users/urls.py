from .handlers import LoginHandler, LogoutHandler, ApplyStateHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/apply_state', ApplyStateHandler)
]