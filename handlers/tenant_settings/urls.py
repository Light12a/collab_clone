from .handlers import (TenantSearchHandler,
                       TenantGetHandler,
                       TenantDeleteHandler,
                       TenantCreateHandler)

urlpatterns = [
   ('/tenant/search', TenantSearchHandler),
   ('/tenant/get', TenantGetHandler),
   ('/tenant/delete', TenantDeleteHandler),
   ('/tenant/create', TenantCreateHandler),
]
