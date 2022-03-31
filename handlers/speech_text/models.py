from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from handlers.users.models import Token, User
from handlers.tenant_settings.models import Tenant
from services.database.mysqldb import Base


class FaqWordLists(Base):
   __tablename__ = 'faq_word_lists'

   faq_list_id = Column(BIGINT(20), primary_key=True)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   faq_list_name = Column(String(256), nullable=False)
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))

   tenant = relationship(Tenant)


class FaqWordData(Base):
   __tablename__ = 'faq_word_data'

   faq_word_id = Column(BIGINT(20), primary_key=True)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   faq_list_id = Column(ForeignKey(FaqWordLists.faq_list_id), nullable=False)
   faq_word = Column(String(255), nullable=False)
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))

   tenant = relationship(Tenant)
   faq_word_lists = relationship(FaqWordLists)


class NgWordLists(Base):
   __tablename__ = 'ng_word_lists'

   ng_list_id = Column(BIGINT(20), primary_key=True)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   ng_list_name = Column(String(256), nullable=False)
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))

   tenant = relationship(Tenant)


class NgWordData(Base):
   __tablename__ = 'ng_word_data'

   ng_word_id = Column(BIGINT(20), primary_key=True)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   ng_list_id = Column(ForeignKey(NgWordLists.ng_list_id), nullable=False)
   ng_word = Column(String(256), nullable=False)
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))

   tenant = relationship(Tenant)
   ng_word_lists = relationship(NgWordLists)


class FaqPartners(Base):
   __tablename__ = 'faq_partners'

   faq_partner_id = Column(BIGINT(20), primary_key=True)
   tenant_id = Column(ForeignKey(Tenant.tenant_id), nullable=False)
   faq_partner_name = Column(String(256), nullable=False)
   url = Column(String(256), nullable=False)
   login_id = Column(String(256))
   password = Column(String(256))
   insert_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False,
                        server_default=text("current_timestamp()"))

   tenant = relationship(Tenant)
