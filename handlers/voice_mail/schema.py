from copy import deepcopy

CREATE_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string",
      },
      "OperationUserId": {
         "type": "string",
      },
      "SaveDate": {
         "type": "string"
      },
      "IncomingDate": {
         "type": "string"
      },
      "RecordingTime": {
         "type": "integer"
      },
      "DialIn": {
         "type": "integer"
      },
      "CustomerTelnum": {
         "type": "string"
      },
      "RecordingPath": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["SaveDate", "IncomingDate", "RecordingTime", "DialIn",
                "CustomerTelnum", "RecordingPath"]
}

CONVERT_CREATE = {
   "TenantId": "tenant_id",
   "OperationUserId": "user_id",
   "SaveDate": "save_date",
   "IncomingDate": "incoming_date",
   "RecordingTime": "recording_time",
   "DialIn": "project_id",
   "CustomerTelnum": "customer_telnum",
   "RecordingPath": "recording_path"
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
      "AuthId": {
         "type": "integer"
      }
   },
   "additionalProperties": False,
   "required": ["AuthId"]
}

PUT_SCHEMA = deepcopy(CREATE_SCHEMA)
PUT_SCHEMA["required"] = ["auth_id"]

JUDGE_SCHEMA = {
   "type": "object",
   "properties": {
      "user_id": {
         "type": "string"
      },
      "operation": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["user_id", "operation"]
}

USER_GET_SCHEMA = {
   "type": "object",
   "properties": {
      "user_id": {
         "type": "string"
      }
   },
   "additionalProperties": False,
   "required": ["user_id"]
}