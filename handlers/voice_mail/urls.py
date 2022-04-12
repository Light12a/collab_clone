from .handlers import VoiceMailCreateHandler


urlpatterns = [
    ('/voice-mail/search', VoiceMailCreateHandler),
    ('/voice-mail/get', VoiceMailCreateHandler),
    ('/voice-mail/delete', VoiceMailCreateHandler),
    ('/voice-mail/create', VoiceMailCreateHandler),
    ('/voice-mail/update', VoiceMailCreateHandler),
    ('/voice-mail/bulk', VoiceMailCreateHandler),
    ('/voice-mail/judgement', VoiceMailCreateHandler),
    ('/voice-mail/user/get', VoiceMailCreateHandler),
]
