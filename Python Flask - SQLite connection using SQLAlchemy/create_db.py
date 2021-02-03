# create_tables.py
from sqlalchemy import create_engine, ForeignKey, Index
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////usr/local/src/study/flask_sqlite/callback.db')
Base = declarative_base()


class callback(Base):
    __tablename__ = 't_callback'
    c_date = Column(String(8), primary_key=True)
    c_time = Column(String(8), primary_key=True)
    c_ani = Column(String, primary_key=True)
    c_dnis = Column(String, nullable=False)
    c_callback_num = Column(String)
    c_callback_date = Column(String(8))
    c_callback_time = Column(String(8))
    c_complete = Column(String(1),index=True)  #Y:completed , N:Not completed
    c_del = Column(String(1))       #Y:deleted , N:Not deleted

#callback_index = Index('callback_idx', callback.c_complete)

Base.metadata.create_all(engine) 
print(engine)
