from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from services.database.mysqldb import Base
from ..tenant_settings.models import Tenant

class Settings(Base):
    __tablename__ = 'settings'

    setting_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
    speech_ext = Column(INTEGER(11), server_default=text("0"))
    recording_type = Column(INTEGER(11), server_default=text("0"))
    list_cnt_users = Column(INTEGER(11), server_default=text("10"))
    list_cnt_groups = Column(INTEGER(11), server_default=text("10"))
    list_cnt_auth = Column(INTEGER(11), server_default=text("10"))
    list_cnt_projects = Column(INTEGER(11), server_default=text("10"))
    list_cnt_skills = Column(INTEGER(11), server_default=text("10"))
    list_cnt_skillassign = Column(INTEGER(11), server_default=text("10"))
    list_cnt_flows = Column(INTEGER(11), server_default=text("10"))
    list_cnt_business_hours = Column(INTEGER(11), server_default=text("10"))
    list_cnt_announcements = Column(INTEGER(11), server_default=text("10"))
    list_cnt_talkscripts = Column(INTEGER(11), server_default=text("10"))
    list_cnt_triggers = Column(INTEGER(11), server_default=text("10"))
    list_cnt_address = Column(INTEGER(11), server_default=text("10"))
    list_cnt_speech = Column(INTEGER(11), server_default=text("10"))
    list_cnt_rreports = Column(INTEGER(11), server_default=text("10"))
    list_cnt_seatviews = Column(INTEGER(11), server_default=text("10"))
    list_cnt_hreports = Column(INTEGER(11), server_default=text("10"))
    list_cnt_dashboards = Column(INTEGER(11), server_default=text("10"))
    list_cnt_respondings = Column(INTEGER(11), server_default=text("10"))
    list_cnt_voicemails = Column(INTEGER(11), server_default=text("10"))
    list_cnt_sms = Column(INTEGER(11), server_default=text("10"))
    list_cnt_operation_logs = Column(INTEGER(11), server_default=text("10"))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    tenant = relationship(Tenant)