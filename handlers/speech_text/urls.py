from .handlers import NGSearchHandler
from .handlers import FAQSearchHandler
from .handlers import FAQPartnerSearchHandler


urlpatterns = [
    ('/speech-text/ng/search', NGSearchHandler),
    ('/speech-text/faq/search', FAQSearchHandler),
    ('/speech-text/faq-partner/search', FAQPartnerSearchHandler),
    ('/speech-text/ng/get', NGSearchHandler),
    ('/speech-text/faq/get', NGSearchHandler),
    ('/speech-text/faq-partner/get', NGSearchHandler),
    ('/speech-text/ng/delete', NGSearchHandler),
    ('/speech-text/faq/delete', NGSearchHandler),
    ('/speech-text/faq-partner/delete', NGSearchHandler),
    ('/speech-text/ng/create', NGSearchHandler),
    ('/speech-text/ng/update', NGSearchHandler),
    ('/speech-text/ng/list/get', NGSearchHandler),
    ('/speech-text/ng/list/delete', NGSearchHandler),
    ('/speech-text/faq/create', NGSearchHandler),
    ('/speech-text/faq/update', NGSearchHandler),
    ('/speech-text/faq/list/get', NGSearchHandler),
    ('/speech-text/faq/list/delete', NGSearchHandler),
    ('/speech-text/ng/list/create', NGSearchHandler),
    ('/speech-text/ng/list/update', NGSearchHandler),
    ('/speech-text/faq/list/create', NGSearchHandler),
    ('/speech-text/faq/list/update', NGSearchHandler),
    ('/speech-text/faq-partner/create', NGSearchHandler),
    ('/speech-text/faq-partner/update', NGSearchHandler)
]
