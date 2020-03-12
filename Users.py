from database import Data_Base
import os
from os import path
import shutil


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


class User(Data_Base):
    def __init__(self, name, password, file_name="Data"):
        super().__init__(file_name)
        self.User_name = name
        self.Password = password
        self.tables=["file","folder"]

    def change_user(self, name, password):
        self.User_name = (name if name else self.User_name)
        self.Password = (password if password else self.Password)

    def get_table_name(self,var):
        return (self.User_name+self.Password+self.tables[var])

    def check_user(self):
        for i in range(len(self.tables)):
            if (not super().table_exists(self.get_table_name(i))):
                return False
        else:
            return True

    def new_user(self):
        for i in range(len(self.tables)):
            self.table_name = self.get_table_name(i)
            super().create_table([["sno", "integer", "primary key", "AUTOINCREMENT"], [
                f"{self.tables[i]}_name", "text"], ["Location", "text"], [f"{self.tables[i]}", "blob"]])
        self.con.commit()

    def Store_File(self,filename):
        if (not super().table_exists(self.get_table_name(0))):
            return False
        data = file_Read(filename)
        if (data == False):
            print("File Does not Exists")
            return False
        location,name=path.split(filename)
        if (not super().insert_in_table(
                [name, location, data], self.table_info[1:])):
            print("Error in Data Base Try Again")
            return False
        if (file_Delete(filename)):
            return True
        else:
            print("Error In Deletion")
            super().delete_in_table(f"{self.tables[0]}_name='{filename}'")
            return False

    def Retrieve_File(self,file_sno):
        if (not super().table_exists(self.get_table_name(0))):
            return False
        Data = super().get_table_data(f"sno={file_sno}")
        if (not Data):
            print("File Does Not Exists In Data Base")
            return False
        Sno, File_Name,location, File = Data
        if (file_Write(path.join(location, File_Name), File)):
            if (super().delete_in_table(f"sno={file_sno}")):
                return True
            else:
                file_Delete(File_Name)
                return False
        else:
            return False

    def Store_Zip(self, pth):
        if (not super().table_exists(self.get_table_name(1))):
            return False
        name = path.split(pth)[1]
        base_name = path.join(path.curdir,name)
        if (not path.isdir(pth)):
            print("Folder Does Not Exists")
            return False
        try:
            shutil.make_archive(base_name, "tar", pth)
        except shutil.Error:
            print("Error Occured In Archieve")
            return False
        data = file_Read(name + ".tar")
        file_Delete(name + ".tar")
        if (not super().insert_in_table(
                [name, pth, data], self.table_info[1:])):
            print("Error in Data Base Try Again")
            return False
        try:
            shutil.rmtree(pth)
            return True
        except shutil.Error:
            print("Error Occured In Deletion")
            super().delete_in_table(f"{self.tables[1]}_name='{pth}'")
            return False

    def Retrieve_Zip(self, zip_sno):
        if (not super().table_exists(self.get_table_name(1))):
            return False
        Data = super().get_table_data(f"sno={zip_sno}")
        if (not Data):
            print("Folder Does Not Exists In Data Base")
            return False
        Sno, Zip_Name, pth, zip = Data
        if (not file_Write(Zip_Name+".tar",zip)):
            print("Issue in writing tar")
            return False
        try:
            shutil.unpack_archive(Zip_Name + ".tar", pth)
            file_Delete(Zip_Name + ".tar")
        except shutil.Error:
            print("Error Occured In Unpacking Data")

        if (not super().delete_in_table(f"sno={zip_sno}")):
            shutil.rmtree(pth)
            return False
        return True
