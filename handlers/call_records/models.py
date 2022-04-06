import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
# from sqlalchemy.ext.declarative import declarative_base
from services.database.mysqldb import Base

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
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)

    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}