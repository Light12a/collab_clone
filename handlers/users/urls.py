from .handlers import LoginHandler,\
         LogoutHandler,\
         RefreshTokenHandler, \
         ReleaseLockHandlers,\
         LoginCPMHandler, \
         BroadcastHangdler
         
urlpatterns = [
   ('/login', LoginHandler),
   ('/logout', LogoutHandler),
   ('/refreshtoken', RefreshTokenHandler),
   ('/release', ReleaseLockHandlers),
   ('/user/login', LoginCPMHandler),
   ('/collabos', BroadcastHangdler)
]
