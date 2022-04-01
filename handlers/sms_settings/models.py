import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
# from sqlalchemy.ext.declarative import declarative_base
from services.database.mysqldb import Base

class SmsSetting(Base):
    __tablename__ = 'sms_settings'

    setting_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    setting_name = Column(String(256))
    sms_context = Column(Text)
    sms_auth_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)
    
    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
