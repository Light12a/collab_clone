LOGIN_SCHEMA = {
   "oneOf": [
      {
         "type": "object",
         "properties": {
            "company_id": {
               "type": "string",
               "minLength":1
            },
            "username": {
               "type": "string",
               "minLength":1
            },
            "password": {
               "type": "string",
               "minLength":1
            },
         },
         "additionalProperties": False,
         "required": ["company_id", "username", "password"]
      },
      {
         "type": "object",
         "properties": {
            "token": {
               "type": "string",
               "minLength":1               
            }
         },
         "additionalProperties": False,
         "required": ["token"]
      }
   ]
}

LOGOUT_SCHEMA = {
    "type": "object",
         "properties": {
            "token": {
               "type": "string",
               "minLength":1
            }
         },
         "additionalProperties": False,
         "required": ["token"]
}

REFRESH_SCHEMA = {
    "type": "object",
         "properties": {
            "token": {
               "type": "string",
               "minLength":1
            }
         },
         "additionalProperties": False,
         "required": ["token"]
}

