from .handlers import LoginHandler,\
         LogoutHandler,\
         RefreshTokenHandler, \
         ReleaseLockHandlers,\
         LoginCPMHandler, \
         BroadcastHangdler, \
         PasswordChangeHandler
         
urlpatterns = [
   ('/login', LoginHandler),
   ('/logout', LogoutHandler),
   ('/refreshtoken', RefreshTokenHandler),
   ('/release', ReleaseLockHandlers),
   ('/user/login', LoginCPMHandler),
   ('/collabos', BroadcastHangdler),
   ('/user/password/update', PasswordChangeHandler)
]
