from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
from ..groups.models import Group
from services.database.mysqldb import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Users : User information'}

    id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True, comment='id')
    tenant_id = Column(ForeignKey(Tenant.tenant_id), primary_key=True, nullable=False, index=True, comment='Tenant Id')
    user_id = Column(VARCHAR(256), primary_key=True, nullable=False, index=True, comment='User ID')
    user_name = Column(VARCHAR(256), comment='Username : Username is used to login collabos by user')
    password = Column(VARCHAR(1024), comment='Password')
    mail = Column(VARCHAR(256), comment='Email : Email address of user')
    group_id = Column(ForeignKey(Group.group_id), comment='Group Id : Id of group which user is belong to')
    device = Column(INTEGER(11), comment='Device : Device that user is using')
    autoin_time = Column(INTEGER(11), comment='Auto In Time : Time that after ending call, user can receive new call')
    auth_id = Column(BIGINT(20), comment='Authority Id : privilege that user is permitted what features to use')
    extension = Column(String(64), comment='Extension Number : Extension number is number that end-user can contact with user via it')
    locked = Column(TINYINT(1), comment='Lock State : 0 is not locked, 1 is locked')
    locked_date = Column(DateTime, comment='Locked date : Last date that state of user is locked')
    login_ng_cnt = Column(INTEGER(11), comment='Login fail consecutive : Number of time that user logged in collabos fail in row')
    user_classifier = Column(INTEGER(11), comment='User Classification : 0 is normal user, 1 is tenant user, 2 is collabos adminitrator')
    insert_date = Column(DateTime,nullable=False, server_default=text("current_timestamp()"), comment='Insert Date : Time that user is created')
    update_date = Column(DateTime,nullable=False, server_default=text("current_timestamp()"), comment='Update Date : Last time that user info is changed')
    firstname = Column(VARCHAR(1024), comment='First Name')
    lastname = Column(VARCHAR(1024), comment='Last Name')
    middlename = Column(VARCHAR(1024), comment='Middle Name')

    tenant = relationship(Tenant)
<<<<<<< HEAD
    group = relationship(Group)
=======
    
    def to_json(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}
>>>>>>> 37f514e... fix some minor bugs


class Token(Base):
    __tablename__ = 'token'
    __table_args__ = {'comment': 'Token : Manage token of each user for authentication'}

    user_id = Column(ForeignKey(User.user_id), primary_key=True,nullable=False, index=True, comment='User Id')
    token_id = Column(VARCHAR(60), unique=True, comment='Token Id : Each user has an unique token_id')
    expired_date = Column(BIGINT(20), comment='Expired Time : Expired time of token')
    create_date = Column(DateTime, comment='Create Date : Created Date of token')

    user = relationship(User)