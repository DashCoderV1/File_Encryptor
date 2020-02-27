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
            self.get_table_info()
            cur.close()
            return True

    def get_table_info(self):
        try:
            cur = self.con.cursor()
            cur.execute(
                f"Pragma table_info({self.table_name})")
            x = cur.fetchall()
            self.table_info = [i[1] for i in x]
            cur.close()
            return True
        except Error:
            return False

    def create_table(self, table_inf):
        try:
            columns_string = ",".join([" ".join(column)
                                       for column in table_inf])
            cur = self.con.cursor()
            cur.execute(
                f"create table {self.table_name} ({columns_string})")
            self.con.commit()
            cur.close()
            return True
        except Error:
            return False

    def drop_table(self):
        try:
            cur = self.con.cursor()
            cur.execute(
                f"drop table {self.table_name}")
            self.con.commit()
            cur.close()
            return True
        except Error:
            return False

    def insert_in_table(self, data, columns):
        if (columns != []):
            columns_string = "(" + ",".join(columns) + ")"
        data_string = f"({','.join(['?' for i in range(len(data))])})"
        data_tup = tuple(data)
        try:
            cur = self.con.cursor()
            cur.execute(
                f"insert into {self.table_name} {columns_string} values {data_string}", data_tup)
            self.con.commit()
            cur.close()
            return True
        except Error:
            return False

    def update_in_table(self, data, condition):
        try:
            cur = self.con.cursor()
            cur.execute(
                f"update {self.table_name} set {data}" + ((" where " + condition) if condition else ""))
            self.con.commit()
            cur.close()
            return True
        except Error:
            return False

    def delete_in_table(self, condition):
        try:
            cur = self.con.cursor()
            cur.execute(
                f"delete  from {self.table_name}" + ((" where " + condition) if condition else ""))
            self.con.commit()
            cur.close()
            return True
        except Error:
            return False

    def get_table_data(self, condition):
        cur = self.con.cursor()
        column_stg = ",".join(self.table_info)
        cur.execute(
            (f"select {column_stg} from  {self.table_name} " + (("where " + condition) if condition else "")))
        data = cur.fetchone()
        cur.close()
        if (data == None):
            return False
        return data

    def print_data(self):
        cur = self.con.cursor()
        column_stg = ",".join(self.table_info[0:-1])
        cur.execute(
            (f"select {column_stg} from  {self.table_name} "))
        tup = cur.fetchall()
        if (tup == []):
            return False
        stg = "\t".join(self.table_info[:-1]) + "\n"

        for i in tup:
            for j in i:
                stg += (str(j) + "\t")
            stg += "\n"
        return stg

    def __del__(self):
        self.con.commit()
        self.con.close()
