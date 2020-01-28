import sqlite3
from sqlite3 import Error
import os


class Data_Base:
    def __init__(self, File_Name):
        try:
            self.con = sqlite3.connect(os.path.join(
                os.path.dirname(__file__), (File_Name + ".db")))
        except Error:
            print("Error Cannot Connect to Data Base")
        self.table_name = ""
        self.table_info = []

    def table_exists(self, table):
        self.table_name = table
        cur = self.con.cursor()
        cur.execute(
            f"Select count(*) from sqlite_master where type='table' and  name='{self.table_name}' ")
        if (cur.fetchone()[0] == 0):
            cur.close()
            return False
        else:
            cur.close()
            return True

    def get_table_info(self):
        cur = self.con.cursor()
        cur.execute(
            f"Pragma table_info({self.table_name})")
        x=cur.fetchall()
        self.table_info = [i[1] for i in x]
        cur.close()


    def create_table(self, table_inf):
        self.table_info = table_inf
        columns_string = ",".join([" ".join(column)
                                   for column in self.table_info])
        cur = self.con.cursor()
        cur.execute(
            f"create table {self.table_name} ({columns_string})")
        self.con.commit()
        cur.close()

    def drop_table(self):
        cur = self.con.cursor()
        cur.execute(
            f"drop table {self.table_name}")
        self.con.commit()
        cur.close()

    def insert_in_table(self, data, columns):
        cur = self.con.cursor()
        if (columns != []):
            columns_string = "(" + ",".join(columns) + ")"
        data_string=f"({','.join(['?' for i in range(len(data))])})"
        data_tup=tuple(data)
        cur.execute(
            f"insert into {self.table_name} {columns_string} values {data_string}",data_tup)
        self.con.commit()
        cur.close()

    def update_in_table(self, data, condition):
        cur = self.con.cursor()
        cur.execute(
            f"update {self.table_name} set {data}" + ((" where " + condition) if condition else ""))
        self.con.commit()
        cur.close()

    def delete_in_table(self, condition):
        cur = self.con.cursor()
        cur.execute(
            f"delete  from {self.table_name}" + ((" where " + condition) if condition else ""))
        self.con.commit()
        cur.close()

    def get_table_data(self, condition):
        cur = self.con.cursor()
        column_stg = ",".join(self.table_info)
        cur.execute(
            (f"select {column_stg} from  {self.table_name} " + (("where " + condition) if condition else "")))
        data = cur.fetchone()
        cur.close()
        return data

    def __str__(self, condition=""):
        cur = self.con.cursor()
        column_stg = ",".join(self.table_info)
        cur.execute(
            (f"select {column_stg} from  {self.table_name} " + (("where " + condition) if condition else "")))
        tup = cur.fetchall()
        stg = "\t".join(self.table_info) + "\n"
        for i in tup:
            for j in i:
                stg += (str(j) + "\t")
            stg += "\n"
        return stg

    def __del__(self):
        self.con.commit()
        self.con.close()
