from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,mapped_column,Mapped
from sqlalchemy.ext.declarative import declarative_base,as_declarative,declared_attr

from datetime import datetime

from . import config

engine =  create_engine(url=config.get_db_url_str())

session_local = sessionmaker(bind=engine,autoflush=False,autocommit=False)
 
@as_declarative()
class Base(object):
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
        
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,sort_order=-1)
    created_on:Mapped[datetime] = mapped_column(default=datetime.now)
    last_updated:Mapped[datetime] = mapped_column(onupdate=datetime.now)

def create_db_table():
    Base.metadata.create_all(engine)
        
def get_db():
    
    db =  session_local()
    
    try:
        yield db

    except Exception as e:
        db.close()
        raise e

