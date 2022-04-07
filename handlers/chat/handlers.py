import datetime

from db import User
from ..base import BaseHandler
from http import HTTPStatus
from utils.config import config
from tornado import gen
from services.logging import logger as log

from ..users.models import User
from .schema import User_Retrieval_SCHEMA, User_Status_Acquisition_SCHEMA

log = log.get(__name__)


class User_RetrievalHandler(BaseHandler):
    """
    It accedes to term, user information is retrieved, and the result is returned. 
    User's status is acquired from the wall board server, and it returns it.

    """
    SCHEMA = User_Retrieval_SCHEMA
    @gen.coroutine
    def post(self):     

        TenantId =self.validated_data.get("TenantId")
        GroupId = self.validated_data.get("GroupId")
        UserName = self.validated_data.get("Username")
        sort1 = self.validated_data.get("Sort1")
        sort2 = self.validated_data.get("Sort2")
        sort3 = self.validated_data.get("Sort3")

       
        if UserName and (not GroupId):
            retrieval_info = yield self._get_retrieval_info_by_UserName(TenantId, UserName, sort1, sort2, sort3)
        elif GroupId and (not UserName):
            retrieval_info = yield self._get_retrieval_info_by_GroupId(TenantId, GroupId, sort1, sort2, sort3)
        else:
            retrieval_info = yield self._get_retrieval_info_by_GroupIdandUserName(TenantId, GroupId, UserName, sort1, sort2, sort3)

        if retrieval_info:
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.OK, response_data= retrieval_info))
        else:
            log.info(" Can not find information ")
            raise gen.Return(self.write_response(
                "1004", code=HTTPStatus.NOT_FOUND, message= "Information not found"))
       
    @gen.coroutine
    def _get_retrieval_info_by_UserName(self, TenantId, UserName, sort1, sort2, sort3):
        """
        This function gets information from database in User tables with condition about TenantId and UserName   
        """
        results = self.db.query(User).filter(User.tenant_id == TenantId, User.user_name == UserName).all()
        
        if results:
            resp = yield self._create_respone_from_queries(results, sort1, sort2, sort3)            
            raise gen.Return(resp)
        else:
            raise gen.Return(None)
          
    @gen.coroutine
    def _get_retrieval_info_by_GroupId(self, TenantId, GroupId, sort1, sort2, sort3):
        """
        This function gets information from database in User tables with condition about TenantId and GroupId 
        """
        results = self.db.query(User).filter(User.tenant_id == TenantId, User.group_id == GroupId).all()
        
        if results:
            resp = yield self._create_respone_from_queries(results, sort1, sort2, sort3)            
            raise gen.Return(resp)
        else:
            raise gen.Return(None)
    
    @gen.coroutine
    def _get_retrieval_info_by_GroupIdandUserName(self, TenantId, GroupId, UserName, sort1, sort2, sort3):
        """
        This function gets information from database in User table with condition about TenantId GroupId and UserName
        """
        results = self.db.query(User).filter(User.tenant_id == TenantId, User.group_id == GroupId, User.user_name == UserName).all()
       
        if results:
            resp = yield self._create_respone_from_queries(results, sort1, sort2, sort3)            
            raise gen.Return(resp)
        else:
            raise gen.Return(None)

    @gen.coroutine
    def _create_respone_from_queries(self, results, sort1, sort2, sort3):
        """
        Create values responding 
        """
        resp = []
        for result in results:
            result = self.to_json(result)      
            resp.append({
                "UserId": result["user_id"],
                "UserName": result["user_name"],
                "Extension": result["extension"],     
                "UserStatus": "Temporary Skip now"      
            }) 
        resp.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
        raise gen.Return(resp)


class User_Status_AcquisitionHandler(BaseHandler):
    """
    User information is acquired for the ID specification. 
    User's status is acquired from the wall board server, and it returns it. 
    
    """
    SCHEMA =  User_Status_Acquisition_SCHEMA
    @gen.coroutine
    def post(self):     
        data = self.validated_data
        TenantId = self.validated_data.get("TenantId")
        UserId = self.validated_data.get("UserId")

        User_Status_info =  yield self._get_user_status(TenantId, UserId)

        if User_Status_info:
            raise gen.Return(self.write_response(
                "0000", code=HTTPStatus.OK, response_data= User_Status_info))
        else:
            log.info(" Can not find information ")
            raise gen.Return(self.write_response(
                "1004", code=HTTPStatus.NOT_FOUND, message= "Information not found"))

    @gen.coroutine
    def _get_user_status(self, TenantId, UserId):
        """
        This function gets information from database in User table with condition about TenantId and UserId
        """

        results = self.db.query(User).filter(User.tenant_id == TenantId, User.user_id == UserId).all()

        if results:
            resp = yield self._create_respone_from_queries(results)            
            raise gen.Return(resp)
        else:
            raise gen.Return(None)
    
    @gen.coroutine
    def _create_respone_from_queries(self, results):
        """
        Create values responding 
        """
        resp = []
        for result in results:
            result = self.to_json(result)      
            resp.append({
                "UserId": result["user_id"],     
                "UserStatus": "Temporary Skip now"      
            }) 
    
        raise gen.Return(resp)