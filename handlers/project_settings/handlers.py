from tornado import gen
from handlers.base import BaseHandler
from http import HTTPStatus

class ProjectsRetrievalHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
            API is to search Projects information
            :param TenantId: "tenant01"
            :param UserId: "User01"
            :param SearchWord: ""
            :param Sort1: 
            :param Sort2:
            :param Sort3:
            :param Offset:
            :param Limit:
        """
        data = self.validated_data
        if data is None:
            pass
        
        self.write_response()

class ProjectsAcquisitionHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
            API is to acquisition Business detail information
            :param TenantId:
            :param UserId:
            :param ProjectId:
        """
        data = self.validated_data
        if data is None:
            pass

        self.write_response()

class ProjectsDeletionHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
            API is to delete Business information
            :param TenantId:
            :param UserId:
            :param ProjectId:
        """
        data = self.validated_data
        if data is None:
            pass

        self.write_response()

class ProjectsRegistrationHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
            API is to register new Business information
            :param TenantId
            :param UserId
            :param ProjectName
            :param DialIn
            :param ChennelCnt
            :param FlowID
            :param InRouteNum
            :param Sla
            :param OutFilter
            :param Carrier
            :param MccGw
            :param GlobalDomain
            :param UseSipport
            :param Sipport
            :param UseRtpport
            :param Rtpport
            :param CarrierUser
            :param CarrierPassword
            :param FaqPartnerId
            :param CallerNum
            :param CallerNumName
            :param PrefixNum
            :param ProjectNgwordsList
            :param NgListId
            :param ProjectFaqwordsList
            :param FaqListId
        """
        data = self.validated_data
        if data is None:
            pass

        self.write_response()

class ProjectsUpdateHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
            API is to update Business information
            :param TenantId
            :param UserId
            :param ProjectName
            :param DialIn
            :param ChennelCnt
            :param FlowID
            :param InRouteNum
            :param Sla
            :param OutFilter
            :param Carrier
            :param MccGw
            :param GlobalDomain
            :param UseSipport
            :param Sipport
            :param UseRtpport
            :param Rtpport
            :param CarrierUser
            :param CarrierPassword
            :param FaqPartnerId
            :param CallerNum
            :param CallerNumName
            :param PrefixNum
            :param ProjectNgwordsList
            :param NgListId
            :param ProjectFaqwordsList
            :param FaqListId
        """
        data = self.validated_data
        if data is None:
            pass

        self.write_response()