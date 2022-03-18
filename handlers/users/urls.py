from .handlers import LoginHandler, RefreshTokenHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/refresh_token', RefreshTokenHandler)
]