from Data_Base import Data_Base
import os
import time
import getpass


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


def file_Temporary_Write(file_name, file):
    pass

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


# Welcome Screen
lis = ["17", "71", "47"]
print('\t\t\t\t\tFile Encryption')
scroll = "\n\n\n\n\n\n\n\n\n\n\n\t\t\t"
convey = ["Welcome To My Project ",
          "\t\t\t\t\tOn File Encryption", "\t\t\t\t\t\t Krishna"]
for i in range(3):
    os.system("color " + lis[i])
    print(scroll[i:], end="\t")
    for i in convey[:(i + 1)]:
        print(i)
    time.sleep(1.5)
    os.system("cls")
    print('\t\t\t\t\tFile Encryption')

os.system("color 5f")
for i in range(3):
    os.system("cls")
    print('\t\t\t\t\tFile Encryption and Hiding')
    print("\n\n\n\n\n\t\t", "UserName", end="\t")
    user = input()
    print("\n\t\t", end="\t")
    password = getpass.getpass()

    if user == "Admin" and password == "Admin":
        os.system("cls")
        print("Welcome Admin")
        break

    else:
        input("Wrong Username or Password Try Again")

else:
    input("Exceeded Login Attempt Try Again Later")
    exit()


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
        os.system("cls")
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
        os.system("cls")
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

    #Work in Progress
    elif (choice == 3):
        os.system("cls")
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
        if (file_Temporary_Write(File_Name, File)):
            print("File Opened")
        else:
            print("Error Try Again")

    elif (choice == "4"):
        break
    else:
        print("Wrong Choice")
    input("Enter")
    os.system("cls")
