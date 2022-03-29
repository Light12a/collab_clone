from .handlers import TenantRetrievalHandler

urlpatterns = [
    ('/tenant/search', TenantRetrievalHandler),
]