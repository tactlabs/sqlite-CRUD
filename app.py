
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 

Course work: 

@author: FLASK-INTERN-TEAM

Source:
    https://stackoverflow.com/questions/13279399/how-to-obtain-values-of-request-variables-using-python-and-flask
'''

from flask import Flask, render_template, request, make_response, jsonify
import sqlite3
from sqlite3 import Error
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
from redis import Redis
import socket
from datetime import timedelta
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
redis = Redis(host='localhost', port=6379)

MAX_HIT_COUNT = 5
CACHE_EXPIRE_IN_MINUTES = 1

database = 'test.db'




def get_last_record(conn):
    sql = '''SELECT * FROM flask1 ORDER BY id DESC LIMIT 1'''
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchall()

    if(len(row) <= 0):
        print('No Data available')
        return 1
    
    current_id = row[0][0]
    return current_id+1

def select_all(conn):
    """
    Query all rows in the flask1 table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list


def update_db(conn,update_obj):
    """
    Query all rows in the flask1 table
    :param conn: the Connection object
    :return:
    """
    sql = ''' UPDATE flask1 SET name = :name, dept = :dept where id = :id'''
    cur = conn.cursor()
    cur.execute(sql,update_obj)
    conn.commit()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list

def insert_into_db(conn,insert_obj):

    sql = ''' INSERT INTO flask1 (id,name,dept) 
            VALUES (:id, :name, :dept) '''

    cur = conn.cursor()
    cur.execute(sql, insert_obj)
    conn.commit()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list

def delete_from_db(conn,delete_obj):
    
    sql = ''' DELETE FROM flask1 WHERE id = :id '''

    cur = conn.cursor()
    cur.execute(sql, delete_obj)
    conn.commit()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    
    name = None

    if request.method == 'POST':
        name = request.values.get("name")

    return name

'''
    http://127.0.0.1:5000/api/db/vanilla/select
'''
@app.route('/api/db/vanilla/select')
def api_db_vanilla_select():

    item_list = None
    with sqlite3.connect("test.db") as conn:
        item_list = select_all(conn)

    result = {
        'users' : item_list
    }

    return render_template("show_db_table.html", result=result)


'''
    http://127.0.0.1:5000/api/db/vanilla/update
'''
@app.route('/api/db/vanilla/update/<id>/<name>/<dept>',methods = ['GET','POST'])
def api_db_vanilla_update(id,name,dept):
    id = int(id)
    if request.method == "POST":
        name = request.form['name']
        dept = request.form['dept']
        item_list = None
        with sqlite3.connect("test.db") as conn:
            update_obj = {
                "id": id,
                "name": name,
                "dept": dept
            }
        item_list = update_db(conn,update_obj)
        result = {
        'users' : item_list
        }
        return render_template("insert_into_db.html", result=result)

    return render_template("update_db.html",id=id,name=name,dept=dept)


'''
    http://127.0.0.1:5000/api/db/vanilla/insert
'''
@app.route('/api/db/vanilla/insert',methods = ['GET', 'POST'])
def api_db_vanilla_insert():
    if request.method == 'POST':
        #id = request.form['id']
        
        name = request.form['name']
        dept = request.form['dept']
        item_list = None
        with sqlite3.connect("test.db") as conn:
            id = get_last_record(conn)
            print("LAST RECORD ID ::: ",id)
            insert_obj = {
                "id": id,
                "name": name,
                "dept": dept
            }
        item_list = insert_into_db(conn,insert_obj)
        result = {
        'users' : item_list
        }

        return render_template("insert_into_db.html", result=result)
    
    item_list = None
    with sqlite3.connect("test.db") as conn:
        item_list = select_all(conn)

    result = {
        'users' : item_list
    }
    
    return render_template("insert_into_db.html", result=result)

'''
    http://127.0.0.1:5000/api/db/vanilla/delete/107
'''
@app.route('/api/db/vanilla/delete/<id>')
def api_db_vanilla_delete(id):

    item_list = None
    with sqlite3.connect("test.db") as conn:
        delete_obj = {
            "id": id,
        }
        item_list = delete_from_db(conn,delete_obj)

    result = {
        'users' : item_list
    }

    return render_template("insert_into_db.html",result=result)





if __name__ == "__main__":
    app.run(debug=True)