from copy import deepcopy

CREATE_SCHEMA = {
   "type": "object",
   "properties": {
      "TenantId": {
         "type": "string"
      },
      "AuthName": {
         "type": "string"
      },
      "UseMonitor": {
         "type": "boolean"
      },
      "UseAddress": {
         "type": "boolean"
      },
      "EditAddress": {
         "type": "boolean"
      },
      "DlAddress": {
         "type": "boolean"
      },
      "DelAddress": {
         "type": "boolean"
      },
      "ScopeAddress": {
         "type": "integer"
      },
      "AddressList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "AddressListId": {
                  "type": "integer"
               }
            }
         },
      },
      "UseResponding": {
         "type": "boolean"
      },
      "EditResponding": {
         "type": "boolean"
      },
      "DlResponding": {
         "type": "boolean"
      },
      "DelResponding": {
         "type": "boolean"
      },
      "ScopeResponding": {
         "type": "integer"
      },
      "RespondingList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "ProjectId": {
                  "type": "integer"
               }
            }
         },
      },
      "UseMessage": {
         "type": "boolean"
      },
      "EditMessage": {
         "type": "boolean"
      },
      "DlMessage": {
         "type": "boolean"
      },
      "DelMessage": {
         "type": "boolean"
      },
      "ScopeMessage": {
         "type": "integer"
      },
      "MessageList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "ProjectId": {
                  "type": "integer"
               }
            }
         },
      },
      "EditDashboard": {
         "type": "boolean"
      },
      "DelDashboard": {
         "type": "boolean"
      },
      "ScopeDashboard": {
         "type": "integer"
      },
      "DashboardList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "ReportType": {
                  "type": "integer"
               },
               "ReportId": {
                  "type": "integer"
               }
            }
         },
      },
      "UseReport": {
         "type": "boolean"
      },
      "EditReport": {
         "type": "boolean"
      },
      "DlReport": {
         "type": "boolean"
      },
      "DelReport": {
         "type": "boolean"
      },
      "ScopeReport": {
         "type": "integer"
      },
      "ReportList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "ReportType": {
                  "type": "integer"
               },
               "ReportId": {
                  "type": "integer"
               }
            }
         },
      },
      "UseUser": {
         "type": "boolean"
      },
      "EditUser": {
         "type": "boolean"
      },
      "DlUser": {
         "type": "boolean"
      },
      "DelUser": {
         "type": "boolean"
      },
      "ScopeUser": {
         "type": "integer"
      },
      "UserList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "Type": {
                  "type": "integer"
               },
               "Id": {
                  "type": "string"
               }
            }
         },
      },
      "UseGroup": {
         "type": "boolean"
      },
      "EditGroup": {
         "type": "boolean"
      },
      "DlGroup": {
         "type": "boolean"
      },
      "DelGroup": {
         "type": "boolean"
      },
      "ScopeGroup": {
         "type": "integer"
      },
      "GroupList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "GroupId": {
                  "type": "string"
               }
            }
         },
      },
      "UseAuth": {
         "type": "boolean"
      },
      "EditAuth": {
         "type": "boolean"
      },
      "DlAuth": {
         "type": "boolean"
      },
      "DelAuth": {
         "type": "boolean"
      },
      "UseFlow": {
         "type": "boolean"
      },
      "EditFlow": {
         "type": "boolean"
      },
      "DelFlow": {
         "type": "boolean"
      },
      "UseSeat": {
         "type": "boolean"
      },
      "EditSeat": {
         "type": "boolean"
      },
      "DelSeat": {
         "type": "boolean"
      },
      "ScopeSeat": {
         "type": "integer"
      },
      "SeatList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "SeatviewId": {
                  "type": "integer"
               }
            }
         },
      },
      "UseChat": {
         "type": "boolean"
      },
      "ScopeChat": {
         "type": "integer"
      },
      "ChatList": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "Type": {
                  "type": "integer"
               },
               "Id": {
                  "type": "string"
               }
            }
         },
      },
      "UseSpeech": {
         "type": "boolean"
      },
      "EditSpeech": {
         "type": "boolean"
      },
      "DelSpeech": {
         "type": "boolean"
      },
      "UseTrigger": {
         "type": "boolean"
      },
      "EditTrigger": {
         "type": "boolean"
      },
      "DelTrigger": {
         "type": "boolean"
      },
      "UseConfig": {
         "type": "boolean"
      },
      "EditConfig": {
         "type": "boolean"
      },
      "UseLog": {
         "type": "boolean"
      },
      "DlLog": {
         "type": "boolean"
      }
   },
   "additionalProperties": False,
   "required": ["TenantId",
                "AuthName",
                "UseMonitor",
                "UseAddress",
                "EditAddress",
                "DlAddress",
                "DelAddress",
                "ScopeAddress",
                "UseResponding",
                "EditResponding",
                "DlResponding",
                "DelResponding",
                "ScopeResponding",
                "UseMessage",
                "EditMessage",
                "DlMessage",
                "DelMessage",
                "ScopeMessage",
                "EditDashboard",
                "DelDashboard",
                "ScopeDashboard",
                "UseReport",
                "EditReport",
                "DlReport",
                "DelReport",
                "ScopeReport",
                "UseUser",
                "EditUser",
                "DlUser",
                "DelUser",
                "ScopeUser",
                "UseGroup",
                "EditGroup",
                "DlGroup",
                "DelGroup",
                "ScopeGroup",
                "UseAuth",
                "EditAuth",
                "DlAuth",
                "DelAuth",
                "UseFlow",
                "EditFlow",
                "DelFlow",
                "UseSeat",
                "EditSeat",
                "DelSeat",
                "ScopeSeat",
                "UseChat",
                "ScopeChat",
                "UseSpeech",
                "EditSpeech",
                "DelSpeech",
                "UseTrigger",
                "EditTrigger",
                "DelTrigger",
                "UseConfig",
                "EditConfig",
                "UseLog",
                "DlLog"]
}

