# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
my_ip = '192.168.11.206'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ivr:ROOT@mysql123@%s/test'%(my_ip)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "flask rocks!"
app.config['MYSQL_CHARSET'] = 'utf8'

db = SQLAlchemy(app)
#db_session = db.create_scoped_session()
