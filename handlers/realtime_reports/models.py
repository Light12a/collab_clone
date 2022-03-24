from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
Base = declarative_base()
metadata = Base.metadata


class RealtimeReportSetting(Base):
    __tablename__ = 'rreport_settings'

    rreport_id = Column(BIGINT(20), primary_key=True, unique=True)
    rreport_name = Column(String(256), nullable=False)
    show_cc_total = Column(TINYINT(1), server_default=text("0"))
    show_cc_talk = Column(TINYINT(1), server_default=text("0"))
    show_cc_hold = Column(TINYINT(1), server_default=text("0"))
    show_cc_wait = Column(TINYINT(1), server_default=text("0"))
    show_cc_incoming_cnt = Column(TINYINT(1), server_default=text("0"))
    show_cc_skill_cnt = Column(TINYINT(1), server_default=text("0"))
    show_cc_ans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_cc_hold_cnt = Column(TINYINT(1), server_default=text("0"))
    show_cc_abd_cnt = Column(TINYINT(1), server_default=text("0"))
    show_cc_force_cnt = Column(TINYINT(1), server_default=text("0"))
    show_cc_ans_rate = Column(TINYINT(1), server_default=text("0"))
    show_cc_abd_rate = Column(TINYINT(1), server_default=text("0"))
    show_cc_sla_cnt = Column(TINYINT(1), server_default=text("0"))
    show_cc_sla_rate = Column(TINYINT(1), server_default=text("0"))
    show_cc_talk_avg = Column(TINYINT(1), server_default=text("0"))
    show_cc_wait_max = Column(TINYINT(1), server_default=text("0"))
    show_cc_hold_avg = Column(TINYINT(1), server_default=text("0"))
    show_us_ext = Column(TINYINT(1), server_default=text("0"))
    show_us_uname = Column(TINYINT(1), server_default=text("0"))
    show_us_uid = Column(TINYINT(1), server_default=text("0"))
    show_us_sts = Column(TINYINT(1), server_default=text("0"))
    show_us_elapsed = Column(TINYINT(1), server_default=text("0"))
    show_us_ans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_us_hold_cnt = Column(TINYINT(1), server_default=text("0"))
    show_us_talk_avg = Column(TINYINT(1), server_default=text("0"))
    show_us_ans_avg = Column(TINYINT(1), server_default=text("0"))
    show_us_acw_avg = Column(TINYINT(1), server_default=text("0"))
    show_us_work_avg = Column(TINYINT(1), server_default=text("0"))
    show_us_direction = Column(TINYINT(1), server_default=text("0"))
    show_us_telnum = Column(TINYINT(1), server_default=text("0"))
    show_us_out_cnt = Column(TINYINT(1), server_default=text("0"))
    show_us_trans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_us_anstrans_cnt = Column(TINYINT(1), server_default=text("0"))
    color_avail = Column(String(64))
    color_acw = Column(String(64))
    color_aux = Column(String(64))
    color_talk = Column(String(64))
    color_hold = Column(String(64))
    color_wait = Column(String(64))
    threshold_wait_1 = Column(INTEGER(11))
    threshold_wait_2 = Column(INTEGER(11))
    threshold_avail_1 = Column(INTEGER(11))
    threshold_avail_2 = Column(INTEGER(11))
    threshold_acw_1 = Column(INTEGER(11))
    threshold_acw_2 = Column(INTEGER(11))
    threshold_aux_1 = Column(INTEGER(11))
    threshold_aux_2 = Column(INTEGER(11))
    threshold_talk_1 = Column(INTEGER(11))
    threshold_hold_1 = Column(INTEGER(11))
    threshold_hold_2 = Column(INTEGER(11))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class RealtimeReportProject(Base):
    __tablename__ = 'rreport_projects'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    rreport_id = Column(ForeignKey(RealtimeReportSetting.rreport_id), nullable=False, index=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False, index=True, comment='Tenant ID')
    project_id = Column(BIGINT(20), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    realtime_report = relationship(RealtimeReportSetting)
    tenant = relationship(Tenant)

