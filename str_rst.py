import sqlite3
import os

FILE = input("Enter File Name")
File_Loc = os.path.join(os.path.dirname(__file__), (FILE + ".db"))


def table_print():
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    cur.execute(
        f"Select name from sqlite_master where type='table'")
    table_name = [i[0] for i in cur.fetchall()]
    con.close()
    return table_name


def table_exists(table_name):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    cur.execute(
        f"Select count(*) from sqlite_master where type='table' and  name='{table_name}' ")
    if (cur.fetchone()[0] == 0):
        con.close()
        return False
    else:
        con.close()
        return True


def column_print(table_name):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    cur.execute(
        f"Pragma table_info({table_name})")
    columns = [i[1] for i in cur.fetchall()]
    con.close()
    return columns


def column_exists(table_name, col_name):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    cur.execute(
        f"Pragma table_info({table_name})")
    columns = [i[1].lower() for i in cur.fetchall()]
    con.close()
    if (col_name.lower() in columns):
        return True
    else:
        return False


def create_table(table_name, columns):
    con = sqlite3.connect(File_Loc)
    columns_string = ",".join([" ".join(column) for column in columns])
    cur = con.cursor()
    cur.execute(
        f"create table {table_name} ({columns_string})")
    con.commit()
    con.close()


def drop_table(table_name):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    cur.execute(
        f"drop table {table_name}")
    con.commit()
    con.close()


def insert_in(table_name, data, columns=[]):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    columns_string = ""
    if (columns != []):
        columns_string = "(" + ",".join(columns) + ")"
    data_string = "(" + ",".join(data) + ")"
    cur.execute(
        f"insert into {table_name} {columns_string} values {data_string}")
    con.commit()
    con.close()


def update_table(table_name, upd, cond=""):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    cur.execute(
        f"update {table_name} set {upd}" + ((" where " + cond) if cond else ""))
    con.commit()
    con.close()


def delete_table(table_name, cond=""):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    cur.execute(
        f"delete  from {table_name}" + ((" where " + cond) if cond else ""))
    con.commit()
    con.close()


def print_table(table_name, columns=["*"], cond=""):
    con = sqlite3.connect(File_Loc)
    cur = con.cursor()
    column_stg = ",".join(columns)
    cur.execute(
        (f"select {column_stg} from  {table_name} " + (("where " + cond) if cond else "")))
    tup = list(cur.fetchall())
    stg = ""
    for i in tup:
        for j in i:
            stg += (str(j) + "\t")
        stg += "\n"
    con.close()
    return stg


print(print_table("User_Files"))
