from .handlers import (ProjectsAcquisitionHandler,
                        ProjectsRetrievalHandler,
                        ProjectsRegistrationHandler,
                        ProjectsDeletionHandler, 
                        ProjectsUpdateHandler)

urlpatterns = [('/project/update', ProjectsUpdateHandler),
                ('/project/create', ProjectsRegistrationHandler),
                ('/project/detele', ProjectsDeletionHandler),
                ('/project/get', ProjectsAcquisitionHandler),
                ('/project/search', ProjectsRetrievalHandler)
]
                    