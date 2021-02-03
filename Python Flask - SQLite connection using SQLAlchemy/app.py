# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/local/src/study/flask_sqlite/callback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "flask rocks!"

db = SQLAlchemy(app)

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
@app.route('/')
def Index():
    all_data = MyCallback.query.all()
 
    return render_template("index.html", t_callback = all_data)
    #return render_template("test.html")


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