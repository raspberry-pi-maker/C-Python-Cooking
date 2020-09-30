#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# main.py
from app import app, db
from db_setup import init_db, db_session
from holidayform import HolidayForm, TimeTableForm
from flask import flash, render_template, request, redirect
from model import Holiday, TimeTable
from table import HolidayResults, TimeTableResults
import pidfile
import os, sys
import signal


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/holiday', methods=['GET', 'POST'])
def holiday_main():
    results = []
    qry = db_session.query(Holiday).filter(Holiday.c_acdcode=='0202')
    results = qry.all()
    if results:
        table = HolidayResults(results)
        table.border = True
    return render_template("holiday.html", table=table)
   
@app.route('/worktime', methods=['GET', 'POST'])
def worktime_main():
    results = []
    qry = db_session.query(TimeTable).filter(TimeTable.c_acdcode=='0202')
    results = qry.all()
    if results:
        table = TimeTableResults(results)
        table.border = True
    return render_template("worktime.html", table=table)

@app.route('/new_holiday', methods=['GET', 'POST'])
def new_holiday():
    """
    Add a new holiday
    """
    form = HolidayForm(request.form)
    if request.method == 'POST' and form.validate():
        h_desc = form.c_desc.data.encode("utf-8", errors="ignore").decode("utf-8")
        h_date = form.c_date.data

        # print('return value:%s %s'%(h_date, h_desc))
        # print('return value:%s %s'%(type(form.t_date.data), len(form.t_desc.data)))
        hday = Holiday(c_acdcode = "0202", c_date = h_date, c_datetype = "7", c_desc = h_desc)
        # print('Object value : %s %s'%(hday.t_date, hday.t_desc))
        db_session.add(hday)
        db_session.commit()

        return redirect('/holiday')
    return render_template('new_holiday.html', form=form)

@app.route('/holiday_del/<string:del_date>', methods=['GET', 'POST'])
def holiday_del(del_date):
    print('holiday del')
    qry = db_session.query(Holiday).filter(Holiday.c_acdcode=='0202').filter(Holiday.c_date == del_date)
    hday = qry.first()
    db_session.delete(hday)
    db_session.commit()    
    print('Holiday delete successfully!')
    return redirect('/holiday')

@app.route('/holiday_edit/<string:edit_date>', methods=['GET', 'POST'])
def holiday_edit(edit_date):
    print('holiday edit [%s] '%edit_date)
    qry = db_session.query(Holiday).filter(Holiday.c_acdcode=='0202').filter(Holiday.c_date == edit_date)
    hday = qry.first()
    form = HolidayForm(formdata=request.form, obj=hday)

    if request.method == 'POST' and form.validate():
        hday.c_date = form.c_date.data      
        hday.c_desc = form.c_desc.data.encode("utf-8", errors="ignore").decode("utf-8") 
        db_session.commit()    
        print('Holiday updated successfully!')
        return redirect('/holiday')
    if hday:
        return render_template('edit_holiday.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id) 


@app.route('/timetable_edit', methods=['GET', 'POST'])
def timetable_edit():
    edit_datetype = request.args.get('edit_datetype')
    edit_timetype = request.args.get('edit_timetype')
    print('timetable_edit datetype [%s]  timetype[%s]'%(edit_datetype, edit_timetype))

    qry = db_session.query(TimeTable).filter(TimeTable.c_acdcode=='0202').filter(TimeTable.c_datetype == edit_datetype).filter(TimeTable.c_timetype == edit_timetype)
    t_table = qry.first()
    form = TimeTableForm(formdata=request.form, obj=t_table)
    if request.method == 'POST' and form.validate():
        t_table.c_starttime = form.c_starttime.data      
        t_table.c_endtime = form.c_endtime.data
        db_session.commit()    
        print('TimeTable updated successfully! start:%s end:%s'%(form.c_starttime.data, form.c_endtime.data) )
        return redirect('/worktime')
    if t_table:
        return render_template('edit_timetable.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id) 



init_db()

app.run(host="0.0.0.0", port="8800")    