from copy import deepcopy


CONVERT_FIELDS = {
   'TenantId': 'tenant_id',
   'OperationUserId': 'user_id',
   'AnnounceName': 'group_name',
   'Summary': 'auth_id',
   'FileName': 'autoin_time'
}

CREATE_SCHEMA = {
        "type": "object",
        "properties": {
            "TenantId": {
                "type": "string"
            },
            "OperationUserId": {
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
        "required": ["TenantId", "OperationUserId", "AnnounceName", "FileName"]
    }

PUT_SCHEMA = deepcopy(CREATE_SCHEMA)
PUT_SCHEMA["required"] = ["TenantId"]