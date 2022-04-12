# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AddressDatum(Base):
    __tablename__ = 'address_data'

    id = Column(INTEGER(11), primary_key=True)
    tenant_id = Column(String(45), nullable=False)
    address_list_id = Column(BIGINT(20), nullable=False)
    name = Column(String(256), nullable=False)
    tel_num = Column(String(64), nullable=False)
    memo = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class AddressList(Base):
    __tablename__ = 'address_lists'

    address_list_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    address_list_name = Column(String(256), nullable=False)
    memo = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class Announcement(Base):
    __tablename__ = 'announcements'

    announce_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    announce_name = Column(String(256), nullable=False)
    summary = Column(Text)
    location = Column(Text, nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class AuthGroup(Base):
    __tablename__ = 'auth_groups'

    auth_id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    tenant_id = Column(String(256), primary_key=True, nullable=False)
    type = Column(INTEGER(11))
    group_id = Column(String(256), primary_key=True, nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class AuthSeatview(Base):
    __tablename__ = 'auth_seatviews'

    auth_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    type = Column(INTEGER(11), server_default=text("0"))
    seatview_id = Column(BIGINT(20), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class Authority(Base):
    __tablename__ = 'authority'

    auth_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(ForeignKey('tenant.tenant_id'), index=True, comment='Tenant ID')
    auth_name = Column(String(256), nullable=False)
    use_monitor = Column(TINYINT(1), server_default=text("0"))
    use_address = Column(TINYINT(1), server_default=text("0"))
    edit_address = Column(TINYINT(1), server_default=text("0"))
    dl_address = Column(TINYINT(1), server_default=text("0"))
    del_address = Column(TINYINT(1), server_default=text("0"))
    scope_address = Column(INTEGER(11), server_default=text("0"))
    use_responding = Column(TINYINT(1), server_default=text("0"))
    edit_responding = Column(TINYINT(1), server_default=text("0"))
    dl_responding = Column(TINYINT(1), server_default=text("0"))
    del_responding = Column(TINYINT(1), server_default=text("0"))
    scope_responding = Column(INTEGER(11), server_default=text("0"))
    use_message = Column(TINYINT(1), server_default=text("0"))
    edit_message = Column(TINYINT(1), server_default=text("0"))
    dl_message = Column(TINYINT(1), server_default=text("0"))
    del_message = Column(TINYINT(1), server_default=text("0"))
    scope_message = Column(INTEGER(11), server_default=text("0"))
    edit_dashboard = Column(TINYINT(1), server_default=text("0"))
    del_dashboard = Column(TINYINT(1), server_default=text("0"))
    scope_dashboard = Column(INTEGER(11), server_default=text("0"))
    use_report = Column(TINYINT(1), server_default=text("0"))
    edit_report = Column(TINYINT(1), server_default=text("0"))
    dl_report = Column(TINYINT(1), server_default=text("0"))
    del_report = Column(TINYINT(1), server_default=text("0"))
    scope_report = Column(INTEGER(11), server_default=text("0"))
    use_user = Column(TINYINT(1), server_default=text("0"))
    edit_user = Column(TINYINT(1), server_default=text("0"))
    dl_user = Column(TINYINT(1), server_default=text("0"))
    del_user = Column(TINYINT(1), server_default=text("0"))
    scope_user = Column(INTEGER(11), server_default=text("0"))
    use_group = Column(TINYINT(1), server_default=text("0"))
    edit_group = Column(TINYINT(1), server_default=text("0"))
    dl_group = Column(TINYINT(1), server_default=text("0"))
    del_group = Column(TINYINT(1), server_default=text("0"))
    scope_group = Column(INTEGER(11), server_default=text("0"))
    use_auth = Column(TINYINT(1), server_default=text("0"))
    edit_auth = Column(TINYINT(1), server_default=text("0"))
    dl_auth = Column(TINYINT(1), server_default=text("0"))
    del_auth = Column(TINYINT(1), server_default=text("0"))
    use_flow = Column(TINYINT(1), server_default=text("0"))
    edit_flow = Column(TINYINT(1), server_default=text("0"))
    del_flow = Column(TINYINT(1), server_default=text("0"))
    use_seat = Column(TINYINT(1), server_default=text("0"))
    edit_seat = Column(TINYINT(1), server_default=text("0"))
    del_seat = Column(TINYINT(1), server_default=text("0"))
    scope_seat = Column(INTEGER(11), server_default=text("0"))
    use_chat = Column(TINYINT(1), server_default=text("0"))
    scope_chat = Column(INTEGER(11), server_default=text("0"))
    use_speech = Column(TINYINT(1), server_default=text("0"))
    edit_speech = Column(TINYINT(1), server_default=text("0"))
    del_speech = Column(TINYINT(1), server_default=text("0"))
    use_trigger = Column(TINYINT(1), server_default=text("0"))
    edit_trigger = Column(TINYINT(1), server_default=text("0"))
    del_trigger = Column(TINYINT(1), server_default=text("0"))
    use_config = Column(TINYINT(1), server_default=text("0"))
    edit_config = Column(TINYINT(1), server_default=text("0"))
    use_log = Column(TINYINT(1), server_default=text("0"))
    dl_log = Column(TINYINT(1), server_default=text("0"))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    tenant = relationship('Tenant')


class BusinessHour(Base):
    __tablename__ = 'business_hours'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    setting_name = Column(String(256), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    open_sun = Column(TINYINT(1))
    open_mon = Column(TINYINT(1))
    open_tue = Column(TINYINT(1))
    open_wed = Column(TINYINT(1))
    open_thu = Column(TINYINT(1))
    open_fri = Column(TINYINT(1))
    open_sat = Column(TINYINT(1))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class CallRecord(Base):
    __tablename__ = 'call_records'

    call_record_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    from_addr = Column(String(64))
    to_addr = Column(String(64))
    destination = Column(String(64))
    start_date = Column(DateTime)
    skill_start_date = Column(DateTime)
    answer_date = Column(DateTime)
    end_date = Column(DateTime)
    total_time = Column(Time)
    talk_time = Column(Time)
    result = Column(INTEGER(11))
    call_id = Column(String(1024))
    unique_id = Column(String(1024))
    hold_time = Column(Time)
    hold_cnt = Column(INTEGER(11))
    proc_time = Column(Time)
    wait_time = Column(Time)
    ring_time = Column(Time)
    skill_id = Column(String(256))
    transfer = Column(TINYINT(1))
    transferred = Column(TINYINT(1))
    passobj = Column(LONGTEXT)
    user_id = Column(String(256))
    group_id = Column(String(256))
    direction = Column(INTEGER(11))
    memo_id = Column(BIGINT(20))
    memo_free = Column(String(512))
    acw_time = Column(Time)
    project_id = Column(BIGINT(20))
    sla_ans = Column(TINYINT(1))
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)


class CallerIdGroup(Base):
    __tablename__ = 'caller_id_groups'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    caller_num_id = Column(BIGINT(20), nullable=False)
    group_id = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class CallerIdUser(Base):
    __tablename__ = 'caller_id_users'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    caller_num_id = Column(BIGINT(20), nullable=False)
    user_id = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class CallerId(Base):
    __tablename__ = 'caller_ids'

    caller_num_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    project_id = Column(BIGINT(20), nullable=False)
    caller_num = Column(String(64))
    caller_num_name = Column(String(256))
    prefix_num = Column(String(32))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class CorrespondenceMemo(Base):
    __tablename__ = 'correspondence_memo'

    correspondence_memo_id = Column(INTEGER(11), primary_key=True)
    tenant_id = Column(INTEGER(11), index=True)
    correspondence_memo_tag = Column(INTEGER(11))
    correspondence_memo_explaination = Column(String(45))
    last_change_date = Column(DateTime)


class Dashboard(Base):
    __tablename__ = 'dashboard'

    dashboard_id = Column(INTEGER(11), primary_key=True)
    tenant_id = Column(INTEGER(11), nullable=False, index=True)
    dashboard_name = Column(VARCHAR(45))
    last_change_date = Column(DateTime)


class DashboardHreport(Base):
    __tablename__ = 'dashboard_hreports'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    dashboard_id = Column(BIGINT(20), nullable=False)
    detail = Column(LONGTEXT)
    hreport_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)


class DashboardRreport(Base):
    __tablename__ = 'dashboard_rreports'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    dashboard_id = Column(BIGINT(20), nullable=False)
    detail = Column(LONGTEXT)
    rreport_id = Column(BIGINT(20))
    view_graph = Column(INTEGER(11), server_default=text("0"))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class DashboardSetting(Base):
    __tablename__ = 'dashboard_setting'

    dashboard_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    dashboard_name = Column(String(256))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class ExtraBusinessHour(Base):
    __tablename__ = 'extra_business_hours'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    setting_name = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class ExtraBusinessHoursDetail(Base):
    __tablename__ = 'extra_business_hours_details'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    parent_id = Column(BIGINT(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class FaqWordDatum(Base):
    __tablename__ = 'faq_word_data'

    faq_word_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(255), nullable=False)
    faq_list_id = Column(BIGINT(20), nullable=False)
    faq_word = Column(String(255), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


t_faq_word_lists = Table(
    'faq_word_lists', metadata,
    Column('faq_list_id', BIGINT(20), nullable=False, unique=True),
    Column('tenant_id', String(256), nullable=False),
    Column('faq_list_name', String(256), nullable=False),
    Column('insert_date', DateTime, nullable=False, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


t_flows = Table(
    'flows', metadata,
    Column('flows_id', BIGINT(20), nullable=False, unique=True),
    Column('tenant_id', INTEGER(11)),
    Column('flow_name', String(256), nullable=False),
    Column('summary', Text),
    Column('project_id', String(256)),
    Column('setting', LONGTEXT),
    Column('insert_date', DateTime, nullable=False),
    Column('update_date', DateTime, nullable=False)
)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(BIGINT(20), nullable=False, unique=True)
    tenant_id = Column(String(256), primary_key=True, nullable=False)
    group_id = Column(String(256), primary_key=True, nullable=False)
    group_name = Column(String(256))
    auth_id = Column(BIGINT(20))
    autoin_time = Column(INTEGER(11))
    insert_date = Column(DateTime)
    update_date = Column(DateTime)


class HreportCallCol(Base):
    __tablename__ = 'hreport_call_cols'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(BIGINT(20), nullable=False)
    tenant_id = Column(String(256), nullable=False)
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


class HreportCcCol(Base):
    __tablename__ = 'hreport_cc_cols'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(BIGINT(20), nullable=False)
    tenant_id = Column(String(256), nullable=False)
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
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)


class HreportGroup(Base):
    __tablename__ = 'hreport_groups'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(BIGINT(20), nullable=False)
    tenant_id = Column(String(256), nullable=False)
    group_id = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


t_hreport_projects = Table(
    'hreport_projects', metadata,
    Column('id', BIGINT(20), nullable=False, unique=True),
    Column('hreport_id', BIGINT(20), nullable=False),
    Column('tenant_id', String(256), nullable=False),
    Column('project_id', BIGINT(20), nullable=False),
    Column('insert_date', DateTime, nullable=False, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


class HreportSetting(Base):
    __tablename__ = 'hreport_settings'

    hreport_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    hreport_name = Column(String(256), nullable=False)
    report_type = Column(INTEGER(11), server_default=text("-1"))
    period_type = Column(INTEGER(11), server_default=text("-1"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    row_group1 = Column(INTEGER(11), server_default=text("-1"))
    row_group2 = Column(INTEGER(11), server_default=text("-1"))
    row_group3 = Column(INTEGER(11), server_default=text("-1"))
    show_zero = Column(TINYINT(1), server_default=text("0"))
    noans_sec = Column(INTEGER(11))
    csv_send_type = Column(INTEGER(11), server_default=text("-1"))
    csv_send_week = Column(INTEGER(11), server_default=text("-1"))
    csv_send_day = Column(INTEGER(11), server_default=text("-1"))
    csv_send_hour = Column(INTEGER(11), server_default=text("-1"))
    csv_send_minute = Column(INTEGER(11), server_default=text("-1"))
    csv_mail = Column(String(512))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


t_hreport_skill_cols = Table(
    'hreport_skill_cols', metadata,
    Column('id', BIGINT(20), nullable=False, unique=True),
    Column('hreport_id', BIGINT(20), nullable=False),
    Column('tenant_id', String(256), nullable=False),
    Column('show_skill_name', TINYINT(1), server_default=text("0")),
    Column('show_skill_id', TINYINT(1), server_default=text("0")),
    Column('show_incoming_cnt', TINYINT(1), server_default=text("0")),
    Column('show_ans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_noans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_ans_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_ans_time_max', TINYINT(1), server_default=text("0")),
    Column('show_noans_time_max', TINYINT(1), server_default=text("0")),
    Column('show_talk_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_talk_time_max', TINYINT(1), server_default=text("0")),
    Column('show_talk_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_acw_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_acw_time_max', TINYINT(1), server_default=text("0")),
    Column('show_hold_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_hold_time_max', TINYINT(1), server_default=text("0")),
    Column('order_setting', Text),
    Column('insert_date', DateTime, nullable=False, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


class HreportSkill(Base):
    __tablename__ = 'hreport_skills'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(BIGINT(20), nullable=False)
    tenant_id = Column(String(256), nullable=False)
    group_id = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


t_hreport_user_cols = Table(
    'hreport_user_cols', metadata,
    Column('id', BIGINT(20), nullable=False, unique=True),
    Column('hreport_id', BIGINT(20), nullable=False),
    Column('tenant_id', String(256), nullable=False),
    Column('show_user_ext', TINYINT(1), server_default=text("0")),
    Column('show_user_id', TINYINT(1), server_default=text("0")),
    Column('show_user_name', TINYINT(1), server_default=text("0")),
    Column('show_out_call_cnt', TINYINT(1), server_default=text("0")),
    Column('show_out_talk_cnt', TINYINT(1), server_default=text("0")),
    Column('show_out_noans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_out_hold_cnt', TINYINT(1), server_default=text("0")),
    Column('show_out_hold_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_out_hold_time_max', TINYINT(1), server_default=text("0")),
    Column('show_out_hold_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_out_acw_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_out_acw_time_max', TINYINT(1), server_default=text("0")),
    Column('show_out_acw_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_out_talk_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_out_talk_time_max', TINYINT(1), server_default=text("0")),
    Column('show_out_talk_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_out_trans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_out_anstrans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_in_incoming_cnt', TINYINT(1), server_default=text("0")),
    Column('show_in_ans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_in_noans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_in_hold_cnt', TINYINT(1), server_default=text("0")),
    Column('show_in_avail_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_acw_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_acw_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_in_acw_time_max', TINYINT(1), server_default=text("0")),
    Column('show_in_auxdetail_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_auxdetail_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_in_aux_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_in_login_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_ans_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_in_ans_time_max', TINYINT(1), server_default=text("0")),
    Column('show_in_noans_time_max', TINYINT(1), server_default=text("0")),
    Column('show_in_talk_avg', TINYINT(1), server_default=text("0")),
    Column('show_in_talk_max', TINYINT(1), server_default=text("0")),
    Column('show_in_talk_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_trans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_in_anstrans_cnt', TINYINT(1), server_default=text("0")),
    Column('show_in_monitor_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_coach_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_hold_time_avg', TINYINT(1), server_default=text("0")),
    Column('show_in_hold_time_max', TINYINT(1), server_default=text("0")),
    Column('show_in_hold_time_sum', TINYINT(1), server_default=text("0")),
    Column('show_in_memo', TINYINT(1), server_default=text("0")),
    Column('order_setting', Text),
    Column('insert_date', DateTime, nullable=False, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


class HreportUser(Base):
    __tablename__ = 'hreport_users'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    hreport_id = Column(BIGINT(20), nullable=False)
    tenant_id = Column(String(256), nullable=False)
    group_id = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


t_ng_word_data = Table(
    'ng_word_data', metadata,
    Column('ng_word_id', BIGINT(20), nullable=False, unique=True),
    Column('tenant_id', String(256), nullable=False),
    Column('ng_list_id', BIGINT(20), nullable=False),
    Column('ng_word', String(256), nullable=False),
    Column('insert_date', DateTime, nullable=False, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


t_ng_word_lists = Table(
    'ng_word_lists', metadata,
    Column('ng_list_id', BIGINT(20), nullable=False, unique=True),
    Column('tenant_id', String(256), nullable=False),
    Column('ng_list_name', String(256), nullable=False),
    Column('insert_date', DateTime, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


class OperationLog(Base):
    __tablename__ = 'operation_logs'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    operation_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    user_id = Column(String(256), nullable=False)
    view_id = Column(BIGINT(20))
    operation = Column(INTEGER(11))
    detail = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class OperationView(Base):
    __tablename__ = 'operation_views'

    view_id = Column(BIGINT(20), primary_key=True, unique=True)
    view_name = Column(String(512), nullable=False)
    view_keyword = Column(String(128))
    list_cnt_reference = Column(String(64))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class VoiceMails(Base):
   __tablename__ = 'voice_mails'

   voicemail_id = Column(BIGINT(20), primary_key=True, nullable=False)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   save_date = Column(DateTime, nullable=False)
   incoming_date = Column(DateTime, nullable=False)
   recording_time = Column(TIME, nullable=False)
   project_id = Column(ForeignKey(Project.project_id))
   customer_telnum = Column(VARCHAR(64), server_default=text("1"))
   status = Column(INTEGER(11))
   user_id = Column(ForeignKey(User.user_id))
   detail = Column(TEXT)
   recording_path = Column(TEXT)
   insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

   tenant = relationship(Tenant)
   project = relationship(Project)
   user = relationship(User)


class ProjectFagword(Base):
    __tablename__ = 'project_fagwords'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256))
    project_id = Column(BIGINT(20))
    faq_list_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class ProjectNgword(Base):
    __tablename__ = 'project_ngwords'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256))
    project_id = Column(BIGINT(20))
    ng_list_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    project_name = Column(String(256), nullable=False)
    dial_in = Column(String(64))
    chennel_cnt = Column(INTEGER(11))
    flow_id = Column(BIGINT(20))
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


class RecDownloadProject(Base):
    __tablename__ = 'rec_download_projects'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    proc_id = Column(BIGINT(20))
    project_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class RecDownloadSetting(Base):
    __tablename__ = 'rec_download_settings'

    proc_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    user_id = Column(String(256), nullable=False)
    proc_sts = Column(INTEGER(11))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    file_format = Column(INTEGER(11))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class RecDownloadZipfile(Base):
    __tablename__ = 'rec_download_zipfiles'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    proc_id = Column(BIGINT(20))
    zipfile_path = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class RecordingExcludedProject(Base):
    __tablename__ = 'recording_excluded_projects'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    setting_id = Column(BIGINT(20), nullable=False)
    project_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class RecordingExcludedUser(Base):
    __tablename__ = 'recording_excluded_users'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    setting_id = Column(BIGINT(20), nullable=False)
    user_id = Column(String(256))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


t_responding_memo = Table(
    'responding_memo', metadata,
    Column('memo_id', BIGINT(20), nullable=False, unique=True),
    Column('tenant_id', String(256), nullable=False),
    Column('memo_name', String(512), nullable=False),
    Column('insert_date', DateTime, nullable=False, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


class RetentionPeriod(Base):
    __tablename__ = 'retention_periods'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    report_days = Column(INTEGER(11), server_default=text("0"))
    recording_days = Column(INTEGER(11), server_default=text("0"))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class RreportProject(Base):
    __tablename__ = 'rreport_projects'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    rreport_id = Column(BIGINT(20), nullable=False, index=True)
    tenant_id = Column(String(256), nullable=False)
    project_id = Column(BIGINT(20), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class RreportSetting(Base):
    __tablename__ = 'rreport_settings'

    rreport_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
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


class Seatview(Base):
    __tablename__ = 'seatviews'

    seatview_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    seatview_name = Column(String(256), nullable=False)
    acw_color = Column(String(64))
    acw_threshold_1 = Column(INTEGER(11))
    acw_threshold_2 = Column(INTEGER(11))
    talk_color = Column(String(64))
    talk_threshold_1 = Column(INTEGER(11))
    talk_threshold_2 = Column(INTEGER(11))
    aux_color = Column(String(64))
    aux_threshold_1 = Column(INTEGER(11))
    aux_threshold_2 = Column(INTEGER(11))
    view_setting = Column(LONGTEXT)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class SecuritySetting(Base):
    __tablename__ = 'security_settings'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    use_password_policy = Column(TINYINT(1), server_default=text("0"))
    password_length = Column(INTEGER(11), server_default=text("1"))
    use_upper = Column(TINYINT(1), server_default=text("0"))
    use_lower = Column(TINYINT(1), server_default=text("0"))
    use_digit = Column(TINYINT(1), server_default=text("0"))
    use_symbol = Column(TINYINT(1), server_default=text("0"))
    use_forced_mix = Column(TINYINT(1), server_default=text("0"))
    mix_cnt = Column(INTEGER(11), server_default=text("1"))
    use_expiration = Column(TINYINT(1), server_default=text("0"))
    effective_days = Column(INTEGER(11), server_default=text("1"))
    use_check_generations = Column(TINYINT(1), server_default=text("0"))
    generations_cnt = Column(INTEGER(11), server_default=text("1"))
    use_account_lock = Column(TINYINT(1), server_default=text("0"))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class Setting(Base):
    __tablename__ = 'settings'

    setting_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
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
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    skill_id = Column(String(256), primary_key=True, nullable=False)
    tenant_id = Column(String(256), primary_key=True, nullable=False)
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


class SmsAuthenticator(Base):
    __tablename__ = 'sms_authenticators'

    sms_auth_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    sms_auth_name = Column(String(256))
    partner = Column(INTEGER(11), server_default=text("-1"))
    account_id = Column(String(256))
    request_id = Column(String(256))
    request_password = Column(String(256))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class SmsSetting(Base):
    __tablename__ = 'sms_settings'

    setting_id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    setting_name = Column(String(256))
    sms_context = Column(Text)
    sms_auth_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)


t_sound_files = Table(
    'sound_files', metadata,
    Column('sound_id', BIGINT(20), nullable=False, unique=True),
    Column('tenant_id', String(256), nullable=False),
    Column('sound_name', String(256), nullable=False),
    Column('location_path', Text),
    Column('sound_type', INTEGER(11), server_default=text("0")),
    Column('insert_date', DateTime, nullable=False, server_default=text("current_timestamp()")),
    Column('update_date', DateTime, nullable=False, server_default=text("current_timestamp()"))
)


class SoundSetting(Base):
    __tablename__ = 'sound_setting'

    id = Column(BIGINT(20), primary_key=True)
    tenant_id = Column(String(256), nullable=False)
    outside_sound_id = Column(BIGINT(20))
    outside_volume = Column(INTEGER(11), server_default=text("1"))
    extension_sound_id = Column(BIGINT(20))
    extension_volume = Column(INTEGER(11), server_default=text("1"))
    hold_sound_id = Column(BIGINT(20))
    hold_volume = Column(INTEGER(11), server_default=text("1"))
    sound_quality = Column(INTEGER(11), server_default=text("0"))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class SpeechExcludedProject(Base):
    __tablename__ = 'speech_excluded_projects'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    setting_id = Column(BIGINT(20))
    project_id = Column(BIGINT(20))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class SpeechExcludedUser(Base):
    __tablename__ = 'speech_excluded_users'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    setting_id = Column(BIGINT(20))
    user_id = Column(String(256))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class TalkScript(Base):
    __tablename__ = 'talk_scripts'

    script_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    script_name = Column(String(256), nullable=False)
    summary = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class Tenant(Base):
    __tablename__ = 'tenant'
    __table_args__ = {'comment': 'Tenant : All information about tenant'}

    tenant_id = Column(String(256), primary_key=True, comment='tenant_id : id of tenant')
    tenant_name = Column(String(256), comment=' tenant_name : name of tenant')
    domain = Column(String(45), comment='domain : domain of tenant,')
    prefix = Column(INTEGER(11), comment='prefix : prefix of tenant, ex a number as 01, 02 ')
    identifier = Column(String(256), comment='identifier : identifier of tenant, ex ABC-01a')
    channel_cnt = Column(INTEGER(11), comment='channel_cnt : number of maximum channel of tenant')
    use_speech_to_text = Column(TINYINT(4), comment='use_speech_to_text : 0 is off, 1 is on speech_to_text')
    st_engine = Column(INTEGER(11), comment='st_engine : Choose between Ami voice or Google speak to text')
    insert_date = Column(DateTime, comment='insert_date : registration date')
    update_date = Column(DateTime, comment='update_date : Last time tenant is changed')


class Threshold(Base):
    __tablename__ = 'threshold'

    threshold_id = Column(INTEGER(11), primary_key=True)
    tenant_id = Column(INTEGER(11))
    seat_view_id = Column(INTEGER(11))
    post_procesing = Column(INTEGER(1))
    tallking = Column(INTEGER(1))
    leave_seat = Column(INTEGER(1))
    threshold_first = Column(INTEGER(11))
    threshold_second = Column(INTEGER(11))


class Token(Base):
    __tablename__ = 'token'
    __table_args__ = {'comment': 'Token : Manage token of each user for authentication'}

    user_id = Column(String(256), primary_key=True, comment='User Id')
    token_id = Column(VARCHAR(60), unique=True, comment='Token Id : Each user has an unique token_id')
    expired_date = Column(INTEGER(11), comment='Expired Time : Expired time of token')
    create_date = Column(INTEGER(11), comment='Create Date : Created Date of token')


class TriggerCondition(Base):
    __tablename__ = 'trigger_conditions'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    trigger_id = Column(BIGINT(20), nullable=False)
    cond_action = Column(INTEGER(11))
    project_id = Column(BIGINT(20))
    skill_id = Column(String(256))
    call_status = Column(INTEGER(11))
    _condition = Column(INTEGER(11))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class TriggerContent(Base):
    __tablename__ = 'trigger_contents'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    trigger_id = Column(BIGINT(20), nullable=False)
    impl_action = Column(INTEGER(11))
    script_id = Column(BIGINT(20))
    url = Column(String(2048))
    method = Column(String(32))
    req_header = Column(Text)
    req_body = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class Trigger(Base):
    __tablename__ = 'triggers'

    trigger_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), nullable=False)
    trigger_name = Column(String(256), nullable=False)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class UserRecord(Base):
    __tablename__ = 'user_records'

    user_record_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256))
    user_id = Column(String(256))
    acd_status = Column(INTEGER(11))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    aux_detail = Column(BIGINT(20))
    incoming_skill = Column(String(256))
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)


class AwayReason(Base):
    __tablename__ = 'away_reason'
    __table_args__ = {'comment': 'Away Reason : Away Reason'}

    id = Column(BIGINT(20), primary_key=True, unique=True, comment='Id')
    tenant_id = Column(ForeignKey('tenant.tenant_id'), index=True, comment='Tenant Id : Tenant Id which these away reasons are belong to')
    away_reason = Column(String(1024), comment='Away Reason : Content of Away reason')
    is_display = Column(TINYINT(1), comment='Is Display : 0 is not displayed, 1 is displayed')
    update_date = Column(DateTime, comment='Update date : Last time that away reason is changed')

    tenant = relationship('Tenant')


class DashboardItem(Base):
    __tablename__ = 'dashboard_item'

    item_id = Column(INTEGER(11), primary_key=True)
    tenant_id = Column(INTEGER(11))
    dashboard_id = Column(ForeignKey('dashboard.dashboard_id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    report_type = Column(INTEGER(1))
    graph_type = Column(String(45))
    coordinate = Column(NullType)
    last_change_date = Column(DateTime)

    dashboard = relationship('Dashboard')


class SkillAssignment(Base):
    __tablename__ = 'skill_assignments'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(ForeignKey('tenant.tenant_id'), nullable=False, index=True)
    skill_id = Column(String(256), nullable=False)
    user_id = Column(String(256), nullable=False)
    skill_level = Column(INTEGER(11), server_default=text("-1"))
    insert_date = Column(DateTime, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, server_default=text("current_timestamp()"))

    tenant = relationship('Tenant')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Users : User information'}

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True, comment='id')
    tenant_id = Column(ForeignKey('tenant.tenant_id'), primary_key=True, nullable=False, index=True, comment='Tenant Id')
    user_id = Column(ForeignKey('token.user_id'), primary_key=True, nullable=False, index=True, comment='User ID')
    user_name = Column(VARCHAR(256), comment='Username : Username is used to login collabos by user')
    password = Column(VARCHAR(1024), comment='Password')
    mail = Column(VARCHAR(256), comment='Email : Email address of user')
    group_id = Column(VARCHAR(256), comment='Group Id : Id of group which user is belong to')
    device = Column(INTEGER(11), comment='Device : Device that user is using')
    autoin_time = Column(INTEGER(11), comment='Auto In Time : Time that after ending call, user can receive new call')
    auth_id = Column(BIGINT(20), comment='Authority Id : privilege that user is permitted what features to use')
    extension = Column(String(64), comment='Extension Number : Extension number is number that end-user can contact with user via it')
    locked = Column(TINYINT(1), comment='Lock State : 0 is not locked, 1 is locked')
    locked_date = Column(DateTime, comment='Locked date : Last date that state of user is locked')
    login_ng_cnt = Column(INTEGER(11), comment='Login fail consecutive : Number of time that user logged in collabos fail in row')
    user_classifier = Column(INTEGER(11), comment='User Classification : 0 is normal user, 1 is tenant user, 2 is collabos adminitrator')
    insert_date = Column(DateTime, comment='Insert Date : Time that user is created')
    update_date = Column(DateTime, comment='Update Date : Last time that user info is changed')
    firstname = Column(VARCHAR(1024), comment='First Name')
    lastname = Column(VARCHAR(1024), comment='Last Name')
    middlename = Column(VARCHAR(1024), comment='Middle Name')
    project_id = Column(BIGINT(20), comment='Project Id : Project which user is belong')

    tenant = relationship('Tenant')
    user = relationship('Token')


class VoiceRecognition(Base):
    __tablename__ = 'voice_recognition'

    voice_reg_id = Column(INTEGER(11), primary_key=True)
    tenant_id = Column(INTEGER(11))
    call_start_datetime = Column(DateTime)
    call_end_datetime = Column(DateTime)
    duration_of_call = Column(INTEGER(11))
    response_agent = Column(VARCHAR(50))
    extension_number = Column(VARCHAR(10))
    after_customer_phone_number = Column(VARCHAR(50))
    call_direction = Column(INTEGER(11))
    corresponding_memo_id = Column(ForeignKey('correspondence_memo.correspondence_memo_id'), index=True)
    call_id = Column(INTEGER(11))

    corresponding_memo = relationship('CorrespondenceMemo')
