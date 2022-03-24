from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from ..tenant_settings.models import Tenant
from ..users.models import User
from services.database.mysqldb import Base


class HistoricalReportSetting(Base):
    __tablename__ = 'hreport_settings'

    hreport_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False, index=True, comment='Tenant ID')
    hreport_name = Column(String(256), nullable=False)
    report_type = Column(INTEGER(11), server_default=text("-1"))
    period_type = Column(INTEGER(11), server_default=text("-1"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    row_group1 = Column(INTEGER(11), server_default=text("-1"))
    row_group2 = Column(INTEGER(11), server_default=text("-1"))
    row_group3 = Column(INTEGER(11), server_default=text("-1"))
    show_zero = Column(TINYINT(1), server_default=text("0"))
    noans_sec = Column(INTEGER(11), server_default=text("-1"))
    csv_send_type = Column(INTEGER(11), server_default=text("-1"))
    csv_send_week = Column(INTEGER(11), server_default=text("-1"))
    csv_send_day = Column(INTEGER(11), server_default=text("-1"))
    csv_send_hour = Column(INTEGER(11), server_default=text("-1"))
    csv_send_minute = Column(INTEGER(11), server_default=text("-1"))
    csv_mail = Column(String(512))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    tenant = relationship(Tenant)

    
class HistoricalReportCallCols(Base):
    """
    Historical Report for call Records column
    """
    __tablename__ = 'hreport_call_cols'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    show_from = Column(TINYINT(1), server_default=text("0"))
    show_to = Column(TINYINT(1), server_default=text("0"))
    show_startdate = Column(TINYINT(1), server_default=text("0"))
    show_answerdate = Column(TINYINT(1), server_default=text("0"))
    show_enddate = Column(TINYINT(1), server_default=text("0"))
    show_totaltime = Column(TINYINT(1), server_default=text("0"))
    show_talktime = Column(TINYINT(1), server_default=text("0"))
    show_result = Column(TINYINT(1), server_default=text("0"))
    show_call_id = Column(TINYINT(1), server_default=text("0"))
    show_unique_id = Column(TINYINT(1), server_default=text("0"))
    show_hold_time = Column(TINYINT(1), server_default=text("0"))
    show_hold_cnt = Column(TINYINT(1), server_default=text("0"))
    show_proc_time = Column(TINYINT(1), server_default=text("0"))
    show_wait_time = Column(TINYINT(1), server_default=text("0"))
    show_ring_time = Column(TINYINT(1), server_default=text("0"))
    show_skill = Column(TINYINT(1), server_default=text("0"))
    show_trans = Column(TINYINT(1), server_default=text("0"))
    show_passobj_1 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_2 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_3 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_4 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_5 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_6 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_7 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_8 = Column(TINYINT(1), server_default=text("0"))
    show_passobj_last = Column(TINYINT(1), server_default=text("0"))
    show_user_id = Column(TINYINT(1), server_default=text("0"))
    order_setting = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)

    


class HistoricalReportCcCols(Base):
    """
    Historical Report for call center columns
    """
    __tablename__ = 'hreport_cc_cols'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    show_ccname = Column(TINYINT(1), server_default=text("0"))
    show_ans_rate = Column(TINYINT(1), server_default=text("0"))
    show_abd_rate = Column(TINYINT(1), server_default=text("0"))
    show_sla_cnt = Column(TINYINT(1), server_default=text("0"))
    show_sla_rate = Column(TINYINT(1), server_default=text("0"))
    show_incoming_cnt = Column(TINYINT(1), server_default=text("0"))
    show_skill_cnt = Column(TINYINT(1), server_default=text("0"))
    show_ans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_waitans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_abd_cnt = Column(TINYINT(1), server_default=text("0"))
    show_force_cnt = Column(TINYINT(1), server_default=text("0"))
    show_hold_cnt = Column(TINYINT(1), server_default=text("0"))
    show_ans_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_ans_time_max = Column(TINYINT(1), server_default=text("0"))
    show_abd_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_abd_time_max = Column(TINYINT(1), server_default=text("0"))
    show_talk_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_talk_time_max = Column(TINYINT(1), server_default=text("0"))
    show_talk_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_hold_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_hold_time_max = Column(TINYINT(1), server_default=text("0"))
    show_hold_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_memo = Column(TINYINT(1), server_default=text("0"))
    order_setting = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)
    
    


