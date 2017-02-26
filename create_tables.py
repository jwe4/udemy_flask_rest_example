import sqlite3


connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# have to use INTEGER PRIMARY KEY to get auto incrementing key
create_table = "create table if not exists users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "create table if not exists items(id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)
# cursor.execute("insert into items values('test',10.99)")
connection.commit()
connection.close()