CONVERT_CREATE = {
   "AuthId": "auth_id",
   "TenantId": "tenant_id",
   "AuthName": "auth_name",
   "UseMonitor": "use_monitor",
   "UseAddress": "use_address",
   "EditAddress": "edit_address",
   "DlAddress": "dl_address",
   "DelAddress": "del_address",
   "ScopeAddress": "scope_address",
   "UseResponding": "use_responding",
   "EditResponding": "edit_responding",
   "DlResponding": "dl_responding",
   "DelResponding": "del_responding",
   "ScopeResponding": "scope_responding",
   "UseMessage": "use_message",
   "EditMessage": "edit_message",
   "DlMessage": "dl_message",
   "DelMessage": "del_message",
   "ScopeMessage": "scope_message",
   "EditDashboard": "edit_dashboard",
   "DelDashboard": "del_dashboard",
   "ScopeDashboard": "scope_dashboard",
   "UseReport": "use_report",
   "EditReport": "edit_report",
   "DlReport": "dl_report",
   "DelReport": "del_report",
   "ScopeReport": "scope_report",
   "UseUser": "use_user",
   "EditUser": "edit_user",
   "DlUser": "dl_user",
   "DelUser": "del_user",
   "ScopeUser": "scope_user",
   "UseGroup": "use_group",
   "EditGroup": "edit_group",
   "DlGroup": "dl_group",
   "DelGroup": "del_group",
   "ScopeGroup": "scope_group",
   "UseAuth": "use_auth",
   "EditAuth": "edit_auth",
   "DlAuth": "dl_auth",
   "DelAuth": "del_auth",
   "UseFlow": "use_flow",
   "EditFlow": "edit_flow",
   "DelFlow": "del_flow",
   "UseSeat": "use_seat",
   "EditSeat": "edit_seat",
   "DelSeat": "del_seat",
   "ScopeSeat": "scope_seat",
   "UseChat": "use_chat",
   "ScopeChat": "scope_chat",
   "UseSpeech": "use_speech",
   "EditSpeech": "edit_speech",
   "DelSpeech": "del_speech",
   "UseTrigger": "use_trigger",
   "EditTrigger": "edit_trigger",
   "DelTrigger": "del_trigger",
   "UseConfig": "use_config",
   "EditConfig": "edit_config",
   "UseLog": "use_log",
   "DlLog": "dl_log",
   "InsertDate": "insert_date",
   "UpdateDate": "update_date"
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