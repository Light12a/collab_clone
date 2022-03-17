from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
Base = declarative_base()
metadata = Base.metadata

class Announcement(Base):
    __tablename__ = 'announcements'

    announce_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False, index=True, comment='Tenant ID')
    announce_name = Column(String(256), nullable=False)
    summary = Column(Text)
    location = Column(Text, nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    tenant = relationship(Tenant)

    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
