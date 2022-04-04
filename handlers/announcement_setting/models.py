from sqlalchemy import Column, Date, DateTime, ForeignKey, String,Text, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from ..tenant_settings.models import Tenant
from services.database.mysqldb import Base
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

