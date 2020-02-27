from Users import User
import os
import time
import getpass

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

user = None
os.system("cls")
print("Enter 1 to Login")
print("Enter 2 to Register")
x = input("Enter Choice:")
if (x == "2"):
    os.system("cls")
    # Register Screen
    print("\n\n\n\n\n\n\t\t", "UserName", end="\t")
    user_name = input()
    print("\n\t\tPassword", end="\t")
    password = input()
    user = User(user_name, password)
    if (user.check_user()):
        print(user_name, " Already Registered")
    else:
        user.new_user()
        print("Welcome ", user_name)

elif (x == "1"):
    # Login Screen
    os.system("color 5f")
    user = None
    for i in range(3):
        os.system("cls")
        print("\n\n\n\n\n\n\t\t", "UserName", end="\t")
        user_name = input()
        print("\n\t\t ", end="\t")
        password = getpass.getpass()
        user = User(user_name, password)
        if (user.check_user()):
            break
        else:
            input("Wrong Username or Password Try Again")

    else:
        input("Exceeded Login Attempt Try Again Later")
        exit()

else:
    print("Wrong Input Exiting")
    time.sleep(0.75)
    exit()
os.system("cls")

print("Welcome ",user.User_name)

while(True):
    print("Enter 1 for Hiding The File")
    print("Enter 2 for Retrieving The File")
    #print("Enter 3 for Retrieve in Temporary_File")
    print("Enter 4 for Hiding The Folder")
    print("Enter 5 for Retrieving The Folder")
    print("Enter 6 for Exiting")
    choice = input("Enter Your Choice:")

    if (choice == "1"):
        os.system("cls")
        filename = input("Enter the Full Path Name Of File:")
        if (user.Store_File(filename)):
            print("File Hidden")
        else:
            print("Error Occured")
            continue

    elif (choice == "2"):
        os.system("cls")
        if (not user.print_data()):
            print("No Files To Retreieve")
            continue
        else:
            print(user.print_data())
        file_sno = input("Enter Sno Of File")
        if (user.Retrieve_File(file_sno)):
            print("File Retreieved")
        else:
            print("Error Occured")
    #Work in Progress
    # elif (choice == 3):

    elif (choice == "4"):
        os.system("cls")
        folder = input("Enter the Full Path Name Of Folder:")
        if (user.Store_Zip(folder)):
            print("Folder Hidden")
        else:
            print("Error Occured")
            continue

    elif (choice == "5"):
        os.system("cls")
        if (not user.print_data()):
            print("No Folder To Retreieve")
            continue
        else:
            print(user.print_data())
        file_sno = input("Enter Sno Of Folder")
        if (user.Retrieve_Zip(file_sno)):
            print("Folder Retreieved")
        else:
            print("Error Occured")
    elif (choice == "6"):
        break
    else:
        print("Wrong Choice")
    time.sleep(0.75)
    os.system("cls")
