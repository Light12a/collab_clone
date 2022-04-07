from .handlers import (
    GetSkillGroupsHandler,
    GroupSearchHandler,
    GroupDetailHandler,
    GroupCreateHandler,
    GroupDeleteHandler,
    GroupUpdateHandler,
    GroupBulkHandler
)

urlpatterns = [
    ('/group/search', GroupSearchHandler),
    ('/group/get', GroupDetailHandler),
    ('/group/create', GroupCreateHandler),
    ('/group/update', GroupUpdateHandler),
    ('/group/delete', GroupDeleteHandler),
    ('/group/bulk', GroupBulkHandler),
    ('/get_skill_groups', GetSkillGroupsHandler),
]
