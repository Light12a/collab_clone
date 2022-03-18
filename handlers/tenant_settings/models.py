import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
# from sqlalchemy.ext.declarative import declarative_base
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
    away_reason = relationship("AwayReason", backref="tenant")


class CallRecord(Base):
    __tablename__ = 'call_records'

    call_record_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    from_addr = Column(String(64))
    to_addr = Column(String(64))
    destination = Column(String(64))
    start_date = Column(DateTime)
    skill_start_date = Column(DateTime)
    answer_date = Column(DateTime)
    end_date = Column(DateTime)
    total_time = Column(Time)
    talk_time = Column(Time)
    result = Column(INTEGER(11))
    call_id = Column(String(1024))
    unique_id = Column(String(1024))
    hold_time = Column(Time)
    hold_cnt = Column(INTEGER(11))
    proc_time = Column(Time)
    wait_time = Column(Time)
    ring_time = Column(Time)
    skill_id = Column(String(256))
    transfer = Column(TINYINT(1))
    transferred = Column(TINYINT(1))
    passobj = Column(LONGTEXT)
    user_id = Column(String(256))
    group_id = Column(String(256))
    direction = Column(INTEGER(11))
    memo_id = Column(BIGINT(20))
    memo_free = Column(String(512))
    acw_time = Column(Time)
    project_id = Column(BIGINT(20))
    sla_ans = Column(TINYINT(1))
    insert_date = Column(DateTime, nullable=True)
    update_date = Column(DateTime, nullable=True)