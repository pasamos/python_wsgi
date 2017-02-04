# ccSystem db create
import sqlite3

#if not exists, it will create the file
conn=sqlite3.connect('ccSystem.db')
cursor = conn.cursor()

# create table user
cursor.execute('create table user (id varchar(20) primary key, name varchar(20), password varchar(20) )')
cursor.execute('insert into user (id, name, password) values (\'admin\', \'Admin\', \'admin\')')
cursor.execute('insert into user (id, name, password) values (\'test\', \'Test\', \'test\')')
conn.commit()

cursor.execute('select * from user')
values = cursor.fetchall()
print values
cursor.close()
conn.close()
