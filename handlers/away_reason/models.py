import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from ..tenant_settings.models import Tenant
from sqlalchemy.ext.declarative import declarative_base
from services.database.mysqldb import Base

Base = declarative_base()
metadata = Base.metadata

class AwayReason(Base):
    __tablename__ = 'away_reason'
    __table_args__ = {'comment': 'Away Reason : Away Reason'}

    id = Column(BIGINT(20), primary_key=True, unique=True, comment='Id')
    tenant_id = Column(ForeignKey(Tenant.tenant_id), index=True, comment='Tenant Id : Tenant Id which these away reasons are belong to')
    away_reason = Column(String(1024), comment='Away Reason : Content of Away reason')
    is_display = Column(TINYINT(1), comment='Is Display : 0 is not displayed, 1 is displayed')
    update_date = Column(DateTime, comment='Update date : Last time that away reason is changed')

    tenant = relationship(Tenant)
    
    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}