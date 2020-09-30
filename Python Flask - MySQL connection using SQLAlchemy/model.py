# models.py 

from app import db

class Holiday(db.Model):
    __tablename__ = 't_sip_holiday'
    c_acdcode = db.Column(db.String(8), primary_key=True)
    c_date = db.Column(db.String(8), primary_key=True)
    c_datetype = db.Column(db.String(1))
    c_desc = db.Column(db.String(255))

    def __init__(self, c_acdcode, c_date, c_datetype, c_desc):
        self.c_acdcode = c_acdcode
        self.c_date = c_date
        self.c_datetype = c_datetype
        self.c_desc = c_desc

    def __repr__(self):
        return "<holiday('%s', '%s', '%s', '%s')>" % (self.c_acd, self.c_date, self.c_datetype, self.c_desc)
		
class TimeTable(db.Model):
    __tablename__ = 't_sip_timetable'
    c_acdcode = db.Column(db.String(4), primary_key=True)
    c_datetype = db.Column(db.String(1), primary_key=True)  #0 : Sunday, ~ 6:Saturday
    c_timetype = db.Column(db.String(1), primary_key=True)  #1 : WorkTime  2: BreakTime
    c_starttime = db.Column(db.String(4))
    c_endtime = db.Column(db.String(4))
    c_desc = db.Column(db.String(255))

    def __init__(self, c_acdcode, c_datetype, c_timetype, c_starttime, c_endtime, c_desc):
        self.c_acdcode = c_acdcode
        self.c_datetype = c_datetype
        self.c_timetype = c_timetype
        self.c_starttime = c_starttime
        self.c_endtime = c_endtime
        self.c_desc = c_desc

    def __repr__(self):
        return "<time table('%s', '%s', '%s', '%s', '%s', '%s')>" % (self.c_acdcode, self.c_datetype, self.c_timetype, self.c_starttime, self.c_endtime, self.c_desc)
		
