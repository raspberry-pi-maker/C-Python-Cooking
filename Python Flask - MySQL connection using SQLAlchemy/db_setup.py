# db_setup.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import  my_ip

engine = create_engine('mysql://ivr:ROOT@mysql123@%s/test'%(my_ip), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import model
    print('Create tables if not exists')
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()    
