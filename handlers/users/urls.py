from .handlers import LoginHandler,\
         LogoutHandler,\
         RefreshTokenHandler, \
         ReleaseLockHandlers,\
         LoginCPMHandler

urlpatterns = [
   ('/login', LoginHandler),
   ('/logout', LogoutHandler),
   ('/refreshtoken', RefreshTokenHandler),
   ('/release', ReleaseLockHandlers),
   ('/user/login', LoginCPMHandler)
]
