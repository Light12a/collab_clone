from .handlers import AuthoritySearchHandler
from .handlers import AuthorityGetHandler
from .handlers import AuthorityDeleteHandler
from .handlers import AuthorityCreateHandler
from .handlers import AuthorityUpdateHandler
from .handlers import AuthorityBulkHandler
from .handlers import AuthorityJudgementHandler
from .handlers import UserAuthorityGetHandler

urlpatterns = [
    ('/authority/search', AuthoritySearchHandler),
    ('/authority/get', AuthorityGetHandler),
    ('/authority/delete', AuthorityDeleteHandler),
    ('/authority/create', AuthorityCreateHandler),
    ('/authority/update', AuthorityUpdateHandler),
    ('/authority/bulk', AuthorityBulkHandler),
    ('/authority/judgement', AuthorityJudgementHandler),
    ('/authority/user/get', UserAuthorityGetHandler),
]
