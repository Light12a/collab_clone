import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from services.database.mysqldb import Base


class Tenant(Base):
   __tablename__ = 'tenant'
   __table_args__ = {'comment': 'Tenant : All information about tenant'}

   tenant_id = Column(String(256), primary_key=True, comment='tenant_id : id of tenant')
   tenant_name = Column(String(256), comment=' tenant_name : name of tenant')
   domain = Column(String(45), comment='domain : domain of tenant,')
   prefix = Column(INTEGER(11), comment='prefix : prefix of tenant, ex a number as 01, 02 ')
   identifier = Column(String(256), comment='identifier : identifier of tenant, ex ABC-01a')
   channel_cnt = Column(INTEGER(11), comment='channel_cnt : number of maximum channel of tenant')
   use_speech_to_text = Column(TINYINT(4), comment='use_speech_to_text : 0 is off, 1 is on speech_to_text')
   st_engine = Column(INTEGER(11), comment='st_engine : Choose between Ami voice or Google speak to text')
   insert_date = Column(DateTime, comment='insert_date : registration date')
   update_date = Column(DateTime, comment='update_date : Last time tenant is changed')
