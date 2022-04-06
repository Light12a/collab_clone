from copy import deepcopy

SEARCH_SCHEMA = {
   "type": "object",
   "properties": {
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
      }
   },
   "additionalProperties": False,
   "required": ["TenantId"]
}
