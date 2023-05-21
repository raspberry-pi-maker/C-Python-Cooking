import pyodbc
import sys

server = "192.168.150.128"
user = "study_user"
password = "study"
db = "study_db"


try:
    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 8.0 Unicode Driver};SERVER=' + server + ';DATABASE='+db+';UID='+user+';PWD=' + password)
except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    sqlstate = sqlstate.split(".")
    print("SQL Connect Error")
    sys.exit(0)
cursor = cnxn.cursor()

sql =  '''select name, belong, phone from professor'''
res =  cursor.execute(sql)
for r in res:
    print(r[0], " ",  r[1], " ", r[2])

cnxn.commit()
cnxn.close()
    