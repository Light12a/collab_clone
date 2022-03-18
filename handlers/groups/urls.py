from .handlers import (
    GroupSearchHandler,
    GroupDetailHandler,
    GroupCreateHandler,
    GroupDeleteHandler,
    GroupUpdateHandler,
    GetSkillGroupsHandler
)

urlpatterns = [
    ('/group/search', GroupSearchHandler),
    ('/group/get', GroupDetailHandler),
    ('/group/create', GroupCreateHandler),
    ('/group/update', GroupUpdateHandler),
    ('/group/delete', GroupDeleteHandler),
    ('/get_skill_groups', GetSkillGroupsHandler)
]