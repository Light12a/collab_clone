from .handlers import TenantSearchHandler, TenantAcquisitionHandler

urlpatterns = [
    ('/tenant/search', TenantSearchHandler),
    ('/tenant/get', TenantAcquisitionHandler),
]