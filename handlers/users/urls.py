from .handlers import ApplyStateHandler, GetUserConfigHandler, LoginHandler, RefreshTokenHandler, TestHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/refresh_token', RefreshTokenHandler),
    ('/test', TestHandler),
    ('/apply_state', ApplyStateHandler),
    ('/get_user_config', GetUserConfigHandler)
]