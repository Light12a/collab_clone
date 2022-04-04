from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from services.database.mysqldb import Base


class OperationView(Base):
   __tablename__ = 'operation_views'

   view_id = Column(BIGINT(20), primary_key=True, unique=True)
   view_name = Column(String(512), nullable=False)
   view_keyword = Column(String(128))
   list_cnt_reference = Column(String(64))
   insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))


class OperationLog(Base):
   __tablename__ = 'operation_logs'

   id = Column(BIGINT(20), primary_key=True, unique=True)
   tenant_id = Column(String(256), nullable=False)
   operation_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
   user_id = Column(String(256), nullable=False)
   view_id = Column(ForeignKey(OperationView.view_id))
   operation = Column(INTEGER(11))
   detail = Column(Text)
   insert_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
   update_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

   operation_views = relationship(OperationView)
