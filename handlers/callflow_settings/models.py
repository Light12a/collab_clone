from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from handlers.tenant_settings.models import Tenant
from services.database.mysqldb import Base

class Flows(Base):
    __tablename__ = 'flows'

    flows_id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
    flow_name = Column(String(256), nullable=False)
    summary = Column(Text)
    flow_setting = Column(LONGTEXT)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    tenant = relationship(Tenant)
