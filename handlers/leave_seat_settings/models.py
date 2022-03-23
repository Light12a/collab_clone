from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
from services.database.mysqldb import Base


class AuxReasonSetting(Base):
    __tablename__ = 'aux_reason_settings'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
    reason1_name = Column(String(256))
    reason2_name = Column(String(256))
    reason3_name = Column(String(256))
    reason4_name = Column(String(256))
    reason5_name = Column(String(256))
    reason6_name = Column(String(256))
    reason7_name = Column(String(256))
    reason8_name = Column(String(256))
    reason9_name = Column(String(256))
    reason10_name = Column(String(256))
    reason11_name = Column(String(256))
    reason12_name = Column(String(256))
    reason13_name = Column(String(256))
    reason14_name = Column(String(256))
    reason15_name = Column(String(256))
    reason1_visible = Column(TINYINT(1))
    reason2_visible = Column(TINYINT(1))
    reason3_visible = Column(TINYINT(1))
    reason4_visible = Column(TINYINT(1))
    reason5_visible = Column(TINYINT(1))
    reason6_visible = Column(TINYINT(1))
    reason7_visible = Column(TINYINT(1))
    reason8_visible = Column(TINYINT(1))
    reason9_visible = Column(TINYINT(1))
    reason10_visible = Column(TINYINT(1))
    reason11_visible = Column(TINYINT(1))
    reason12_visible = Column(TINYINT(1))
    reason13_visible = Column(TINYINT(1))
    reason14_visible = Column(TINYINT(1))
    reason15_visible = Column(TINYINT(1))
    insert_date = Column(DateTime, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, server_default=text("current_timestamp()"))

    tenant = relationship(Tenant)