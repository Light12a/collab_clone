from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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


class Token(Base):
   __tablename__ = 'token'
   __table_args__ = {'comment': 'Token : Manage token of each user for authentication'}

   user_id = Column(String(256), primary_key=True, comment='User Id')
   token_id = Column(VARCHAR(60), unique=True, comment='Token Id : Each user has an unique token_id')
   expired_date = Column(INTEGER(11), comment='Expired Time : Expired time of token')
   create_date = Column(INTEGER(11), comment='Create Date : Created Date of token')


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
