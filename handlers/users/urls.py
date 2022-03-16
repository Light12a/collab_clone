from .handlers import LoginHandler, LogoutHandler, RefreshTokenHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/refreshtoken', RefreshTokenHandler)
]