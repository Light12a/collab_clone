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
      "GroupId": {
         "type": "string"
      },
      "GroupName": {
         "type": "string"
      },
      "AuthId": {
         "type": "integer",
      },
      "AutoinTime": {
         "type": "integer",
      }
   },
   "additionalProperties": False,
   "required": ["TenantId",
                "GroupId",
                "GroupName",
                "AuthId",
                "AutoinTime"]
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
      "GroupId": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["GroupId"]
}

GET_SKILL_SCHEMA = {
   "type": "object",
   "properties": {
      "token": {
         "type": "string",
         "minLength": 1
      }
   },
   "additionalProperties": False,
   "required": ["token"]
}

PUT_SCHEMA = deepcopy(CREATE_SCHEMA)
PUT_SCHEMA["required"] = ["GroupId"]