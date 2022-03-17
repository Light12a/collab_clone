from .handlers import TalkScriptHandler,TalkScriptSearchHandler

urlpatterns = [
    (r'/talk_scripts/(.+))', TalkScriptHandler),
    (r'/talk_scripts/search', TalkScriptSearchHandler )
]