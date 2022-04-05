from sqlalchemy import Column, Date, DateTime, ForeignKey, String,Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from handlers.project_settings.models import Project
from ..tenant_settings.models import Tenant
from services.database.mysqldb import Base

class AuthProject(Base):
    __tablename__ = 'auth_projects'

    auth_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), primary_key=True, nullable=False, index=True, comment='Tenant ID')
    type = Column(INTEGER(11))
    project_id = Column(ForeignKey(Project.project_id), primary_key=True)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    tenant = relationship(Tenant)

