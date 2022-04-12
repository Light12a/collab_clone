from sqlalchemy import Column, Date, DateTime, ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, BOOLEAN
from sqlalchemy.orm import relationship
from handlers.tenant_settings.models import Tenant
from services.database.mysqldb import Base


class SecuritySetting(Base):
   __tablename__ = 'security_settings'

   id = Column(BIGINT(20), primary_key=True, unique=True, nullable=False)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   use_password_policy = Column(BOOLEAN, server_default=False)
   password_length = Column(INTEGER(11), server_default=text("1"))
   use_upper = Column(BOOLEAN, server_default=False)
   use_lower = Column(BOOLEAN, server_default=False)
   use_digit = Column(BOOLEAN, server_default=False)
   use_symbol = Column(BOOLEAN, server_default=False)
   use_forced_mix = Column(BOOLEAN, server_default=False)
   mix_cnt = Column(INTEGER(11), server_default=text("1"))
   use_expiration = Column(BOOLEAN, server_default=False)
   effective_days = Column(INTEGER(11), server_default=text("1"))
   use_check_generations = Column(BOOLEAN, server_default=False)
   generations_cnt = Column(INTEGER(11), server_default=text("1"))
   use_account_lock = Column(BOOLEAN, server_default=False)
   insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

   tenant = relationship(Tenant)
