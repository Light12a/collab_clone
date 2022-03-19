from .handlers import LoginHandler, RefreshTokenHandler, TestHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/refresh_token', RefreshTokenHandler),
    ('/test', TestHandler)
]