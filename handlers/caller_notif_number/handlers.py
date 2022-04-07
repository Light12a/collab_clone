from operator import or_
from .models import CallerId, CallerIdGroup, CallerIdUser
from handlers.project_settings.models import Project
from handlers.asterisk.models import PsEndpoint
from handlers.base import BaseHandler
from http import HTTPStatus
from tornado import gen
from .schemas import *
from sqlalchemy import or_, func

# Create API for caller notification number


class CallerIdSearchHandler(BaseHandler):
   SCHEMA = SEARCH_SCHEMA

   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to search caller notification number by conditions.
      :param TenantId
      :param UserId
      :param SearchWord
      :param Sort1
      :param Sort2
      :param Sort3
      :param Offset
      :param Limit
      """
      tenant_id = self.validated_data.get('TenantId')
      search_word = self.validated_data.get("SearchWord")
      offset = self.validated_data.get("Offset", 0)
      limit = self.validated_data.get("Limit")
      limit = limit + offset if limit is not None else None
      sort1 = self.validated_data.get("Sort1", "").lower()
      sort2 = self.validated_data.get("Sort2", "").lower()
      sort3 = self.validated_data.get("Sort3", "").lower()

      query = self.db.query(CallerId).filter(
          CallerId.tenant_id == tenant_id, or_(
              CallerId.caller_num_name.like("%" + search_word + "%"),
              CallerId.tenant_id.like("%" + search_word + "%")))[offset:limit]

      resp = []
      for q in query:
         temp = {}
         temp["CallerNumId"] = q.caller_num_id
         temp["ProjectId"] = q.project.project_id
         temp["ProjectName"] = q.project.project_name
         temp['CallerNum'] = q.caller_num
         temp['callerNumName'] = q.caller_num_name
         temp["PrefixNum"] = q.prefix_num
         temp["UpdateDate"] = q.update_date
         resp.append(temp)
      resp.sort(key=lambda x: (x.get(sort1), x.get(sort2), x.get(sort3)))
      return self.write_response('0000', response_data=resp,
                                 code=HTTPStatus.OK, message=None)


class CallerIdGetHandler(BaseHandler):

   SCHEMA = GET_SCHEMA

   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to get a specified caller notification number detailed allocation is acquired. 
      :param TenantId
      :param UserId
      :param CallerNumId
      """
      # Init variables
      resp = {}
      user_list = []
      group_list = []

      tenant_id = self.validated_data.get('TenantId')
      caller_num_id = self.validated_data.get("CallerNumId")
      try:
         caller_num_id = int(caller_num_id)
      except ValueError:
         return self.not_found(
             4009, "CallerId with CallerNumId=%s not found" % caller_num_id)

      query = self.db.query(CallerId, CallerIdUser, CallerIdGroup)
      join = query.join(CallerIdUser, isouter=True).join(
         CallerIdGroup, isouter=True)
      filters = join.filter(CallerId.caller_num_id ==
                            caller_num_id, CallerId.tenant_id == tenant_id)
      if not filters.count():
         return self.not_found(
             4009, "CallerId with CallerNumId=%s not found" % caller_num_id)

      for f in filters.all():
         user_dict = {}
         group_dict = {}
         call_ids = f[0]
         call_ids_user = f[1]
         call_ids_group = f[2]

         resp['CallerNumId'] = call_ids.caller_num_id
         resp['ProjectId'] = call_ids.project_id
         resp['ProjectName'] = call_ids.project.project_name
         resp['CallerNum'] = call_ids.caller_num
         resp['CallerNumName'] = call_ids.caller_num_name
         resp['PrefixNum'] = call_ids.prefix_num
         if call_ids_user is not None:
            user_dict['UserId'] = call_ids_user.user_id
            user_list.append(user_dict)
         resp['UserList'] = user_list

         if call_ids_group is not None:
            group_dict['Group'] = call_ids_group.group_id
            group_list.append(group_dict)
         resp['GroupList'] = group_list

      return self.write_response("0000",
                                 response_data=resp, code=HTTPStatus.OK)


class CallerIdUpdateHandler(BaseHandler):

   @gen.coroutine
   def post(self, *args, **kwargs):
      """
      API is used to update the caller notification number
      :param TenantId
      :param UserId
      :param UserList
          :subparam UserId
      :param GroupList
          :subparam GroupId
      """
      self.write_response()
