from utils.config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Create engine sql
Base = declarative_base()

class SQLChemyConnection(object):
    def __init__(self) -> None:
        self.host = config['db_local']['host']
        self.user = config['db_local']['user']
        self.password = config['db_local']['password']
        self.database = config['db_local']['database']
        self.engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                   (self.user, self.password, self.host, self.database),
                   encoding='utf-8', echo=False,
                   pool_size=100, pool_recycle=10)

    