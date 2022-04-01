import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
# from sqlalchemy.ext.declarative import declarative_base
from services.database.mysqldb import Base

class SmsAuthenticator(Base):
    __tablename__ = 'sms_authenticators'

    sms_auth_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    sms_auth_name = Column(String(256))
    partner = Column(INTEGER(11), server_default=text("-1"))
    account_id = Column(String(256))
    request_id = Column(String(256))
    request_password = Column(String(256))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    
    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}