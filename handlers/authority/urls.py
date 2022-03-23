from .handlers import AuthorityHandler

urlpatterns = [
    ('/authorize', AuthorityHandler)
]