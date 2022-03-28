from turtle import back
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Users : User information'}

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True, comment='id')
    tenant_id = Column(ForeignKey(Tenant.tenant_id), primary_key=True, nullable=False, index=True, comment='Tenant Id')
    user_id = Column(VARCHAR(256), primary_key=True, nullable=False, index=True, comment='User ID')
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
    sound_id = Column(INTEGER(11), comment="Sound Id: ringtone which user have selected" )
    tenant = relationship(Tenant)

    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class Token(Base):
    __tablename__ = 'token'
    __table_args__ = {'comment': 'Token : Manage token of each user for authentication'}

    user_id = Column(ForeignKey(User.user_id), primary_key=True,nullable=False, index=True, comment='User Id')
    token_id = Column(VARCHAR(512), unique=True, comment='Token Id : Each user has an unique token_id')
    expired_date = Column(BIGINT(20), comment='Expired Time : Expired time of token')
    create_date = Column(DateTime, comment='Create Date : Created Date of token')

    user = relationship(User)

class UserRecord(Base):
    __tablename__ = 'user_records'

    user_record_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256))
    user_id = Column(String(256))
    acd_status = Column(INTEGER(11))
    sub_status = Column(INTEGER(11))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    aux_detail = Column(BIGINT(20))
    incoming_skill = Column(String(256))
    insert_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)
    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
# class AwayReason(Base):
#     __tablename__ = 'away_reason'
#     __table_args__ = {'comment': 'Away Reason : Away Reason'}

#     id = Column(BIGINT(20), primary_key=True, unique=True, comment='Id')
#     tenant_id = Column(index=True, comment='Tenant Id : Tenant Id which these away reasons are belong to')
#     away_reason = Column(String(1024), comment='Away Reason : Content of Away reason')
#     is_display = Column(TINYINT(1), comment='Is Display : 0 is not displayed, 1 is displayed')
#     update_date = Column(DateTime, comment='Update date : Last time that away reason is changed')
    #tenant = relationship(Tenant)

    # def to_json(self):
    #     return {c.key: getattr(self, c.key)
    #             for c in inspect(self).mapper.column_attrs}