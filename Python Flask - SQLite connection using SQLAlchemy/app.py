# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import datetime

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/local/src/study/flask_sqlite/callback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "flask rocks!"

db = SQLAlchemy(app)

#DatePicker
class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

#Creating model table for our CRUD database
class MyCallback(db.Model):
    __tablename__ = 't_callback'
    c_date = db.Column(db.String(8), primary_key=True)
    c_time = db.Column(db.String(8), primary_key=True)
    c_ani = db.Column(db.String, primary_key=True)
    c_dnis = db.Column(db.String, nullable=False)
    c_callback_num = db.Column(db.String)
    c_callback_date = db.Column(db.String(8))
    c_callback_time = db.Column(db.String(8))
    c_complete = db.Column(db.String(1),index=True)  #Y:completed , N:Not completed
    c_del = db.Column(db.String(1))       #Y:deleted , N:Not deleted
    def __init__(self, date, ani, dnis, callback_num):
       self.c_date = date
       self.c_time = time
       self.c_ani = ani
       self.c_dnis = dnis
       self.c_callback_num = callback_num
       self.c_callback_date = ''
       self.c_complete = 'N'
       self.c_del = 'N'

#This is the index route where we are going to
#query on all our employee data
@app.route('/', methods=['GET','POST'])
def Index():
    form = InfoForm()
    if form.validate_on_submit():
        session['startdate'] = str(form.startdate.data)[:4] +  str(form.startdate.data)[5:7] + str(form.startdate.data)[-2:]      #2021-02-02
        session['enddate'] = str(form.enddate.data)[:4] +  str(form.enddate.data)[5:7] + str(form.enddate.data)[-2:]
        print(session['startdate'])
        print(session['enddate'])
        all_data = db.session.query(MyCallback).filter(MyCallback.c_date <= session['enddate']).filter(MyCallback.c_date >= session['startdate'])
    else:    
        all_data = MyCallback.query.all()
    print('Query Count:%d'%all_data.count())
    return render_template("index.html", t_callback = all_data, form=form, count = all_data.count() )
    # return render_template("test.html")


#this is our update route where we are going to update our employee
@app.route('/update/<c_date>/<c_time>/<c_ani>/', methods = ['GET', 'POST'])
def update(c_date, c_time, c_ani):
    now = datetime.datetime.now()
    formattedDate = now.strftime("%Y%m%d")    
    formattedTime = now.strftime("%H%M%S")    
    qry = db.session.query(MyCallback).filter(MyCallback.c_date==c_date).filter(MyCallback.c_time==c_time).filter(MyCallback.c_ani==c_ani)
    my_data = qry.first()
    my_data.c_complete = 'Y'
    my_data.c_callback_date =  formattedDate
    my_data.c_callback_time =  formattedTime
    db.session.commit()
    return redirect(url_for('Index'))

 
 
 
#This route is for deleting our employee
@app.route('/delete/<c_date>/<c_time>/<c_ani>/', methods = ['GET', 'POST'])
def delete(c_date, c_time, c_ani):
    qry = db.session.query(MyCallback).filter(MyCallback.c_date==c_date).filter(MyCallback.c_time==c_time).filter(MyCallback.c_ani==c_ani)
    my_data = qry.first()
    db.session.delete(my_data)
    db.session.commit()
    flash("콜백 삭제 성공")
    print("Employee Deleted Successfully :" + c_date + ' ' + c_time + ' ' + c_ani)
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)    