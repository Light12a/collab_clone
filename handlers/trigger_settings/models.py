from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
Base = declarative_base()
metadata = Base.metadata

class Trigger(Base):
    __tablename__ = 'triggers'

    trigger_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False, index=True, comment='Tenant ID')
    trigger_name = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    tenant = relationship(Tenant)

    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

class TriggerCondition(Base):
    __tablename__ = 'trigger_conditions'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    trigger_id = Column(ForeignKey(Trigger.trigger_id), nullable=False)
    cond_action = Column(INTEGER(11))
    project_id = Column(BIGINT(20))
    skill_id = Column(String(256))
    call_status = Column(INTEGER(11))
    _condition = Column(INTEGER(11))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    trigger = relationship(Trigger)

    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

class TriggerContent(Base):
    __tablename__ = 'trigger_contents'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    trigger_id = Column(ForeignKey(Trigger.trigger_id), nullable=False)
    impl_action = Column(INTEGER(11))
    script_id = Column(BIGINT(20))
    url = Column(String(2048))
    method = Column(String(32))
    req_header = Column(Text)
    req_body = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    trigger = relationship(Trigger)

    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