class HistoricalReportGroup(Base):
    """
    Historical Report for group
    """
    __tablename__ = 'hreport_groups'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    group_id = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)

    

class HistoricalReportProjects(Base):
    __tablename__ = 'hreport_projects'

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    hreport_id =Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    project_id = Column(BIGINT(20), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date =Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)

    


class HistoricalReportSkillColsSetting(Base):
    __tablename__ = 'hreport_skill_cols'

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    hreport_id = Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    show_skill_name = Column(TINYINT(1), server_default=text("0"))
    show_skill_id = Column(TINYINT(1), server_default=text("0"))
    show_incoming_cnt = Column( TINYINT(1), server_default=text("0"))
    show_noans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_ans_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_ans_time_max = Column(TINYINT(1), server_default=text("0"))
    show_noans_time_max = Column(TINYINT(1), server_default=text("0"))
    show_talk_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_talk_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_acw_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_acw_time_max = Column(TINYINT(1), server_default=text("0"))
    show_hold_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_hold_time_max = Column(TINYINT(1), server_default=text("0"))
    order_setting = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)

    


class HistoricalReportSkill(Base):
    __tablename__ = 'hreport_skills'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    group_id = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)

    


class HistoricalReportUserCols(Base):

    __tablename__ = 'hreport_user_cols'

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    hreport_id = Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    show_user_ext = Column(TINYINT(1), server_default=text("0"))
    show_user_id = Column(TINYINT(1), server_default=text("0"))
    show_user_name = Column(TINYINT(1), server_default=text("0"))
    show_out_call_cnt = Column(TINYINT(1), server_default=text("0"))
    show_out_talk_cnt = Column(TINYINT(1), server_default=text("0"))
    show_out_noans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_out_hold_cnt = Column(TINYINT(1), server_default=text("0"))
    show_out_hold_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_out_hold_time_max = Column(TINYINT(1), server_default=text("0"))
    show_out_hold_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_out_acw_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_out_acw_time_max = Column(TINYINT(1), server_default=text("0"))
    show_out_acw_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_out_talk_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_out_talk_time_max = Column(TINYINT(1), server_default=text("0"))
    show_out_talk_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_out_trans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_out_anstrans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_in_incoming_cnt = Column(TINYINT(1), server_default=text("0"))
    show_in_ans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_in_noans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_in_hold_cnt = Column(TINYINT(1), server_default=text("0"))
    show_in_avail_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_acw_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_acw_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_in_acw_time_max = Column(TINYINT(1), server_default=text("0"))
    show_in_auxdetail_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_auxdetail_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_in_aux_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_in_login_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_ans_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_in_ans_time_max = Column(TINYINT(1), server_default=text("0"))
    show_in_noans_time_max = Column(TINYINT(1), server_default=text("0"))
    show_in_talk_avg = Column(TINYINT(1), server_default=text("0"))
    show_in_talk_max = Column(TINYINT(1), server_default=text("0"))
    show_in_talk_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_trans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_in_anstrans_cnt = Column(TINYINT(1), server_default=text("0"))
    show_in_monitor_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_coach_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_hold_time_avg = Column(TINYINT(1), server_default=text("0"))
    show_in_hold_time_max = Column(TINYINT(1), server_default=text("0"))
    show_in_hold_time_sum = Column(TINYINT(1), server_default=text("0"))
    show_in_memo = Column(TINYINT(1), server_default=text("0"))
    order_setting = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)


class HistoricalReportUser(Base):
    __tablename__ = 'hreport_users'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(ForeignKey(HistoricalReportSetting.hreport_id), nullable=False)
    user_id	= Column(ForeignKey(User.user_id), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    historical_setting = relationship(HistoricalReportSetting)
    user = relationship(User)

    
 
 
