User_Retrieval_SCHEMA = {
    "type": "object",
    "properties": {
            "TenantId": {
                "type": "string"
            },
            "GroupId": {
                "type": "string"
            },
            "UserName": {
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
    },
    "additionalProperties": False,
    "required": ["TenantId", "GroupId", "UserName", "Sort1", "Sort2", "Sort3"]
}

User_Status_Acquisition_SCHEMA = {
    "type": "object",
    "properties": {
            "TenantId": {
                "type": "string"
            },
            "UserId": {
                "type": "string"
            },
    },
    "additionalProperties": False,
    "required": ["TenantId", "UserId"]

}