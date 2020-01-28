import sqlite3
import os

default = os.path.join(os.path.dirname(__file__), "DB1.db")
const = "insert into Hello (S_id, Stg) values (?,?)"
con = sqlite3.connect(default)
cur = con.cursor()
cur.execute(
    "Select count(*) from sqlite_master where type='table' and name='Hello' ")
if (cur.fetchone()[0] == 0):
    cur.execute("CREATE TABLE Hello (S_id integer primary key, Stg text)")
    print("Creating New Table")

for i in range(int(input("Enter Rows:"))):
    id, stg = input("Enter Elements").split()
    cur.execute(const, (int(id), stg))

con.commit()
cur.execute("Select * from Hello")

results = list(cur.fetchall())
for i in results:
    print(i)

con.close()
