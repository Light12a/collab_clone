from copy import deepcopy

CONVERT_FIELDS = {
   'TenantId': 'tenant_id',
   'GroupId': 'group_id',
   'GroupName': 'group_name',
   'AuthId': 'auth_id',
   'AutoinTime': 'autoin_time'
}

CREATE_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string"
      },
      "UserList": {
         "type": "string"
      },
      "GroupList": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["TenantId",
                "UserList",
                "GroupList"]
}

SEARCH_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string"
      },
      "SearchWord": {
         "type": "string"
      },
      "Sort1": {
         "type": "string"
      },
      "Sort2": {
         "type": "string"
      },
      "Sort3": {
         "type": "string"
      },
      "Offset": {
         "type": "integer"
      },
      "Limit": {
         "type": "integer"
      }
   },
   "additionalProperties": False,
   "required": ["SearchWord"]
}

GET_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string"
      },
      "CallerNumId": {
         "type": "integer"
      }
   },
   "additionalProperties": False,
   "required": ["CallerNumId"]
}

PUT_SCHEMA = deepcopy(CREATE_SCHEMA)
PUT_SCHEMA["required"] = ["CallerNumId"]