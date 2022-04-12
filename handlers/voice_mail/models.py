from sqlalchemy import Column, DateTime, ForeignKey, text, TIME, TEXT
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, BOOLEAN, VARCHAR
from sqlalchemy.orm import relationship
from handlers.tenant_settings.models import Tenant
from handlers.project_settings.models import Project
from handlers.users.models import User
from services.database.mysqldb import Base


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
