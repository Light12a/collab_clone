from .handlers import ApplyCorrespondenceMemoHandler, GetCorrespondenceMemoListHandler

urlpatterns = [
    ('/get_correspondence_memo_list', GetCorrespondenceMemoListHandler)
    ('/apply_correspondence_memo', ApplyCorrespondenceMemoHandler)
]