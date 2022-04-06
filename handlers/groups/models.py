from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from handlers.tenant_settings.models import Tenant
from handlers.authority.models import Authority
from services.database.mysqldb import Base

class Group(Base):
    __tablename__ = 'groups'

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), primary_key=True, nullable=False, index=True)
    group_id = Column(VARCHAR(256), primary_key=True, nullable=False, index=True)
    group_name = Column(VARCHAR(256))
    auth_id = Column(BIGINT(20), ForeignKey(Authority.auth_id), nullable=False)
    autoin_time = Column(INTEGER(11))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    tenant = relationship(Tenant)
    authority = relationship(Authority)
    