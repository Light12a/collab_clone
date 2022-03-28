from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from handlers.tenant_settings.models import Tenant
from handlers.users.models import User
from handlers.project_settings.models import Project
from services.database.mysqldb import Base

class RecDownloadSetting(Base):
    __tablename__ = 'rec_download_settings'

    proc_id = Column(BIGINT(20), primary_key=True, unique=True)
    tenant_id = Column(String(256), ForeignKey(Tenant.tenant_id), nullable=False)
    user_id = Column(String(256), ForeignKey(User.user_id), nullable=False)
    proc_sts = Column(INTEGER(11))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    file_format = Column(INTEGER(11))
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    tenant = relationship(Tenant, backref='rec_download')
    user = relationship(User, backref='rec_download')


class RecDownloadProject(Base):
    __tablename__ = 'rec_download_projects'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    proc_id = Column(BIGINT(20), ForeignKey(RecDownloadSetting.proc_id), nullable=False)
    project_id = Column(BIGINT(20), ForeignKey(Project.project_id), nullable=True)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    
    rec_download = relationship(RecDownloadSetting, backref='rec_download_project')
    project = relationship(Project, backref='rec_download_project')

class RecDownloadZipfile(Base):
    __tablename__ = 'rec_download_zipfiles'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    proc_id = Column(BIGINT(20), ForeignKey(RecDownloadSetting.proc_id), nullable=False)
    zipfile_path = Column(Text)
    insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    rec_download = relationship(RecDownloadSetting, backref='rec_download_project')