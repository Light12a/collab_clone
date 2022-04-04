<<<<<<< HEAD
from .handlers import LoginHandler, LogoutHandler, RefreshTokenHandler, ReleaseLockHandlers
=======
from .handlers import LoginHandler, LogoutHandler
from .handlers import GetUserByUsernameHandler, GetUserHandler
>>>>>>> 3ac182e... convert APIs

urlpatterns = [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
<<<<<<< HEAD
    ('/refreshtoken', RefreshTokenHandler),
    ('/release', ReleaseLockHandlers)
]
=======
    ('/get_users', GetUserHandler),
    ('/get_user_by_username', GetUserByUsernameHandler)
]
>>>>>>> 3ac182e... convert APIs
