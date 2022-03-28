import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from services.database.mysqldb import Base
from ..tenant_settings.models import Tenant
from handlers.authority.models import Authority
from handlers.callflow_settings.models import Flows

class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
    project_name = Column(String(256), nullable=False)
    dial_in = Column(String(64))
    chennel_cnt = Column(INTEGER(11))
    flow_id = Column(ForeignKey(Flows.flows_id))
    in_route_num = Column(String(64))
    sla = Column(INTEGER(11))
    out_filter = Column(BIGINT(20))
    carrier = Column(INTEGER(11), server_default=text("0"))
    mcc_gw = Column(INTEGER(11), server_default=text("0"))
    global_domain = Column(String(256))
    use_sipport = Column(TINYINT(1), server_default=text("0"))
    sipport = Column(String(64))
    use_rtpport = Column(TINYINT(1), server_default=text("0"))
    rtpport = Column(String(64))
    carrier_user = Column(String(256))
    carrier_password = Column(String(256))
    faq_partner_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    tenant = relationship(Tenant)
    flow = relationship(Flows)


class ProjectNgword(Base):
    __tablename__ = 'project_ngwords'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id))
    project_id = Column(ForeignKey(Project.project_id))
    ng_list_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    tenant = relationship(Tenant)
    project = relationship(Project)

class ProjectFagword(Base):
    __tablename__ = 'project_fagwords'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id))
    project_id = Column(ForeignKey(Project.project_id))
    faq_list_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    
    tenant = relationship(Tenant)
    project = relationship(Project)