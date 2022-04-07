from copy import deepcopy

CREATE_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string"
      },
      "TenantName": {
         "type": "string"
      },
      "Identifier": {
         "type": "string"
      },
      "ChannelCnt": {
         "type": "integer"
      },
      "UseSpeechToText": {
         "type": "boolean"
      },
      "StEngine": {
         "type": "integer"
      },
      "UserName": {
         "type": "string"
      },
      "Password": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["TenantId",
                "TenantName",
                "Identifier",
                "ChannelCnt",
                "UseSpeechToText",
                "StEngine",
                "UserName",
                "Password"]
}

CONVERT_CREATE = {
   "TenantId": "tenant_id",
   "TenantName": "tenant_name",
   "Identifier": "identifier",
   "ChannelCnt": "channel_cnt",
   "UseSpeechToText": "use_speech_to_text",
   "StEngine": "st_engine"
}

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
