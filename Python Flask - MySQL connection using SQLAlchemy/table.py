from flask_table import Table, Col, LinkCol

class HolidayResults(Table):
    c_acdcode = Col('c_acdcode')
    c_date = Col('c_date')
    c_datetype = Col('c_datetype')
    c_desc = Col('c_desc')
    edit = LinkCol('  Modify  ', 'holiday_edit', url_kwargs=dict(edit_date='c_date'))
    delete = LinkCol('  Delete  ', 'holiday_del', url_kwargs=dict(del_date='c_date'))


class TimeTableResults(Table):
    c_acdcode = Col('c_acdcode')
    c_datetype = Col('c_datetype')
    c_timetype = Col('c_timetype')
    c_starttime = Col('c_starttime')
    c_endtime = Col('c_endtime')
    c_desc = Col('c_desc')
    edit = LinkCol('  Modify  ', 'timetable_edit', url_kwargs=dict(edit_datetype='c_datetype', edit_timetype = 'c_timetype'))
