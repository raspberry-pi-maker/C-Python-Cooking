#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

#This makes 2 flask processes
#export FLASK_ENV=development

export FLASK_APP="/usr/local/src/flask_web/flask_main.py"
cd /usr/local/src/flask_web
/usr/bin/nohup /usr/local/bin/flask run --host=0.0.0.0 --port=880 &
#flask run --host=0.0.0.0 --port=880 2>/dev/null
#/usr/local/src/flask_web/main.py &

 

