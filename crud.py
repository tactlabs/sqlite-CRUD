
'''
Created on 

@author: 

source:

'''

import sqlite3

conn = sqlite3.connect('test.db')

def create_table():
    conn.execute("CREATE TABLE CITY (name TEXT, city_name TEXT);")

def insert(name, city_name):
    conn.execute(f"INSERT INTO CITY (name,city_name) VALUES ('{name}','{city_name}'); ")
    conn.commit()

def update_city(new_city):
    conn.execute(f"UPDATE CITY SET city_name = '{new_city}'")
    conn.commit()
    print("City updated")

def read():
    values = conn.execute("SELECT * FROM CITY WHERE name='Monisha'")

    for value in values:
        print(value)

def delete(name):

    conn.execute(f"DELETE FROM CITY WHERE name='{name}'")
    conn.commit()

def startpy():

    # create_table()
    # insert("Monisha","Madurai")
    # update_city("Hyderabad")
    # read()
    # delete("Chaaya")
    # print("Tact101")
    

if __name__ == '__main__':
    startpy()