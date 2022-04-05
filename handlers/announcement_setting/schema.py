from copy import deepcopy


CONVERT_FIELDS = {
   'TenantId': 'tenant_id',
   'AnnounceName': 'announce_name',
   'Summary': 'summary',
   'FileName': 'location'
}

CREATE_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string"
      },
      "AnnounceName": {
         "type": "string"
      },
      "Summary": {
         "type": "string"
      },
      "FileName": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["TenantId", "AnnounceName", "FileName"]
}

GET_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string"
      },
      "AnnounceId": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["TenantId", "AnnounceId"]
}

PUT_SCHEMA = deepcopy(CREATE_SCHEMA)
PUT_SCHEMA["required"] = ["TenantId"]
