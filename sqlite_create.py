import sqlite3
import csv
import os.path

def load_data1(path='./Restaurant.csv'):
    Rest = list()
    with open('./Restaurant.csv','r') as f:
        for line in f.readlines()[1:]:
            Rest.append(line.rstrip().split(','))
    return Rest

def load_data2(path='./Address.csv'):
    Add = list()
    with open('./Address.csv','r') as f:
        for line in f.readlines()[1:]:
            Add.append(line.rstrip().split(','))
    return Add


def connect_db(path=''):
    conn = sqlite3.connect('data.db')
    return conn


'''def create_table(_cursor):
    _cursor.execute(CREATE TABLE IRIS
                        ( ID           INTEGER   PRIMARY KEY    AUTOINCREMENT,
                          SEPAL_LENGTH REAL                 NOT NULL,
                          SEPAL_WIDTH  REAL                 NOT NULL,
                          PETAL_LENGTH REAL                 NOT NULL,
                          PETAL_WIDTH  REAL                 NOT NULL,
                          SPECIES      CHAR(50)             NOT NULL);)
    pass
'''


def insert_item1(a,b,c,d,e,f,g,h,_cursor):
    command = "INSERT INTO Restaurant (Name, Phone, Style, OT, Facebook, Seat, Payment, Line) \
            VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %d, %d, \'%s\');" % (a,b,c,d,e,f,g,h)
    _cursor.execute(command)

    pass

def insert_item2(a,b,c,d,_cursor):
    command = "INSERT INTO Address (Area, District, Street, RestaurantName) VALUES (\'%s\', \'%s\', \' %s\', \'%s\');" % (a,b,c,d)
    _cursor.execute(command)

    pass


if __name__=="__main__":
    data1 = load_data1()
    data2 = load_data2()
    conn = connect_db()
    for items in data1:
        insert_item1(items[0],items[1],items[2],items[3],items[4],int(items[5]),int(items[6]),items[7], conn.cursor())
    for items in data2:
        insert_item2(items[0],items[1],items[2],items[3],conn.cursor())
    conn.commit()
    conn.close()
