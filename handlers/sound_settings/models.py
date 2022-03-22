from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text, Time, text, inspect
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from ..tenant_settings.models import Tenant
Base = declarative_base()
metadata = Base.metadata

class SoundFiles(Base): 
    __tablename__ = 'sound_files'

    sound_id = Column(BIGINT(20), primary_key=True, nullable=False, unique=True)
    tenant_id = Column(String(256), nullable=False)
    sound_name = Column(String(256), nullable=False)
    location_path = Column(Text)
    sound_type = Column(INTEGER(11), server_default=text("0"))
    insert_data = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    update_data = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    def to_json(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}

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


