from .handlers import LoginHandler, LogoutHandler, RefreshTokenHandler, ReleaseLockHandlers
from .handlers import GetUserHandler, GetUserByUsernameHandler, GetUserByPhoneNumberHandler

urlpatterns = [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/refreshtoken', RefreshTokenHandler),
    ('/release', ReleaseLockHandlers)
    ('/get_users', GetUserHandler),
    ('/get_user_by_username', GetUserByUsernameHandler),
    ('/get_user_by_phone_number', GetUserByPhoneNumberHandler)
]
