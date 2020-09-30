# create_tables.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://ivr:ROOT@mysql123@192.168.11.206/test')
Base = declarative_base()


class Holiday(Base):
    __tablename__ = 't_sip_holiday'
    c_acdcode = Column(String(8), primary_key=True)
    c_date = Column(String(8), primary_key=True)
    c_datetype = Column(String(1))
    c_desc = Column(String(255))


class TimeTable(Base):
    __tablename__ = 't_sip_timetable'
    c_acdcode = Column(String(4), primary_key=True)
    c_datetype = Column(String(1), primary_key=True)  #0 : Sunday, ~ 6:Saturday
    c_timetype = Column(String(1), primary_key=True)  #1 : WorkTime  2: BreakTime
    c_starttime = Column(String(4))
    c_endtime = Column(String(4))
    c_desc = Column(String(255))


Base.metadata.create_all(engine)  