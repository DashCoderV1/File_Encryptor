from database import Data_Base
import os


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

    def change_user(self, name, password):
        self.User_name = (name if name else self.User_name)
        self.Password = (password if password else self.Password)

    def get_table_name(self):
        return (self.User_name)

    def check_user(self):
        if (super().table_exists(self.get_table_name())):
            super().get_table_info()
            return True
        else:
            return False

    def new_user(self):
        super().create_table([["sno", "integer", "primary key", "AUTOINCREMENT"], [
                             "file_name", "text"], ["File", "blob"]])
        super().get_table_info()

    def Store_File(self,filename):
        data = file_Read(filename)
        if (data == False):
            print("File Does not Exists")
            return False
        if (not super().insert_in_table(
                [filename, data], self.table_info[1:])):
            print("Error in Data Base Try Again")
            return False
        if (file_Delete(filename)):
            return True
        else:
            print("Error In Deletion")
            super().delete_in_table(f"file_name='{filename}'")
            return False

    def Retrieve_File(self,file_sno):
        Data = super().get_table_data(f"sno={file_sno}")
        if (not Data):
            print("File Does Not Exists In Data Base")
            return False
        Sno, File_Name, File = Data
        if (file_Write(File_Name, File)):
            if (super().delete_in_table(f"sno={file_sno}")):
                return True
            else:
                file_Delete(File_Name)
                return False
        else:
            return False
