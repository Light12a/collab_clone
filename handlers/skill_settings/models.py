import imp
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from services.database.mysqldb import Base
from ..tenant_settings.models import Tenant
from handlers.authority.models import Authority
from handlers.users.models import User

class Skill(Base):
    __tablename__ = 'skills'

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    skill_id = Column(String(256), primary_key=True, nullable=False)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), primary_key=True, nullable=False)
    skill_name = Column(String(256), nullable=False)
    routing_method = Column(INTEGER(11), server_default=text("0"))
    timeout_sec = Column(INTEGER(11), server_default=text("-1"))
    whisper_ann = Column(BIGINT(20))
    wait_start_sec = Column(INTEGER(11), server_default=text("0"))
    wait_sec = Column(INTEGER(11), server_default=text("-1"))
    ann_first_sec = Column(INTEGER(11), server_default=text("0"))
    ann_interval_sec = Column(INTEGER(11), server_default=text("0"))
    wait_ann = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

class SkillAssignment(Base):
    __tablename__ = 'skill_assignments'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False, index=True)
    skill_id = Column(ForeignKey(Skill.skill_id), nullable=False)
    user_id = Column(ForeignKey(User.user_id), nullable=False)
    skill_level = Column(INTEGER(11), server_default=text("-1"))
    insert_date = Column(DateTime, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, server_default=text("current_timestamp()"))