from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from handlers.project_settings.models import Project
from handlers.tenant_settings.models import Tenant
from handlers.users.models import User
from handlers.groups.models import Group
from services.database.mysqldb import Base


class CallerId(Base):
   __tablename__ = 'caller_ids'

   caller_num_id = Column(BIGINT(20), primary_key=True, unique=True)
   tenant_id = Column(String(256), ForeignKey(
       Tenant.tenant_id), nullable=False)
   project_id = Column(BIGINT(20), ForeignKey(
       Project.project_id), nullable=False)
   caller_num = Column(String(64), nullable=False)
   caller_num_name = Column(String(256))
   prefix_num = Column(String(32))
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   tenant = relationship(Tenant, backref='caller_id')
   project = relationship(Project, backref='caller_id')


class CallerIdGroup(Base):
   __tablename__ = 'caller_id_groups'

   id = Column(BIGINT(20), primary_key=True, unique=True)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   caller_num_id = Column(BIGINT(20), ForeignKey(
       CallerId.caller_num_id), nullable=False)
   group_id = Column(ForeignKey(Group.group_id), nullable=False)
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))

   tenant = relationship(Tenant, backref='caller_id_group')
   caller_id = relationship(CallerId, backref='caller_id_group')
   group = relationship(Group, backref='caller_id_group')


class CallerIdUser(Base):
   __tablename__ = 'caller_id_users'

   id = Column(BIGINT(20), primary_key=True, unique=True)
   tenant_id = Column(ForeignKey(Tenant.tenant_id),  nullable=False)
   caller_num_id = Column(BIGINT(20), ForeignKey(
       CallerId.caller_num_id), nullable=False)
   user_id = Column(ForeignKey(User.user_id), nullable=False)
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))

   tenant = relationship(Tenant, backref='caller_id_user')
   caller_id = relationship(CallerId, backref='caller_id_user')
   user = relationship(User, backref='caller_id_user')
