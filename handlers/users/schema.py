LOGIN_SCHEMA = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "company_id": {
                    "type": "string",
                    "minLength": 1
                },
                "username": {
                    "type": "string",
                    "minLength": 1
                },
                "password": {
                    "type": "string",
                    "minLength": 1
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
                    "minLength": 1
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
                "minLength": 1
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
                "minLength": 1
            }
    },
    "additionalProperties": False,
    "required": ["token"]
}

LOGIN_CPM_SCHEMA = {
    "type": "object",
    "properties": {
        "TenantId": {
            "type": "string",
            "minLength": 1
        },
        "UserId": {
            "type": "string",
            "minLength": 1
        },
        "Password": {
            "type": "string",
            "minLength": 1
        },
        "Lang": {
            "type": "integer",
            "minLength": 1
        },
    },
    "additionalProperties": False,
    "required": ["TenantId", "UserId", "Password", "Lang"]
}

PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "TenantId": {
            "type": "string",
            "minLength": 1
        },
        "UserId": {
            "type": "string",
            "minLength": 1
        }},
    "additionalProperties": False,
    "required": ["TenantId", "UserId"]
}

PASSWORD_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {
        "TenantId": {
            "type": "string",
            "minLength": 1
        },
        "UserId": {
            "type": "string",
            "minLength": 1
        },
        "OldPassword": {
            "type": "string",
            "minLength": 1,
        },
        "NewPassword": {
            "type": "string",
            "minLength": 1
        },
        "ConfirmPassword": {
            "type": "string",
            "minLength": 1
        }
        },
    "additionalProperties": False,
    "required": ["TenantId", "UserId", "OldPassword", "NewPassword", "ConfirmPassword"]
}
