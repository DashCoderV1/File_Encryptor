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


def file_Read(file_name):
    try:
        with open(file_name, "rb") as f:
            file = f.read()
        return file
    except FileNotFoundError:
        print("File Not Found")
        return False


def file_Write(file_name, data):
    try:
        with open(file_name, "wb") as f:
            f.write(data)
        return True
    except FileNotFoundError:
        print("File Not Found")
        return False


def file_Delete(file_name):
    if os.path.isfile(file_name):
        try:
            os.remove(file_name)
            return True
        except OSError:
            print("Error Try Again Later")
            return False
    else:
        print(f'Error: {file_name} not a valid filename')
        return False


os.system("color 1f")
dtb = Data_Base("Data_Config")
if (not dtb.table_exists("User_Files")):
    dtb.create_table([["sno", "integer", "primary key", "AUTOINCREMENT"], [
                     "file_name", "text"], ["File", "blob"]])
dtb.get_table_info()
while(True):
    print("Enter 1 for Hiding The File")
    print("Enter 2 for Retrieving The File")
    #print("Enter 3 for Retrieve in Temporary_File")
    print("Enter 4 for Exiting")
    choice = input("Enter Your Choice:")


    if (choice == "1"):
        filename = input("Enter the Full Path Name Of File:")
        data = file_Read(filename)
        if (data == False):
            print("File Does not Exists")
            continue
        if (not dtb.insert_in_table(
                [filename, data], dtb.table_info[1:])):
            print("Error in Data Base Try Again")
            continue
        if (file_Delete(filename)):
            print("File Hidden")
        else:
            print("Error In Deletion")
            dtb.delete_in_table(f"file_name='{filename}'")


    elif (choice == "2"):
        if (not dtb.print_data()):
            print("No Files To Retreieve")
            continue
        else:
            print(dtb.print_data())
        file_sno = input("Enter Sno Of File")

        Data = dtb.get_table_data(f"sno={file_sno}")
        if (not Data):
            print("File Does Not Exists In Data Base")
            continue
        Sno, File_Name, File = Data
        if (file_Write(File_Name, File)):
            dtb.delete_in_table(f"sno={file_sno}")
            print("File Retrieved")
        else:
            print("Error Try Again")


    # elif (choice == 3):

    elif (choice == "4"):
        break
    else:
        print("Wrong Choice")
