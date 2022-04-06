from .handlers import TenantSearchHandler, TenantGetHandler

urlpatterns = [
    ('/tenant/search', TenantSearchHandler),
    ('/tenant/get', TenantGetHandler),
]