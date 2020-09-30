from wtforms import Form, StringField, SelectField, validators

class HolidayForm(Form):
    c_date = StringField('Day(YYYYMMDD)')
    c_desc = StringField('Description')

class TimeTableForm(Form):
    c_starttime = StringField('StartTime(HHMM)')
    c_endtime = StringField('EndTime(HHMM)')
