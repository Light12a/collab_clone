from tkinter import Variable
from MySQLdb import DATE
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
from ..users.models import User
Base = declarative_base()
metadata = Base.metadata



class CorrespondenceMemo(Base):
    __tablename__ = 'correspondence_memo'

    correspondence_memo_id = Column(INTEGER(11), primary_key=True)
    tenant_id = Column(INTEGER(11), index=True)
    correspondence_memo_tag = Column(INTEGER(11))
    correspondence_memo_explaination = Column(String(45))
    last_change_date = Column(DateTime)

class RespondingMemo(Base):
    __tablename__ = 'responding_memo'

    memo_id = Column(INTEGER(11), primary_key = True, nullable=False)
    tenant_id = Column(VARCHAR(256), ForeignKey(Tenant.tenant_id))
    memo_name = Column(VARCHAR(256))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    tenant = relationship(Tenant)




