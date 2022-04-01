from .handlers import TenantRetrievalHandler, TenantAcquisitionHandler

urlpatterns = [
    ('/tenant/search', TenantRetrievalHandler),
    ('/tenant/get', TenantAcquisitionHandler),
]
