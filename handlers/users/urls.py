from .handlers import LoginHandler, LogoutHandler, RefreshTokenHandler, ReleaseLockHandlers

urlpatterns = [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/refreshtoken', RefreshTokenHandler),
    ('/release', ReleaseLockHandlers)
]
